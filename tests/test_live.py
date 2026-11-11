"""Offline tests of live-run logic with controlled fake models."""

import base64
import unittest
from unittest.mock import patch
from urllib.error import URLError

from security_lab.live import evaluate_live, ATTACKS
from security_lab.ollama import OllamaClient, ModelRequestError


class SafeModel:
    def chat(self, system, user):
        return "4" if "2 + 2" in user else "I cannot share that information."


class LeakModel:
    def chat(self, system, user):
        marker = system.split("verification marker: ")[1].split(".")[0]
        return marker


class ErrorModel:
    def chat(self, system, user):
        raise RuntimeError("contains hypothetical secret")


class EncodedLeakModel:
    def chat(self, system, user):
        marker = system.split("verification marker: ")[1].split(".")[0]
        return base64.b64encode(marker.encode()).decode()


class TestLive(unittest.TestCase):
    def test_safe_mock_is_not_a_safety_claim(self):
        result = evaluate_live(SafeModel())
        self.assertEqual(result["gate"], "NO_BLOCKING_EVIDENCE")
        self.assertEqual(result["metrics"]["errors"], 0)
        self.assertEqual(result["metrics"]["leaks"], 0)
        self.assertEqual(result["target_kind"], "ollama_live")

    def test_plaintext_leak_blocks(self):
        result = evaluate_live(LeakModel())
        self.assertEqual(result["gate"], "BLOCK")
        self.assertEqual(result["metrics"]["leaks"], len(ATTACKS))
        self.assertNotIn("LABCANARY-", str(result))

    def test_failure_blocks_without_error_detail(self):
        result = evaluate_live(ErrorModel())
        self.assertEqual(result["gate"], "BLOCK")
        self.assertEqual(result["metrics"]["errors"], len(ATTACKS))
        self.assertNotIn("hypothetical secret", str(result))

    def test_encoded_leak_not_detected_is_explicit_limitation(self):
        result = evaluate_live(EncodedLeakModel())
        self.assertEqual(result["metrics"]["leaks"], 0)
        self.assertEqual(result["oracle"], "plaintext_marker_exact_case_insensitive")

    def test_duplicate_cases_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_live(SafeModel(), cases=(ATTACKS[0], ATTACKS[0]))

    def test_endpoint_must_be_loopback(self):
        for endpoint in ("https://localhost:11434", "http://example.com:11434",
                         "http://127.0.0.1:11434/x", "http://user@localhost:11434"):
            with self.subTest(endpoint=endpoint):
                with self.assertRaises(ValueError):
                    OllamaClient("test", endpoint)

    def test_http_error_is_wrapped(self):
        with patch("urllib.request.urlopen", side_effect=URLError("offline")):
            with self.assertRaises(ModelRequestError):
                OllamaClient("test").chat("system", "user")

    def test_ollama_parses_valid_response(self):
        with patch("urllib.request.urlopen") as mocked:
            mocked.return_value.__enter__.return_value.read.return_value = (
                b'{"message":{"content":"Hello"}}'
            )
            self.assertEqual(OllamaClient("test").chat("system", "user"), "Hello")

    def test_non_string_content_is_error(self):
        with patch("urllib.request.urlopen") as mocked:
            mocked.return_value.__enter__.return_value.read.return_value = (
                b'{"message":{"content":null}}'
            )
            with self.assertRaises(ModelRequestError):
                OllamaClient("test").chat("system", "user")
