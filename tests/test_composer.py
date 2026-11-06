from avatar_feel import (
    NEUTRAL_FACE,
    AffectState,
    compose_face,
    compose_head,
    normalize_labels,
)


def _state(labels, intensity=1.0, confidence=0.8):
    return AffectState(labels=normalize_labels(labels), intensity=intensity, confidence=confidence)


def test_neutral_label_keeps_the_model_neutral_inputs():
    face = compose_face(_state({"neutral": 1.0}, 0.9))
    for key, value in NEUTRAL_FACE.items():
        assert abs(face[key] - value) < 1e-9


def test_zero_intensity_is_neutral_even_with_strong_labels():
    face = compose_face(_state({"sad": 1.0}, 0.0))
    assert abs(face["smile"] - NEUTRAL_FACE["smile"]) < 1e-9
    assert abs(face["inner_brow"]) < 1e-9


def test_happy_reaches_its_anchor_at_full_intensity():
    face = compose_face(_state({"happy": 1.0}, 1.0))
    assert face["smile"] > 0.9
    assert face["eye"] > 0.85
    assert face["inner_brow"] < 0.1


def test_sad_and_surprised_are_distinct():
    sad = compose_face(_state({"sad": 1.0}, 1.0))
    surprised = compose_face(_state({"surprised": 1.0}, 1.0))
    assert sad["inner_brow"] > 0.8
    assert sad["eye"] < NEUTRAL_FACE["eye"]
    assert surprised["eye"] > 0.95
    assert surprised["brow"] > sad["brow"]


def test_mixed_labels_land_between_the_anchors():
    happy = compose_face(_state({"happy": 1.0}, 1.0))
    mixed = compose_face(_state({"happy": 0.6, "tired": 0.4}, 1.0))
    assert NEUTRAL_FACE["smile"] < mixed["smile"] < happy["smile"]
    assert mixed["eye"] < happy["eye"]


def test_chinese_aliases_reach_the_same_anchors():
    state = _state({"开心": 1.0}, 1.0)
    assert "happy" in state.labels
    assert compose_face(state) == compose_face(_state({"happy": 1.0}, 1.0))


def test_unknown_label_never_creates_a_strong_expression():
    face = compose_face(_state({"bewildered": 1.0}, 1.0))
    for key, value in NEUTRAL_FACE.items():
        assert abs(face[key] - value) < 1e-9


def test_head_bias_scales_with_intensity():
    full = compose_head(_state({"happy": 1.0}, 1.0))
    half = compose_head(_state({"happy": 1.0}, 0.5))
    assert full["pitch"] < 0
    assert abs(half["pitch"] - full["pitch"] / 2) < 1e-9
    assert compose_head(_state({"happy": 1.0}, 0.0)) == {"yaw": 0.0, "pitch": 0.0, "roll": 0.0}
