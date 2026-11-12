
"""Example tests for selection_core."""

import pytest
import copy
import selection_core


@pytest.mark.req("REQ-SEL-01")
def test_valid_selection_is_returned(sample_event):
    selection = selection_core.submit_selection(
        sample_event,
        "cli_100",
        ["med_1"],
        ["add_to_album"]
    )

    assert selection["media_ids"] == ["med_1"]
    assert selection["service_codes"] == ["add_to_album"]


@pytest.mark.req("REQ-SEL-01")
def test_valid_selection_is_recorded_on_the_event(sample_event):
    selection_core.submit_selection(
        sample_event,
        "cli_100",
        ["med_1", "med_2"],
        ["add_to_album"]
    )

    assert len(sample_event["selections"]) == 1


@pytest.mark.req("REQ-SEL-03")
def test_available_services_lists_enabled_services_only(sample_event):
    assert selection_core.available_services(sample_event) == ["add_to_album"]


@pytest.mark.req("REQ-SEL-02")
def test_media_must_belong_to_event(sample_event):
    with pytest.raises(selection_core.SelectionError) as exc:
        selection_core.submit_selection(
            sample_event,
            "cli_100",
            ["med_9"],
            ["add_to_album"]
        )

    assert exc.value.code == "MEDIA_NOT_IN_EVENT"


@pytest.mark.req("REQ-SEL-05")
def test_duplicate_media_is_rejected(sample_event):
    with pytest.raises(selection_core.SelectionError) as exc:
        selection_core.submit_selection(
            sample_event,
            "cli_100",
            ["med_1", "med_1"],
            ["add_to_album"]
        )

    assert exc.value.code == "DUPLICATE_MEDIA"


@pytest.mark.req("REQ-SEL-04")
def test_rejected_selection_does_not_change_event(sample_event):
    before = copy.deepcopy(sample_event)

    with pytest.raises(selection_core.SelectionError):
        selection_core.submit_selection(
            sample_event,
            "cli_100",
            ["med_9"],
            ["add_to_album"]
        )

    assert sample_event == before


@pytest.mark.req("REQ-SEL-06")
def test_only_event_client_can_submit_selection(sample_event):
    with pytest.raises(selection_core.SelectionError) as exc:
        selection_core.submit_selection(
            sample_event,
            "cli_999",
            ["med_1"],
            ["add_to_album"]
        )

    assert exc.value.code == "FORBIDDEN"
