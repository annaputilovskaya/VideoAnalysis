from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import BinaryIO

from domain.entity.video_file import VideoFileId


@dataclass(frozen=True)
class FileLocation:
    """
    Represents an abstract location of a file.

    This can be a local file path, an object storage key (e.g., S3),
    a URL, or any other identifier determined by the infrastructure layer.

    Attributes:
        value (str): The string representation of the file location.
    """
    value: str


@dataclass(frozen=True)
class FileSaveResult:
    """
    The result of a file persistence operation.

    Encapsulates whether the operation was successful and provides
    either the resulting location or an error description.

    Attributes:
        success (bool): Indicates if the file was saved successfully.
        location (Optional[FileLocation]): The location of the saved file
            if successful. Defaults to None.
        error_message (Optional[str]): A descriptive error message
            if the operation failed. Defaults to None.
    """
    success: bool
    location: FileLocation | None = None
    error_message: str | None = None


class FileStorage(ABC):
    """
    Abstract interface for file storage operations.

    This service defines the domain's requirements for persisting files.
    Implementation details such as streaming, buffering, retries, and
    specific storage providers are handled at the infrastructure level.
    """

    @abstractmethod
    def save_video_content(
        self,
        video_idx: "VideoFileId",
        content: BinaryIO,
    ) -> FileSaveResult:
        """
        Persists binary video content associated with a domain entity.

        Links the raw binary data to a specific VideoFile entity via its
        identifier.

        Args:
            video_idx (VideoFileId): The unique identifier of the video
                file entity.
            content (BinaryIO): An abstract binary stream (e.g., an open
                file, network stream, or buffer).

        Returns:
            FileSaveResult: An object containing the status and
                location of the saved file.
        """
        raise NotImplementedError
