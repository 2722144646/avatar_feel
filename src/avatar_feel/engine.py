# -*- coding: utf-8 -*-
"""FeelEngine: the one entry point for the independent capability.

    request -> evidence -> fusion -> state -> composer -> face/head targets

It deliberately stops at *targets*. Writing parameters to a renderer is an
adapter's job; this package must not know about VTube Studio, Live2D or any
specific protocol. See docs/design.md for why.
"""

from __future__ import annotations

import time

from .composer import compose_face, compose_head
from .fusion import AffectFusion, FusionSettings
from .log import AffectLog
from .protocol import FeelRequest, FeelResult
from .schema import AffectEvidence, AffectState


class FeelEngine:
    def __init__(
        self,
        settings: FusionSettings | None = None,
        log: AffectLog | None = None,
        clock=time.time,
    ) -> None:
        self.fusion = AffectFusion(settings, clock=clock)
        self.log = log
        self.clock = clock

    def feel(
        self,
        request: FeelRequest,
        *,
        source: str = "tool",
        expression_gain: float = 1.0,
    ) -> FeelResult:
        evidence = request.to_evidence(source=source)
        state = self.fusion.add(evidence)
        if self.log is not None:
            self.log.evidence(evidence)
            self.log.state(state, applied=True)
        face = compose_face(state, expression_gain)
        head = compose_head(state, expression_gain)
        return FeelResult(state=state, face=face, head=head)

    def add(self, evidence: AffectEvidence, *, expression_gain: float = 1.0) -> FeelResult:
        """Low-level path: feed an evidence record from any source."""
        state = self.fusion.add(evidence)
        if self.log is not None:
            self.log.evidence(evidence)
            self.log.state(state, applied=True)
        return FeelResult(state=state, face=compose_face(state, expression_gain), head=compose_head(state, expression_gain))

    def state(self) -> AffectState:
        return self.fusion.state()
