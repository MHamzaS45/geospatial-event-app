"""
These tests cover a mathematical identity, an inclusion decision, boundary semantics and  ranking behaviour. 
The tests are written in a way that they can be run independently. Together they prove more than a single 
happy-path example.

"""

import pytest
from geowatch.analyzer import distance_km, nearest_events, within_bounds, within_radius
from geowatch.models import GeoEvent



CENTER = GeoEvent("Center", "TEST", 1, 0.0, 0.0)
NEAR = GeoEvent("Near", "TEST", 1, 0.0, 0.1)
FAR = GeoEvent("Far", "TEST", 1, 0.0, 2.0)


# A point has no distance from itself.
def test_distance_to_same_point_is_zero() -> None:
    assert distance_km(CENTER, CENTER) == pytest.approx(0.0)


# The radius includes the near point and excludes the far point.
def test_radius_query_filters_by_distance() -> None:
    assert within_radius([NEAR, FAR], CENTER, 20.0) == [NEAR]


# Inclusive bounds retain a point on the maximum edge.
def test_bounds_query_includes_boundary() -> None:
    matches = within_bounds([NEAR, FAR], -1.0, 1.0, -1.0, 0.1)
    assert matches == [NEAR]

# Prove ranking ignores input order and respects the requested limit.
def test_nearest_events_returns_top_two() -> None:
    middle = GeoEvent("Middle", "TEST", 1, 0.0, 0.5)
    events = [FAR, NEAR, middle]
    nearest = nearest_events(events, CENTER, 2)
    assert nearest == [NEAR, middle]
    assert events == [FAR, NEAR, middle]