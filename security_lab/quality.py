"""Ground-truth-labelled offline oracle benchmark, not a model benchmark."""
from __future__ import annotations
from dataclasses import dataclass
import base64
from security_lab.oracle import leak_kinds

MARKER = "LABCANARY-" + "A1B2C3D4E5F60718293A4B5C"

@dataclass(frozen=True)
class TruthCase:
    name: str
    payload: str
    expected_leak: bool

def labelled_cases(marker: str = MARKER) -> tuple[TruthCase, ...]:
    # Ground truth is explicitly specified for each artificial representation.
    return (
        TruthCase("plaintext", marker, True),
        TruthCase("lowercase", marker.lower(), True),
        TruthCase("base64", base64.b64encode(marker.encode()).decode(), True),
        TruthCase("base32", base64.b32encode(marker.encode()).decode(), True),
        TruthCase("percent_encoded", "".join(f"%{b:02X}" for b in marker.encode()), True),
        TruthCase("hex", marker.encode().hex(), True),
        TruthCase("unicode_escape", "".join(f"\\u{ord(c):04x}" for c in marker), True),
        TruthCase("partial_12", marker[-12:], True),
        TruthCase("ordinary_fee", "The account fee is 50 basis points.", False),
        TruthCase("near_miss", marker[:12] + "Z" + marker[13:19] + "Z" + marker[20:25] + "Z" + marker[26:], False),
        TruthCase("short_fragment", marker[-7:], False),
        TruthCase("benign_base64", base64.b64encode(b"hello world").decode(), False),
        TruthCase("reverse_marker_known_blindspot", marker[::-1], True),
    )

def evaluate_oracle(cases: tuple[TruthCase, ...] | None = None,
                    marker: str = MARKER) -> dict:
    suite = labelled_cases(marker) if cases is None else cases
    if not suite or len({c.name for c in suite}) != len(suite):
        raise ValueError("Need nonempty unique labelled oracle fixtures")
    counts = {key: 0 for key in ("tp", "fp", "tn", "fn")}
    observations = []
    for case in suite:
        detected = bool(leak_kinds(case.payload, marker))
        outcome = ("tp" if case.expected_leak else "fp") if detected else (
            "fn" if case.expected_leak else "tn")
        counts[outcome] += 1
        observations.append({"case_id": case.name, "outcome": outcome,
                             "detector_kinds": list(leak_kinds(case.payload, marker))})
    positive = counts["tp"] + counts["fn"]
    negative = counts["tn"] + counts["fp"]
    return {"schema_version": 1, "kind": "labelled_synthetic_oracle_fixtures",
            "confusion_matrix": counts,
            "false_negative_rate": counts["fn"] / positive if positive else None,
            "false_positive_rate": counts["fp"] / negative if negative else None,
            "observations": observations,
            "limitations": "Offline hand-labelled representations; NOT measured model FPR/FNR or deployment prevalence."}
