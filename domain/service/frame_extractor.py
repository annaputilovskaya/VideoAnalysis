from abc import ABC, abstractmethod
from typing import Iterable

from domain.entity.video_file import VideoFileId
from domain.entity.frame import Frame


class FrameExtractor(ABC):
    """
    Abstract service for extracting frames from video files.

    At the domain level, this service defines the contract for converting
    a video recording into a sequence of individual frames required
    for further processing and analytics.
    """

    @abstractmethod
    def extract_frames(self, video_idx: "VideoFileId") -> Iterable["Frame"]:
        """
        Extracts frames for the specified video record.

        The concrete implementation determines the technical details, such as
        how to access the source file (local storage, object storage, etc.)
        and the specific parameters for the extraction process (e.g., frequency,
        resolution, or codecs).

        Args:
            video_idx (VideoFileId): The unique identifier of the video
                file to be processed.

        Returns:
            Iterable[Frame]: A sequence of Frame entities extracted
                from the video.

        Raises:
            NotImplementedError: If the concrete subclass does not
                implement this method.
        """
        raise NotImplementedError
