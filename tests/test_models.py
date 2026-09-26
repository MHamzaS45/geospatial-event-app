"""
test_models.py prooves the coordinate contract. The first 2 coordinate tests (latitude and longitude) verify the 
exception type and useful message category and the boundary test protects inclusive comparisons from later regression.

Each test owns one behaviour. The tests are written in a  way that they can be run independently
 and do not rely on any external dependencies or state.

"""


from math import inf 

import pytest
from geowatch.models import GeoEvent, InvalidCoordinateError

def test_rejects_invalid_latitude() -> None:
    with pytest.raises(InvalidCoordinateError, match="Latitude"):
        GeoEvent("Bad", "TEST", 1, 95.0, 0.0)
    
def test_rejects_invalid_longitude() -> None:
    with pytest.raises(InvalidCoordinateError, match="Longitude"):
        GeoEvent("Bad", "TEST", 1, 0.0, inf)

def test_accepts_global_boundaries() -> None:
    event = GeoEvent("Boundary", "TEST", 1, -90.0, -180.0)
    assert event.latitude == -90.0
    assert event.longitude == -180.0
   