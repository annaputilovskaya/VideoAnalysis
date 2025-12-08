from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True)
class RecordingSourceId:
    """
    Unique identifier of the recording source within the system.

    Attributes:
        value(UUID): The universally unique identifier of the recording source.
    """

    value: UUID

    @staticmethod
    def new() -> "RecordingSourceId":
        return RecordingSourceId(uuid4())

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class RecordingSourceExtra:
    """
    Optional extra data about a recording source.

    Attributes:
        floor (int | None):
            The building floor level where the source (e.g., camera) is located.
            Defaults to None if unspecified.
        location_label (str | None):
            A human-readable label or description of the physical location.
            Defaults to None if unspecified.
        meta (dict[str, Any]):
            A flexible dictionary for storing arbitrary, unstructured metadata.
            Initialized as an empty dictionary by default using a factory function.
    """

    floor: int | None = None
    location_label: str |str = None
    meta: dict[str, Any] = field(default_factory=dict)


class RecordingSource:
    """
    Recording source (e.g., camera or logical channel).

    This domain-level class aggregates essential information about a recording source:
    its unique identifier and optional extra metadata.

    Attributes:
        idx (RecordingSourceId):
            The unique identifier of the recording source.
        extra (RecordingSourceExtra):
            Optional extra metadata and location details for the source.
            Defaults to an empty RecordingSourceExtra instance.
    """

    idx: RecordingSourceId
    extra: RecordingSourceExtra = RecordingSourceExtra()

    def __init__(
        self,
        idx: RecordingSourceId,
        extra: RecordingSourceExtra = RecordingSourceExtra(),
    ) -> None:
        self.idx: RecordingSourceId = idx
        self.source_id: RecordingSourceExtra = extra
