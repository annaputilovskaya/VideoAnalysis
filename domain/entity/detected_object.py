from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from domain.entity.video_file import VideoFileId


@dataclass(frozen=True)
class ObjectId:
    """Unique identifier for an object (person, cart, phone, etc.).

    Attributes:
        value (UUID): The underlying UUID value of the identifier.
    """
    value: UUID

    @staticmethod
    def new() -> "ObjectId":
        """Generates a new unique ObjectId using UUID4.

        Returns:
            ObjectId: A new instance with a random UUID.
        """
        return ObjectId(uuid4())

    def __str__(self) -> str:
        """Returns the string representation of the UUID.

        Returns:
            str: The UUID as a string.
        """
        return str(self.value)



@dataclass(frozen=True)
class ObjectClass:
    """Represents the category of the detected object.

    Used to distinguish between different types of entities such as 'person',
    'cart', 'phone', 'employee', 'thief', etc.

    Attributes:
        value (str): The string name of the object class.
    """
    value: str


@dataclass
class ObjectAttributes:
    """Additional characteristics and metadata of an object.

    This class provides a flexible way to store extra features (e.g., gender,
    color, status) without modifying the core entity structure.

    Attributes:
        meta (dict[str, Any]): A dictionary of arbitrary attributes.
            Defaults to an empty dictionary.
    """
    meta: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Coordinate:
    """Bounding box coordinates of an object within a frame.

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
    """A reference to a specific frame where an object was captured.

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
    """An entity representing an object detected in a video stream.

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
        """Initializes a DetectedObject.

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
