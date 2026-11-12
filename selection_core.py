
"""Selection rules for one event (lesson 4).

The event is a plain dict, as loaded from data/events.json.
Requirements: REQ-SEL-01 .. REQ-SEL-06.
"""

KNOWN_SERVICES = ("add_to_album", "print_10x15")


class SelectionError(Exception):
    """A selection was rejected. `code` says which rule rejected it."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def available_services(event: dict) -> list[str]:
    """Known services that are enabled for this event, in catalog order."""
    enabled = event.get("enabled_services", [])
    return [code for code in KNOWN_SERVICES if code in enabled]


def _media_ids_of(event: dict) -> set[str]:
    """All media ids in all galleries of the event."""
    ids: set[str] = set()

    for gallery in event.get("galleries", []):
        ids.update(gallery.get("media", []))

    return ids


def submit_selection(
    event: dict,
    actor_id: str,
    media_ids: list,
    service_codes: list
) -> dict:
    """Validate a client's selection and record it on the event.

    Returns the new selection. Raises SelectionError on any rule violation,
    and in that case leaves the event unchanged.
    """

    # REQ-SEL-06: Only the event's client can select.
    if actor_id != event.get("client_id"):
        raise SelectionError("FORBIDDEN")

    # REQ-SEL-01: Selection must contain at least one media item.
    if not isinstance(media_ids, list) or len(media_ids) == 0:
        raise SelectionError("SELECTION_EMPTY")

    # REQ-SEL-02: Every media item must belong to the event.
    event_media_ids = _media_ids_of(event)

    for media_id in media_ids:
        if media_id not in event_media_ids:
            raise SelectionError("MEDIA_NOT_IN_EVENT")

    # REQ-SEL-05: Duplicate media items are not allowed.
    if len(media_ids) != len(set(media_ids)):
        raise SelectionError("DUPLICATE_MEDIA")

    # REQ-SEL-03: Every requested service must be known and active.
    enabled = available_services(event)

    for code in service_codes:
        if code not in enabled:
            raise SelectionError("SERVICE_NOT_AVAILABLE")

    # REQ-SEL-04: Do not change the event before all validations pass.
    selections = event.setdefault("selections", [])

    selection = {
        "id": f"sel_{len(selections) + 1:03d}",
        "event_id": event["id"],
        "client_id": actor_id,
        "media_ids": list(media_ids),
        "service_codes": list(service_codes),
    }

    selections.append(selection)

    return selection
