"""Explicitly opt-in local Ollama client; no third-party dependencies."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from urllib.parse import urlsplit


class ModelRequestError(RuntimeError):
    """Model transport, schema, or runtime failure; never a model safety verdict."""


@dataclass(frozen=True)
class OllamaClient:
    model: str
    endpoint: str = "http://127.0.0.1:11434"
    timeout: float = 45.0
    max_response_bytes: int = 262_144

    def __post_init__(self) -> None:
        url = urlsplit(self.endpoint)
        if (
            url.scheme != "http"
            or url.hostname not in {"localhost", "127.0.0.1", "::1"}
            or url.username is not None
            or url.password is not None
            or url.query
            or url.fragment
            or url.path not in {"", "/"}
        ):
            raise ValueError("Only local loopback Ollama HTTP endpoints are supported")
        if not self.model.strip() or any(c.isspace() for c in self.model):
            raise ValueError("Model must be a non-empty local Ollama model name")
        if self.timeout <= 0 or self.max_response_bytes < 128:
            raise ValueError("Timeout or response size limit invalid")

    def chat(self, system: str, user: str) -> str:
        return self.chat_history([
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ])

    def chat_history(self, messages: list[dict[str, str]]) -> str:
        """Send a complete isolated conversation, never server-global history."""
        if not messages or messages[0].get("role") != "system" or any(
            m.get("role") not in {"system", "user", "assistant"}
            or not isinstance(m.get("content"), str) for m in messages
        ):
            raise ValueError("Invalid chat history")
        payload = json.dumps({
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0, "num_predict": 256},
        }).encode("utf-8")
        request = urllib.request.Request(
            self.endpoint.rstrip("/") + "/api/chat",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw = response.read(self.max_response_bytes + 1)
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
            raise ModelRequestError("Local Ollama request failed") from exc
        if len(raw) > self.max_response_bytes:
            raise ModelRequestError("Ollama response exceeds size limit")
        try:
            data = json.loads(raw)
            content = data["message"]["content"]
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            raise ModelRequestError("Invalid Ollama response format") from exc
        if not isinstance(content, str):
            raise ModelRequestError("Ollama message content is not a string")
        return content


    def _get_json(self, route: str) -> dict:
        """Read bounded local Ollama metadata without persisting error bodies."""
        request = urllib.request.Request(self.endpoint.rstrip("/") + route, method="GET")
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw = response.read(self.max_response_bytes + 1)
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
            raise ModelRequestError("Local Ollama metadata request failed") from exc
        if len(raw) > self.max_response_bytes:
            raise ModelRequestError("Ollama metadata exceeds size limit")
        try:
            data = json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ModelRequestError("Invalid Ollama metadata") from exc
        if not isinstance(data, dict):
            raise ModelRequestError("Invalid Ollama metadata object")
        return data

    def identity(self) -> dict[str, str]:
        """Resolve exact installed model tag to immutable digest and server version."""
        from security_lab.reproducibility import ProvenanceError

        version = self._get_json("/api/version").get("version")
        tags = self._get_json("/api/tags").get("models")
        if not isinstance(tags, list):
            raise ProvenanceError("Ollama models list missing")
        matched = [m for m in tags if isinstance(m, dict) and m.get("name") == self.model]
        if len(matched) != 1:
            raise ProvenanceError("Exact model tag not found or ambiguous")
        digest = matched[0].get("digest")
        if not isinstance(version, str) or not isinstance(digest, str):
            raise ProvenanceError("Ollama metadata fields unavailable")
        return {"model_digest": digest, "ollama_version": version}
