# -*- coding: utf-8 -*-
"""Wire protocol for the self-report channel.

The capability is protocol-agnostic: any caller (an LLM tool call, an HTTP
endpoint, a local script) turns into one ``FeelRequest``. Validation lives here
so every adapter behaves the same.
"""

from __future__ import annotations

from dataclasses import dataclass

from .schema import AffectEvidence, AffectState


@dataclass(slots=True)
class FeelRequest:
    labels: dict[str, float]
    intensity: float = 0.7
    confidence: float = 0.8
    note: str = ""
    turn_id: str = ""

    @classmethod
    def from_message(cls, message: dict) -> "FeelRequest":
        if not isinstance(message, dict):
            raise TypeError("feel message must be a dict")
        raw_labels = message.get("labels") or {}
        if not isinstance(raw_labels, dict):
            raise ValueError("labels must be an object of label -> weight")
        labels: dict[str, float] = {}
        for key, value in raw_labels.items():
            try:
                labels[str(key)] = float(value)
            except (TypeError, ValueError):
                continue
        return cls(
            labels=labels,
            intensity=_clamp(float(message.get("intensity", 0.7)), 0.0, 1.0),
            confidence=_clamp(float(message.get("confidence", 0.8)), 0.0, 1.0),
            note=str(message.get("note") or ""),
            turn_id=str(message.get("turn_id") or ""),
        )

    def to_evidence(self, source: str = "tool") -> AffectEvidence:
        return AffectEvidence(
            source=source,
            labels=dict(self.labels),
            intensity=self.intensity,
            confidence=self.confidence,
            note=self.note,
            turn_id=self.turn_id,
        )


@dataclass(slots=True)
class FeelResult:
    state: AffectState
    face: dict[str, float]
    head: dict[str, float]

    def to_dict(self) -> dict:
        return {
            "ok": True,
            "labels": dict(self.state.labels),
            "intensity": round(self.state.intensity, 4),
            "confidence": self.state.confidence,
            "valence": round(self.state.valence, 4),
            "arousal": round(self.state.arousal, 4),
            "dominant": self.state.dominant(2),
            "face": dict(self.face),
            "head": dict(self.head),
        }


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))
