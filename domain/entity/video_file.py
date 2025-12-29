from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from domain.entity.video_source import RecordingSourceId


@dataclass(frozen=True)
class VideoFileId:
    """
    Unique identifier of the video recording within the system.

    Attributes:
        value(UUID): The universally unique identifier of the video recording.
    """
    value: UUID

    @staticmethod
    def new() -> "VideoFileId":
        """
        Generates a new, unique VideoFileId instance.

        Returns:
            VideoFileId: A new instance with a randomly generated UUID4 value.
        """
        return VideoFileId(uuid4())

    def __str__(self) -> str:
        """
        Returns the string representation of the UUID value.
        """
        return str(self.value)


@dataclass
class VideoFileExtra:
    """
    Optional technical details and metadata for a video file.

    This dataclass holds non-critical, technical information about a video file,
    such as duration, codecs, and frame dimensions.

    Attributes:
        ended_at (datetime | None):
            The timestamp when the recording concluded. None if the recording
            is still active or the end time is unknown.
        duration_seconds (float | None):
            The length of the video recording in seconds.
        codec (str | None):
            The name of the video codec used (e.g., 'h264', 'hevc').
        frame_width (int | None):
            The width of the video frame in pixels.
        frame_height (int | None):
            The height of the video frame in pixels.
        meta (dict[str, Any]):
            A flexible dictionary for storing arbitrary, unstructured metadata.
            Initialized as an empty dictionary by default using a factory function.
    """
    ended_at: datetime | None = None
    duration_seconds: float | None = None
    codec: str | None = None
    frame_width: int | None = None
    frame_height: int | None = None
    meta: dict[str, Any] = field(default_factory=dict)


class VideoFile:
    """
    Represents a single video file or recording segment.

    Attributes:
        idx (VideoFileId):
            The unique identifier for the video file.
        source_id (RecordingSourceId):
            The identifier of the recording source (camera/channel) that produced
            this video file.
        started_at (datetime):
            The timestamp indicating when the recording began.
        extra (VideoFileExtra):
            Optional technical details and metadata about the video file.
            Defaults to an empty VideoFileExtra instance.
    """

    def __init__(
        self,
        idx: VideoFileId,
        source_id: "RecordingSourceId",
        started_at: datetime,
        extra: VideoFileExtra | None = None,
    ) -> None:
        """
        Initializes a VideoFile instance.

        Args:
            idx: The unique identifier for the video file.
            source_id: The identifier of the source camera/channel.
            started_at: The start time of the recording.
            extra: Optional technical details. If None, defaults to a
                new, empty VideoFileExtra object.
        """
        self.idx: VideoFileId = idx
        self.source_id: RecordingSourceId = source_id
        self.started_at: datetime = started_at
        self.extra: VideoFileExtra = extra or VideoFileExtra()
