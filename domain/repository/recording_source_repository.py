from abc import ABC, abstractmethod

from domain.entity.video_source import RecordingSource, RecordingSourceId


class RecordingSourceRepository(ABC):
    """
    Abstract repository for managing recording sources.

    This interface defines the persistence contract for recording sources,
    decoupling the domain logic from specific storage implementations such as
    relational databases (Postgres), NoSQL, local files, or in-memory storage.
    """

    @abstractmethod
    def save(self, source: "RecordingSource") -> None:
        """
        Saves or updates a recording source in the persistent storage.

        Args:
            source (RecordingSource): The recording source entity to be persisted.

        Raises:
            NotImplementedError: If the concrete implementation is missing.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_idx(self, idx: "RecordingSourceId") -> "RecordingSource | None":
        """
        Retrieves a recording source by its unique domain identifier.

        Args:
            idx (RecordingSourceId): The unique identifier of the recording source.

        Returns:
            Optional[RecordingSource]: The found recording source entity,
                or None if no source matches the given identifier.

        Raises:
            NotImplementedError: If the concrete implementation is missing.
        """
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> list["RecordingSource"]:
        """
        Returns a list of all known recording sources.

        Returns:
            list[RecordingSource]: A collection of all recording source entities
                available in the storage.

        Raises:
            NotImplementedError: If the concrete implementation is missing.
        """
        raise NotImplementedError
