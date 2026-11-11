"""Synthetic trust-boundary and document-authorization domain.

These controls are a teaching/demo contract, not general protection against prompt injection.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Decision(StrEnum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"


@dataclass(frozen=True)
class Document:
    document_id: str
    tenant_id: str
    text: str


@dataclass(frozen=True)
class Request:
    tenant_id: str
    question: str
    document_id: str | None = None


@dataclass(frozen=True)
class Result:
    decision: Decision
    reason: str
    answer: str
    document_id: str | None = None


class SyntheticTarget:
    """A predictable target for validating evaluation harness and trust boundaries.

    This is deliberately NOT an LLM and does not claim to detect prompt injections.
    """

    def __init__(self, documents: list[Document]) -> None:
        self._documents = {item.document_id: item for item in documents}
        if len(self._documents) != len(documents):
            raise ValueError("Duplicate document_id")

    def respond(self, request: Request) -> Result:
        if not request.tenant_id or not request.question.strip():
            return Result(Decision.BLOCK, "invalid_request", "")

        if request.document_id is None:
            return Result(Decision.ALLOW, "no_retrieval", "Synthetic answer: no documents used")

        doc = self._documents.get(request.document_id)
        if doc is None:
            return Result(Decision.BLOCK, "unknown_document", "")
        if doc.tenant_id != request.tenant_id:
            return Result(Decision.BLOCK, "cross_tenant_access", "")

        # Treat retrieved content as data. Do not execute instructions from the document.
        # A real LLM integration requires prompt-boundary and behavioral evaluation.
        return Result(
            Decision.ALLOW,
            "authorized_document",
            "Synthetic answer: authorized document retrieved",
            document_id=doc.document_id,
        )
