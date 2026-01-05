from abc import ABC, abstractmethod
from datetime import datetime

from domain.entity.report import Report, ReportId, ReportType


class ReportRepository(ABC):
    """
    Abstract repository for managing Report entities.
    """

    @abstractmethod
    def save(self, report: "Report") -> None:
        """
        Saves or updates a report in the repository.

        Args:
            report: The Report instance to persist.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_idx(self, idx: "ReportId") -> "Report | None":
        """
        Retrieves a report by its domain identifier.

        Args:
            idx: The unique domain identifier of the report.

        Returns:
            The found Report instance, or None if no report exists with the given ID.
        """
        raise NotImplementedError

    @abstractmethod
    def list_by_type(
        self,
        report_type: "ReportType",
        *,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list["Report"]:
        """
        Retrieves reports of a specific type within a time range.

        The time range defines the period for which the reports were generated.
        The specific implementation determines how start_time and end_time
        relate to the report's internal TimeRange field.

        Args:
            report_type: The category of reports to filter by.
            start_time: The beginning of the period of interest.
            end_time: The end of the period of interest.
            limit: Maximum number of reports to return.
            offset: Number of reports to skip for pagination.

        Returns:
            A list of Report instances matching the criteria.
        """
        raise NotImplementedError

    @abstractmethod
    def list_all(
        self,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list["Report"]:
        """
        Retrieves all reports with optional pagination.

        Args:
            limit: Maximum number of reports to return.
            offset: Number of reports to skip for pagination.

        Returns:
            A list of all stored Report instances.
        """
        raise NotImplementedError
