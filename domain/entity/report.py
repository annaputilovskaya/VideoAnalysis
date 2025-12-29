from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from domain.entity.video_source import RecordingSourceId
from domain.entity.video_file import VideoFileId
from domain.entity.detected_object import ObjectId


@dataclass(frozen=True)
class ReportId:
    """
    Unique identifier for a report.

    Attributes:
        value (UUID): The underlying UUID value of the report identifier.
    """
    value: UUID

    @staticmethod
    def new() -> "ReportId":
        """
        Generates a new unique ReportId using UUID4.

        Returns:
            ReportId: A new instance with a random UUID.
        """
        return ReportId(uuid4())

    def __str__(self) -> str:
        """
        Returns the string representation of the report ID.

        Returns:
            str: The UUID as a string.
        """
        return str(self.value)


@dataclass(frozen=True)
class ReportType:
    """
    Represents the classification of the report.

    Defines the purpose of the report, such as 'people_count' or
    'gender_distribution'.

    Attributes:
        value (str): The string constant identifying the report type.
    """
    value: str


@dataclass(frozen=True)
class TimeRange:
    """
    A time interval for which the report is generated.

    Attributes:
        start (datetime): The beginning of the reporting period.
        end (datetime): The end of the reporting period.
    """
    start: datetime
    end: datetime


@dataclass
class ReportData:
    """
    Aggregated report data container.

    Currently, stores data in a flexible dictionary format to allow for
    evolution. Specific metrics can be extracted into structured fields
    once the domain logic stabilizes.

    Attributes:
        meta (dict[str, Any]): A dictionary containing the aggregated metrics
            and results. Defaults to an empty dictionary.
    """
    meta: dict[str, Any] = field(default_factory=dict)



class Report:
    """
    An analytical report generated for the customer.

    This entity encapsulates the final results of data processing,
    linking aggregated metrics with their time range, source recordings,
    and identified objects.

    Attributes:
        idx (ReportId): Unique identifier of the report.
        report_type (ReportType): Category of the analysis performed.
        time_range (TimeRange): The specific period covered by the report.
        data (ReportData): The actual calculated results and metadata.
        source_idx_list (list[RecordingSourceId]): List of IDs for the
            recording sources (cameras/streams) used.
        video_idx_list (list[VideoFileId]): List of IDs for the specific
            video files analyzed.
        object_idx_list (list[ObjectId]): List of unique object identifiers
            included in this report.
    """

    def __init__(
        self,
        idx: ReportId,
        report_type: ReportType,
        time_range: TimeRange,
        data: ReportData,
        source_idx_list: list["RecordingSourceId"],
        video_idx_list: list["VideoFileId"],
        object_idx_list: list["ObjectId"],
    ) -> None:
        """
        Initializes a Report instance.

        Args:
            idx (ReportId): Unique identifier for the report.
            report_type (ReportType): Type of the report.
            time_range (TimeRange): Time interval for the data.
            data (ReportData): Aggregated result data.
            source_idx_list (list[RecordingSourceId]): Collection of source
                recording identifiers.
            video_idx_list (list[VideoFileId]): Collection of video file
                identifiers.
            object_idx_list (list[ObjectId]): Collection of detected object
                identifiers.
        """
        self.idx = idx
        self.report_type = report_type
        self.time_range = time_range
        self.data = data

        self.source_idx_list = list(source_idx_list)
        self.video_idx_list = list(video_idx_list)
        self.object_idx_list = list(object_idx_list)
