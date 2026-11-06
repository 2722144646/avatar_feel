from avatar_feel import AffectLog, FeelEngine, FeelRequest


def test_feel_request_validates_and_clamps():
    request = FeelRequest.from_message(
        {"labels": {"happy": 2.0, "tired": "0.4"}, "intensity": 3, "confidence": -1, "note": "ok"}
    )
    assert request.labels == {"happy": 2.0, "tired": 0.4}
    assert request.intensity == 1.0
    assert request.confidence == 0.0
    assert request.note == "ok"


def test_feel_request_rejects_bad_labels():
    try:
        FeelRequest.from_message({"labels": ["happy"]})
    except ValueError as exc:
        assert "labels" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("list labels must be rejected")


def test_engine_blends_mixed_labels_end_to_end(tmp_path):
    log = AffectLog(tmp_path / "affect")
    engine = FeelEngine(log=log)
    result = engine.feel(FeelRequest.from_message({"labels": {"happy": 0.6, "tired": 0.4}, "intensity": 0.8}))

    assert result.state.labels["happy"] == 0.6
    assert result.state.labels["tired"] == 0.4
    assert result.face["smile"] > 0.5
    assert "pitch" in result.head
    assert engine.state().labels["happy"] == 0.6
    assert list((tmp_path / "affect").glob("affect-*.jsonl"))


def test_low_confidence_vote_does_not_move_the_face(tmp_path):
    engine = FeelEngine()
    weak = engine.feel(FeelRequest(labels={"sad": 1.0}, intensity=1.0, confidence=0.0))
    assert weak.state.intensity == 0.0
    assert weak.state.labels == {"neutral": 1.0}


def test_result_is_json_friendly(tmp_path):
    engine = FeelEngine()
    payload = engine.feel(FeelRequest(labels={"angry": 1.0}, intensity=0.7)).to_dict()
    assert payload["ok"] is True
    assert payload["dominant"][0][0] == "angry"
    assert isinstance(payload["face"], dict)
