from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from domain.entity.detected_object import DetectedObject, ObjectId
from domain.entity.video_file import VideoFileId
from domain.entity.video_source import RecordingSourceId


@dataclass
class ObjectAnalyticsResult:
    """
    The outcome of analyzing unique detected objects.

    This container consolidates all the information necessary for report
    generation, including aggregated statistical data and references to
    the supporting evidence (sources, videos, and objects).

    Attributes:
        meta (dict[str, Any]): A dictionary of aggregated metrics and
            statistical insights. Defaults to an empty dictionary.
        source_idx_list (list[RecordingSourceId]): A list of source
            recording identifiers used for the analysis.
        video_idx_list (list[VideoFileId]): A list of video file
            identifiers processed during analysis.
        object_idx_list (list[ObjectId]): A list of unique object
            identifiers included in the result.
    """
    meta: dict[str, Any] = field(default_factory=dict)
    source_idx_list: list["RecordingSourceId"] = field(default_factory=list)
    video_idx_list: list["VideoFileId"] = field(default_factory=list)
    object_idx_list: list["ObjectId"] = field(default_factory=list)


class ObjectAnalyzer(ABC):
    """
    Abstract service for analyzing identified and classified objects.

    This service processes a collection of unique DetectedObject entities to
    extract meaningful patterns and metrics. It acts as a bridge between raw
    object data and high-level reporting logic.
    """

    @abstractmethod
    def analyze_objects(
        self,
        objects: list["DetectedObject"],
    ) -> ObjectAnalyticsResult:
        """
        Analyzes a set of unique objects to produce aggregated results.

        Processes the historical data and attributes of the provided objects
        to calculate metrics suitable for report construction.

        Args:
            objects (list[DetectedObject]): A collection of unique objects
                tracked across video streams.

        Returns:
            ObjectAnalyticsResult: An object containing aggregated insights
                and references to the source data.

        Raises:
            NotImplementedError: If the concrete analysis logic is not
                implemented.
        """
        raise NotImplementedError
