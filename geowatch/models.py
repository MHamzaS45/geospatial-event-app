""" 
Modelling the flawed event feed via a dataclass. This is a temporary solution until we have a proper database and ORM in place.
The dataclass generates the initializer and comparison methods..

The first version has no coordinate guard, which will create a flaw to be exposed. Thereafter, we validate the model so that it
rejects impossible coordinates. The validation is done via a __post_init__ method, which raises a ValueError 
if the coordinates for both latitude and longitude are out of bounds.

"""

from dataclasses import dataclass
from math import isfinite

class InvalidCoordinateError(ValueError):
    """Raise custom exception for invalid coordinates."""

@dataclass(frozen=True)
class GeoEvent:
    name: str
    category: str
    severity: int
    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        if not isfinite(self.latitude) or not -90.0 <= self.latitude <= 90.0:
            raise InvalidCoordinateError(
                "Latitude must be finite and between -90 and 90."
            )
        if not isfinite(self.longitude) or not -180.0 <= self.longitude <= 180.0:
            raise InvalidCoordinateError(
                "Longitude must be finite and between -180 and 180."
            )