
import json

from baseline.tasks import (
    count_selected,
    group_by_gallery,
    total_price,
    first_missing,
    load_events,
)


def test_count_selected():
    assert count_selected(["a", "b", "a"]) == 2
    assert count_selected([]) == 0


def test_group_by_gallery():
    media = [
        {"gallery_id": "g1", "id": "m1"},
        {"gallery_id": "g2", "id": "m2"},
        {"gallery_id": "g1", "id": "m3"},
    ]

    assert group_by_gallery(media) == {
        "g1": ["m1", "m3"],
        "g2": ["m2"],
    }


def test_total_price():
    assert total_price([100, None, 200, None]) == 300
    assert total_price([]) == 0


def test_first_missing():
    assert first_missing(["a", "b", "c"], ["a", "c"]) == "b"
    assert first_missing(["a", "b"], ["a", "b"]) is None


def test_load_events(tmp_path):
    events = [{"id": "evt_1", "name": "Test"}]

    file_path = tmp_path / "events.json"
    file_path.write_text(
        json.dumps(events, ensure_ascii=False),
        encoding="utf-8",
    )

    assert load_events(file_path) == events
