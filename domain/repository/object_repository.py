from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from domain.entity.detected_object import DetectedObject, ObjectId, ObjectClass
from domain.entity.record_source import RecordingSourceId
from domain.entity.video_file import VideoFileId


@dataclass
class ObjectSearchCriteria:
    """
    Criteria for searching detected objects.

    This is an abstract filter that can be incrementally extended as new
    scenarios emerge in services.

    Attributes:
        object_classes: List of object classes to filter by.
        source_idx: Unique identifier of the recording source.
        video_idx: Unique identifier of the video file.
        appeared_from: Start of the time range when the object was detected.
        appeared_to: End of the time range when the object was detected.
        attributes: Key-value pairs for filtering based on object metadata.
    """
    object_classes: list["ObjectClass"] | None = None
    source_idx: "RecordingSourceId | None" = None
    video_idx: "VideoFileId | None" = None
    appeared_from: datetime | None = None
    appeared_to: datetime | None = None
    attributes: dict[str, Any] = field(default_factory=dict)


class ObjectRepository(ABC):
    """
    Abstract repository for managing DetectedObject entities.
    """

    @abstractmethod
    def save(self, obj: "DetectedObject") -> None:
        """
        Saves or updates a detected object in the repository.

        Args:
            obj: The DetectedObject instance to persist.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_idx(self, idx: "ObjectId") -> "DetectedObject | None":
        """
        Retrieves an object by its domain identifier.

        Args:
            idx: The unique domain identifier of the object.

        Returns:
            The found DetectedObject instance, or None if no object exists
            with the given ID.
        """
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        criteria: ObjectSearchCriteria,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list["DetectedObject"]:
        """
        Searches for objects matching the specified criteria.

        Args:
            criteria: An ObjectSearchCriteria instance defining the filters.
            limit: Maximum number of objects to return.
            offset: Number of objects to skip for pagination.

        Returns:
            A list of DetectedObject instances matching the criteria.
        """
        raise NotImplementedError
