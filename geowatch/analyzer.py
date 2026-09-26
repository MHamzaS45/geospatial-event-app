"""
Calculation and visualisation of spatial queries is implemented in this module. The main class is the Analyzer, which
is used to perform spatial queries on a given dataset and visualize the results. The module also includes 
utility functions for data preprocessing and visualization.

Spatial queries are performed using the Shapely library, which provides a set of geometric objects and operations
for spatial analysis. The Analyzer class takes a list of GeoEvent objects as input and provides methods for performing spatial queries such as point-in-polygon tests and distance calculations.

For calculating the spherical distance, the Haversine formula is used to estimate the great-circle distance
between two coordinates on a sphere. GeoWatch uses Earth's mean radius of 6371.0 kilometers. Events are filtered by radius and 
bounding box, followed by a visualisation of overlapping query results with marker colors
  - Radius filtering works via the guard clause, which raises a ValueError if the radius is negative. 
  - Bounding box filtering works via the guard clause, which raises a ValueError if the minimum bounds exceed the maximum bounds.

Both filters scan n events, so each query is O(n). Bounding comparisons are cheaper per event, while Haversine distance better represents a circular search area on Earth's surface.
In a larger system, a spatial index can reduce the candidate set before exact distance checks.

"""

from math import asin, cos, radians, sin, sqrt
from .models import GeoEvent

EARTH_RADIUS_KM = 6371.0


"""
For calculations to remain stable, the radians convert degree inputs into the units expected by Python's trigonometric functions.
The Haversine terms determine the central angle between both points & the clamp protects asin() from tiny floating-point drift outside 0.0 through 1.0.

"""

#  Reference code:
#  GeekForGeeks, 2022, Haversine formula to find distance between two points on a sphere  
#  URL at: https://www.geeksforgeeks.org/dsa/haversine-formula-to-find-distance-between-two-points-on-a-sphere/

def distance_km(first: GeoEvent, second: GeoEvent) -> float:
    first_lat = radians(first.latitude)
    second_lat = radians(second.latitude)
    latitude_delta = second_lat - first_lat
    longitude_delta = radians(second.longitude - first.longitude)

    latitude_term = sin(latitude_delta / 2.0) ** 2
    longitude_term = sin(longitude_delta / 2.0) ** 2
    haversine = latitude_term + cos(first_lat) * cos(second_lat) * longitude_term
    stable_value = min(1.0, max(0.0, haversine))
    central_angle = 2.0 * asin(sqrt(stable_value))
    return EARTH_RADIUS_KM * central_angle


def within_radius(events: list[GeoEvent], center: GeoEvent, radius_km: float) -> list[GeoEvent]:
    if radius_km < 0.0:
        raise ValueError("Radius must be non-negative.")
    return [event for event in events if distance_km(center, event) <= radius_km]


def within_bounds(
    events: list[GeoEvent],
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
) -> list[GeoEvent]:
    if min_lat > max_lat or min_lon > max_lon:
        raise ValueError("Minimum bounds must not exceed maximum bounds.")
    return [
        event
        for event in events
        if min_lat <= event.latitude <= max_lat
        and min_lon <= event.longitude <= max_lon
    ]


"""
In times of major crisis all over the region, the command center may need to prioritize some incidents. 
The questions becomes which event should the command center inspect first when several valid events surround it? 

To answer this question, the nearest_events function ranks events by distance from the command center and returns 
a 2 of the closest events. The limit is guarded to be at least 1, otherwise a ValueError is raised.
Sorting by a computed key keeps distance logic in one place. The returned list is a new object, so ranking 
does not change the feed's original order. A full sort costs O(n log n). A top-k heap can reduce this to O(n log k)
 when the event collection is large and k is small.
"""

def nearest_events(
    events: list[GeoEvent], center: GeoEvent, limit: int
) -> list[GeoEvent]:
    if limit < 1:
        raise ValueError("Limit must be at least 1.")
    ranked = sorted(events, key=lambda event: distance_km(center, event))
    return ranked[:limit]