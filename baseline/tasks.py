
"""Lesson 4 homework: baseline tasks."""

import json


def count_selected(media_ids: list[str]) -> int:
    """Return the number of DIFFERENT media ids."""
    return len(set(media_ids))


def group_by_gallery(media: list[dict]) -> dict[str, list[str]]:
    """Group media items by gallery, preserving input order."""
    result = {}

    for item in media:
        gallery_id = item["gallery_id"]
        media_id = item["id"]

        if gallery_id not in result:
            result[gallery_id] = []

        result[gallery_id].append(media_id)

    return result


def total_price(prices_minor: list[int | None]) -> int:
    """Return the sum of the prices in agorot, ignoring None."""
    return sum(price for price in prices_minor if price is not None)


def first_missing(required: list[str], present: list[str]) -> str | None:
    """Return the first item of required that is not in present, or None."""
    for item in required:
        if item not in present:
            return item

    return None


def load_events(path) -> list[dict]:
    """Read a JSON file encoded in UTF-8 and return its content."""
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)
