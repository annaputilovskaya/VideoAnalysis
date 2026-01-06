from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from domain.entity.record_source import RecordingSourceId


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

    def mark_ended(self, ended_at: datetime | None = None) -> None:
        """
        Marks the video recording as finished and calculates its duration.

        Args:
            ended_at (datetime | None): The timestamp when the recording ended.
                Defaults to the current UTC time if not provided.

        Raises:
            ValueError: If the end timestamp is earlier than the start timestamp.
        """
        new_ended_at = ended_at or datetime.utcnow()

        if new_ended_at < self.started_at:
            raise ValueError("Ended_at cannot be earlier than started_at")

        if self.extra.ended_at is not None and new_ended_at <= self.extra.ended_at:
            return

        self.extra.ended_at = new_ended_at
        self.extra.duration_seconds = (new_ended_at - self.started_at).total_seconds()

    def update_duration(self, duration_seconds: float) -> None:
        """
        Updates the duration of the video recording.

        Args:
            duration_seconds (float): The total duration in seconds.

        Raises:
            ValueError: If duration_seconds is negative.
        """
        if duration_seconds < 0:
            raise ValueError("Duration_seconds cannot be negative")

        self.extra.duration_seconds = duration_seconds

    def update_technical_info(
        self,
        *,
        codec: str | None = None,
        frame_width: int | None = None,
        frame_height: int | None = None,
        meta: dict[str, Any] | None = None,
    ) -> None:
        """
        Updates the technical parameters of the video recording.

        Args:
            codec (str | None): The video codec used (e.g., 'h264').
            frame_width (int | None): The width of the video frame in pixels.
            frame_height (int | None): The height of the video frame in pixels.
            meta (dict[str, Any] | None): Additional metadata to merge into the
                existing metadata dictionary.

        Raises:
            ValueError: If frame_width or frame_height is not positive.
        """
        if frame_width is not None and frame_width <= 0:
            raise ValueError("Frame_width must be positive")

        if frame_height is not None and frame_height <= 0:
            raise ValueError("Frame_height must be positive")

        if codec is not None:
            self.extra.codec = codec

        if frame_width is not None:
            self.extra.frame_width = frame_width

        if frame_height is not None:
            self.extra.frame_height = frame_height

        if meta:
            self.extra.meta.update(meta)

    def update_extra(self, extra: VideoFileExtra) -> None:
        """
        Completely replaces the extra metadata object.

        Args:
            extra (VideoFileExtra): The new metadata object to associate with the video.
        """
        self.extra = extra
