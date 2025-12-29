from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entity.frame import Frame
from domain.entity.detected_object import ObjectId, FrameRef
from domain.service.frame_processor import RawDetection

@dataclass(frozen=True)
class ObjectClassificationDecision:
    """
    The result of classifying and matching a raw detection.

    Determines whether a detected entity corresponds to an existing
    object or represents a new discovery. It links the raw inference
    data with the domain's tracking context.

    Attributes:
        existing_object_idx (Optional[ObjectId]): The identifier of an
            already known object. If None, the detection is treated as new.
        frame_ref (FrameRef): Reference to the specific frame and location
            where the detection occurred.
        raw_detection (RawDetection): The original inference data (class,
            attributes, coordinates).
    """
    existing_object_idx: "ObjectId | None"
    frame_ref: "FrameRef"
    raw_detection: "RawDetection"

    @property
    def is_new(self) -> bool:
        """
        Indicates whether a new domain object should be created.

        Returns:
            bool: True if the detection does not match any existing object.
        """
        return self.existing_object_idx is None


class ObjectClassifier(ABC):
    """
    Abstract service for object classification and matching across frames.

    This service is responsible for the logic of object re-identification
    and tracking. It abstracts away the technical implementation, such as
    Euclidean distance tracking, Re-ID neural networks, or motion
    prediction models.
    """

    @abstractmethod
    def classify_objects(
        self,
        frame: "Frame",
        detections: list["RawDetection"],
    ) -> list[ObjectClassificationDecision]:
        """
        Maps a set of raw detections to existing or new domain objects.

        Analyzes detections within the context of the current frame to
        determine object continuity.

        Args:
            frame (Frame): The current frame being analyzed.
            detections (list[RawDetection]): A list of raw inference
                results from the frame processor.

        Returns:
            list[ObjectClassificationDecision]: A list of decisions mapping
                each detection to an identity status.

        Raises:
            NotImplementedError: If the concrete implementation is missing.
        """
        raise NotImplementedError
