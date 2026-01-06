from dataclasses import dataclass
from datetime import datetime
from typing import Any

from domain.entity.video_file import VideoFileId

@dataclass(frozen=True)
class FrameData:
    """
    The raw data of a single frame.

    This class abstracts the underlying implementation of frame data.

    Attributes:
        value (Any):
            The encapsulated raw data of the video frame. The type can vary
            based on the specific implementation requirements (e.g., bytes, ndarray).
    """
    value: Any


class Frame:
    """
    Represents a single frame extracted from a video recording.

    Attributes:
        video_idx (VideoFileId):
            The unique identifier of the video file to which this frame belongs.
        captured_at (datetime):
            The precise timestamp indicating when the frame was captured/recorded.
        data (FrameData):
            The value object containing the raw data of the frame.
    """

    def __init__(
        self,
        video_idx: "VideoFileId",
        captured_at: datetime,
        data: FrameData,
    ) -> None:
        """
        Initializes a Frame instance.

        Args:
            video_idx: The ID of the parent video file.
            captured_at: The timestamp when the frame was captured.
            data: The raw data payload of the frame.
        """
        self.video_idx = video_idx
        self.captured_at = captured_at
        self.data = data

    def update_data(self, data: FrameData) -> None:
        """
        Updates the frame's raw data.

        This method centralizes all changes to the underlying frame data,
        accounting for scenarios such as:
            - Re-encoding the frame.
            - Applying anonymization or masking.
            - Downscaling or changing compression (e.g., to JPEG).

        Args:
            data (FrameData): The new frame data object to replace the current one.
        """
        self.data = data

    def is_in_time_range(self, start: datetime, end: datetime) -> bool:
        """
        Checks if the frame's capture time falls within the interval.

        Args:
            start (datetime): The beginning of the interval (inclusive).
            end (datetime): The end of the interval (exclusive).

        Returns:
            bool: True if the frame was captured within the specified interval,
                False otherwise.
        """
        return start <= self.captured_at < end
