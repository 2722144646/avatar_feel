# -*- coding: utf-8 -*-
"""avatar_feel — a self-report channel from an LLM to a face.

Core idea: the model that already read the conversation writes down how it
feels as weighted labels; this package turns that into one continuous state,
blends it into five-feature targets, and hands the targets to whatever
renderer you use. No keyword priority, no forced preset, no extra model.

Author: 2722144646
License: AGPL-3.0; commercial/closed-source license available (COMMERCIAL.md).
"""

from .anchors import EXPRESSION_HEAD, EXPRESSION_TARGETS, NEUTRAL_FACE
from .composer import (
    FACE_KEYS,
    HEAD_KEYS,
    NEUTRAL_HEAD,
    blend_face,
    blend_head,
    compose_face,
    compose_head,
)
from .engine import FeelEngine
from .fusion import DEFAULT_SOURCE_WEIGHT, SOURCE_WEIGHTS, AffectFusion, FusionSettings
from .log import AffectLog, read_log
from .presets import ANCHORS, LABEL_ALIASES, UNKNOWN_ANCHOR, anchor, canonical, is_known
from .protocol import FeelRequest, FeelResult
from .schema import (
    NEUTRAL_LABELS,
    SOURCES,
    AffectEvidence,
    AffectState,
    derive_valence_arousal,
    normalize_labels,
)

__all__ = [
    "ANCHORS",
    "AffectEvidence",
    "AffectFusion",
    "AffectLog",
    "AffectState",
    "DEFAULT_SOURCE_WEIGHT",
    "EXPRESSION_HEAD",
    "EXPRESSION_TARGETS",
    "FACE_KEYS",
    "FeelEngine",
    "FeelRequest",
    "FeelResult",
    "FusionSettings",
    "HEAD_KEYS",
    "LABEL_ALIASES",
    "NEUTRAL_FACE",
    "NEUTRAL_HEAD",
    "NEUTRAL_LABELS",
    "SOURCES",
    "SOURCE_WEIGHTS",
    "UNKNOWN_ANCHOR",
    "anchor",
    "blend_face",
    "blend_head",
    "canonical",
    "compose_face",
    "compose_head",
    "derive_valence_arousal",
    "is_known",
    "normalize_labels",
    "read_log",
]
