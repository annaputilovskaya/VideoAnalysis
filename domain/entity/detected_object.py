from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from domain.entity.video_file import VideoFileId


@dataclass(frozen=True)
class ObjectId:
    """
    Unique identifier for an object (person, cart, phone, etc.).

    Attributes:
        value (UUID): The underlying UUID value of the identifier.
    """
    value: UUID

    @staticmethod
    def new() -> "ObjectId":
        """
        Generates a new unique ObjectId using UUID4.

        Returns:
            ObjectId: A new instance with a random UUID.
        """
        return ObjectId(uuid4())

    def __str__(self) -> str:
        """
        Returns the string representation of the UUID.

        Returns:
            str: The UUID as a string.
        """
        return str(self.value)



@dataclass(frozen=True)
class ObjectClass:
    """
    Represents the category of the detected object.

    Used to distinguish between different types of entities such as 'person',
    'cart', 'phone', 'employee', 'thief', etc.

    Attributes:
        value (str): The string name of the object class.
    """
    value: str


@dataclass
class ObjectAttributes:
    """
    Additional characteristics and metadata of an object.

    This class provides a flexible way to store extra features (e.g., gender,
    color, status) without modifying the core entity structure.

    Attributes:
        meta (dict[str, Any]): A dictionary of arbitrary attributes.
            Defaults to an empty dictionary.
    """
    meta: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Coordinate:
    """
    Bounding box coordinates of an object within a frame.

    Attributes:
        x (int): The x-coordinate of the top-left corner.
        y (int): The y-coordinate of the top-left corner.
        width (int): The width of the bounding box.
        height (int): The height of the bounding box.
    """
    x: int
    y: int
    width: int
    height: int


@dataclass(frozen=True)
class FrameRef:
    """
    A reference to a specific frame where an object was captured.

    Uniquely identifies a frame using a combination of the video source
    and the timestamp.

    Attributes:
        video_idx (VideoFileId): Unique identifier of the source video file.
        captured_at (datetime): The timestamp when the frame was captured.
        coordinate (Coordinate): The location of the object in this specific frame.
    """
    video_idx: "VideoFileId"
    captured_at: datetime
    coordinate: Coordinate


class DetectedObject:
    """
    An entity representing an object detected in a video stream.

    Tracks the object's identity, classification, specific attributes,
    and a history of frames where it appeared for further aggregation
    and analytics.

    Attributes:
        idx (ObjectId): The unique domain identifier for the object.
        object_class (ObjectClass): The category of the object.
        attributes (ObjectAttributes): Metadata and extra traits of the object.
        frames (list[FrameRef]): A list of frame references where the object
            was detected.
    """

    def __init__(
        self,
        idx: ObjectId,
        object_class: ObjectClass,
        attributes: ObjectAttributes | None = None,
        frames: list[FrameRef]| None = None,
    ) -> None:
        """
        Initializes a DetectedObject.

        Args:
           idx (ObjectId): Unique identifier for the object.
           object_class (ObjectClass): The type/category of the object.
           attributes (Optional[ObjectAttributes]): Additional metadata.
               Defaults to an empty ObjectAttributes.
           frames (Optional[list[FrameRef]]): Initial list of frame detections.
               Defaults to an empty list.
       """
        self.idx = idx
        self.object_class = object_class
        self.attributes = attributes or ObjectAttributes()
        self.frames: list[FrameRef] = frames or []

    def add_frame(self, frame_ref: FrameRef) -> None:
        """
        Records that the object was detected in an additional frame.

        Args:
            frame_ref (FrameRef): Reference to the frame where the object appeared.
        """
        self.frames.append(frame_ref)

    def last_seen_at(self) -> datetime | None:
        """
        Returns the timestamp of the object's most recent detection.

        Returns:
            datetime | None: The latest captured_at timestamp from the frames history,
                or None if the object has no associated frames.
        """
        if not self.frames:
            return None
        return max(ref.captured_at for ref in self.frames)

    def was_seen_in_range(self, start: datetime, end: datetime) -> bool:
        """
        Checks if the object appeared within the specified time interval.

        Args:
            start (datetime): The beginning of the interval (inclusive).
            end (datetime): The end of the interval (exclusive).

        Returns:
            bool: True if at least one detection falls within the range, False otherwise.
        """
        return any(start <= ref.captured_at < end for ref in self.frames)

    def update_attributes(self, meta: dict[str, Any]) -> None:
        """
        Updates the object's metadata attributes.

        Args:
            meta (dict[str, Any]): A dictionary of attributes to merge into the
                existing object metadata (attributes.meta).
        """
        self.attributes.meta.update(meta)
