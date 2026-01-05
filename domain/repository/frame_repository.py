from abc import ABC, abstractmethod
from datetime import datetime

from domain.entity.frame import Frame
from domain.entity.video_file import VideoFileId


class FrameRepository(ABC):
    """
    Abstract repository for managing frame entities.

    This repository handles the persistence of analyzed frames, which serve as
    visual evidence (provenance) of the system's operations. It provides
    capabilities to retrieve frames based on video source and temporal data.
    """

    @abstractmethod
    def save(self, frame: "Frame") -> None:
        """
        Saves or updates a frame entity in the persistent storage.

        Args:
            frame (Frame): The frame entity to be stored.

        Raises:
            NotImplementedError: If the concrete implementation is missing.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_video_and_time(
        self,
        video_idx: "VideoFileId",
        captured_at: datetime,
    ) -> "Frame | None":
        """
        Retrieves a specific frame using its composite unique identifier.

        Args:
            video_idx (VideoFileId): Unique identifier of the source video.
            captured_at (datetime): The exact timestamp when the frame was captured.

        Returns:
            Optional[Frame]: The matching frame entity, or None if no frame
                is found for the given video and timestamp.

        Raises:
            NotImplementedError: If the concrete implementation is missing.
        """
        raise NotImplementedError

    @abstractmethod
    def list_by_video_idx(
        self,
        video_idx: "VideoFileId",
        *,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> list["Frame"]:
        """
        Retrieves a collection of frames associated with a specific video.

        Allows filtering the resulting frames within a specific time range.

        Args:
            video_idx (VideoFileId): Unique identifier of the source video.
            start_time (Optional[datetime]): The beginning of the time range
                filter. Defaults to None (no lower bound).
            end_time (Optional[datetime]): The end of the time range
                filter. Defaults to None (no upper bound).

        Returns:
            list[Frame]: A list of frame entities matching the criteria.

        Raises:
            NotImplementedError: If the concrete implementation is missing.
        """
        raise NotImplementedError
