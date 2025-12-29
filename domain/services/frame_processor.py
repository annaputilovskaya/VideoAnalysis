from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entity.frame import Frame
from domain.entity.detected_object import ObjectClass, ObjectAttributes, Coordinate


@dataclass(frozen=True)
class RawDetection:
    """
    Represents a raw detection result from neural networks for a single object.

    At the frame processing level, this structure captures the essential
    output of the inference: the object's classification, its detected
    attributes, and its spatial location within the frame.

    Attributes:
        object_class (ObjectClass): The category of the detected object.
        attributes (ObjectAttributes): Set of traits identified for the object.
        coordinate (Coordinate): The bounding box of the object in the frame.
    """
    object_class: "ObjectClass"
    attributes: "ObjectAttributes"
    coordinate: "Coordinate"


class FrameProcessor(ABC):
    """
    Abstract service for neural network-based frame processing.

    This interface decouples the domain logic from the specifics of
    computer vision models. It abstracts away the number of models,
    their execution order, and the underlying hardware (CPU/GPU/TPU)
    used for inference.
    """

    @abstractmethod
    def process_frame(self, frame: "Frame") -> list[RawDetection]:
        """
        Analyzes a frame and returns a list of detected objects.

        Runs inference on the provided frame to identify entities and
        extract their classes, attributes, and coordinates.

        Args:
            frame (Frame): The frame entity to be processed.

        Returns:
            list[RawDetection]: A list of objects found in the frame.

        Raises:
            NotImplementedError: Must be implemented by an infrastructure-level
                adapter.
        """
        raise NotImplementedError
