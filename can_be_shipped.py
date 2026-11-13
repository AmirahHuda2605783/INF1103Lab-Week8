from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface for anything that needs physical shipping."""

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass