from abc import ABC, abstractmethod

from domain.entity.video_file import VideoFile, VideoFileId
from domain.entity.video_source import RecordingSourceId


class VideoFileRepository(ABC):
    """
    Abstract repository for managing video file entities.

    This interface defines the persistence operations for VideoFile entities,
    providing methods to store, retrieve, and filter video records within
    the domain.
    """


    @abstractmethod
    def save(self, video: "VideoFile") -> None:
        """
        Saves or updates a video file entity in the storage.

        Args:
            video (VideoFile): The video file entity to be persisted.

        Raises:
            NotImplementedError: If the concrete implementation is missing.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_idx(self, idx: "VideoFileId") -> "VideoFile | None":
        """
        Retrieves a video file by its unique domain identifier.

        Args:
            idx (VideoFileId): The unique identifier of the video file.

        Returns:
            Optional[VideoFile]: The video file entity if found, otherwise None.

        Raises:
            NotImplementedError: If the concrete implementation is missing.
        """
        raise NotImplementedError

    @abstractmethod
    def list_by_source_idx(self, source_idx: "RecordingSourceId") -> list["VideoFile"]:
        """
        Retrieves all video files associated with a specific recording source.

        Args:
            source_idx (RecordingSourceId): The unique identifier of the
                originating recording source.

        Returns:
            list[VideoFile]: A list of video file entities linked to
                the given source.

        Raises:
            NotImplementedError: If the concrete implementation is missing.
        """
        raise NotImplementedError
