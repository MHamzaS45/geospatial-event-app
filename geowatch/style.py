"""
A seperate file for marking the query results. The colorama library is not used as the colors are intended to be used 
in a GUI context, not a terminal. The colors are defined in hexadecimal format, which is compatible with most GUI frameworks.

Before the queries are marked, the overlaps are checked first, then the radius and bounds are checked. The colors are assigned 
based on the following rules:

- If the event is in both the radius and bounds, it is marked with purple.
- If the event is only in the radius, it is marked with red.
- If the event is only in the bounds, it is marked with orange.
- If the event is in neither/unmatched, it is marked with gray.
"""


from .models import GeoEvent


# Give overlaps priority before individual query categories.
def marker_color(
    event: GeoEvent, radius_names: set[str], bounds_names: set[str]
) -> str:
    in_radius = event.name in radius_names
    in_bounds = event.name in bounds_names
    
    if in_radius and in_bounds:
        return "#7c3aed" 
    if in_radius:
        return "#dc2626"
    if in_bounds:
        return "#ea580c"  
        
    return "#64748b"      
