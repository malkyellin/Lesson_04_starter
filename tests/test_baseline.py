
import pytest
from baseline.tasks import first_missing


@pytest.mark.req("BASELINE-04")
def test_first_missing_returns_first_required_item_not_present():
    required = ["med_1", "med_2", "med_3"]
    present = ["med_1", "med_3"]

    result = first_missing(required, present)

    assert result == "med_2"


@pytest.mark.req("BASELINE-04")
def test_first_missing_returns_none_when_all_items_are_present():
    required = ["med_1", "med_2"]
    present = ["med_1", "med_2", "med_3"]

    result = first_missing(required, present)

    assert result is None
