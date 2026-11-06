# -*- coding: utf-8 -*-
"""Expression anchors: the shared vocabulary between labels and face targets.

A label ("happy") is not a screenshot and not a preset. It is a *target*
dictionary the composer can blend with other labels. The values came out of
calibrating one specific Live2D model (蒂亚圣诞树树) and are model-agnostic in
shape but not in numbers; a different rig needs its own calibration pass.

Author: 2722144646
Created: 2026-11-06
License: AGPL-3.0 (see LICENSE); commercial/closed-source license available
         (see COMMERCIAL.md).
"""

from __future__ import annotations

# label -> {face unit: target value}
# Units: smile / eye / brow / angry / inner_brow / open / gaze_x / gaze_y /
#        brow_l / brow_r
EXPRESSION_TARGETS: dict[str, dict[str, float]] = {
    "happy": {"smile": 0.95, "eye": 0.90, "brow": 0.30, "angry": 0.0, "inner_brow": 0.04, "open": 0.04},
    "joy": {"smile": 0.99, "eye": 0.94, "brow": 0.35, "angry": 0.0, "inner_brow": 0.03, "open": 0.06},
    "excited": {"smile": 0.97, "eye": 0.96, "brow": 0.55, "angry": 0.0, "inner_brow": 0.03, "open": 0.18},
    "sad": {"smile": 0.0, "eye": 0.38, "brow": 0.02, "angry": 0.0, "inner_brow": 1.0, "open": 0.0, "gaze_x": 0.0, "gaze_y": -0.50, "brow_l": 0.12, "brow_r": 0.12},
    "angry": {"smile": 0.0, "eye": 0.50, "brow": 0.10, "angry": 0.60, "inner_brow": 0.50, "open": 0.02, "gaze_x": -0.25, "gaze_y": 0.10},
    "surprised": {"smile": 0.16, "eye": 1.0, "brow": 0.96, "angry": 0.0, "inner_brow": 0.08, "open": 0.70},
    "surprise": {"smile": 0.16, "eye": 1.0, "brow": 0.96, "angry": 0.0, "inner_brow": 0.08, "open": 0.70},
    "thinking": {"smile": 0.12, "eye": 0.98, "brow": 0.45, "angry": 0.0, "inner_brow": 0.08, "open": 0.02, "gaze_x": 0.85, "gaze_y": 0.55, "brow_l": 0.72, "brow_r": 0.20},
    "wronged": {"smile": 0.06, "eye": 0.58, "brow": 0.04, "angry": 0.0, "inner_brow": 0.82, "open": 0.02, "gaze_x": 0.65, "gaze_y": 0.35, "brow_l": 0.70, "brow_r": 0.20},
    "curious": {"smile": 0.24, "eye": 0.94, "brow": 0.52, "angry": 0.0, "inner_brow": 0.10, "open": 0.08},
    "shy": {"smile": 0.75, "eye": 0.38, "brow": 0.14, "angry": 0.0, "inner_brow": 0.40, "open": 0.02, "gaze_x": -0.50, "gaze_y": 0.55, "brow_l": 0.24, "brow_r": 0.24},
    "neutral": {"smile": 0.14, "eye": 0.93, "brow": 0.10, "angry": 0.0, "inner_brow": 0.04, "open": 0.02},
    "calm": {"smile": 0.20, "eye": 0.90, "brow": 0.08, "angry": 0.0, "inner_brow": 0.06, "open": 0.02},
}

# label -> head bias (degrees are applied by the caller's gain)
EXPRESSION_HEAD: dict[str, dict[str, float]] = {
    "happy": {"yaw": 0.0, "pitch": -0.6, "roll": 1.2},
    "joy": {"yaw": 0.0, "pitch": -0.8, "roll": 1.8},
    "excited": {"yaw": 0.0, "pitch": -0.4, "roll": 2.4},
    "sad": {"yaw": 0.0, "pitch": -7.0, "roll": -3.5},
    "angry": {"yaw": 0.0, "pitch": 3.0, "roll": -6.0},
    "surprised": {"yaw": 0.0, "pitch": -5.0, "roll": 0.0},
    "thinking": {"yaw": 0.0, "pitch": 1.0, "roll": -10.0},
    "wronged": {"yaw": 3.0, "pitch": -2.0, "roll": 7.0},
    "curious": {"yaw": 1.2, "pitch": -0.6, "roll": 3.0},
    "shy": {"yaw": -2.0, "pitch": -10.0, "roll": 5.0},
    "neutral": {"yaw": 0.0, "pitch": 0.0, "roll": 0.0},
    "calm": {"yaw": 0.0, "pitch": 0.0, "roll": 0.4},
}

# The model's own neutral input values. Zero is *not* neutral for this rig:
# sending 0 makes the mouth frown and the brows collapse.
NEUTRAL_FACE: dict[str, float] = {
    "smile": 0.50,
    "eye": 0.55,
    "brow": 0.575,
    "angry": 0.0,
    "inner_brow": 0.0,
    "open": 0.0,
    "gaze_x": 0.0,
    "gaze_y": 0.0,
    "brow_l": 0.0,
    "brow_r": 0.0,
}
