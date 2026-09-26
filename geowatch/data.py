""" 
 data.py involves the creation of sample records of events to be tested in the geowatch system. The records are generated
 based on a set of parameters and can be used to simulate various scenarios for testing purposes.

 The records will consist of Finnish weather disturbances, which will be used to test the system's ability to
   handle and process event data. The sample records will be generated using a combination of randomization and 
   predefined parameters to ensure a diverse set of events.

   Exception statement added to account for coordinate failures, which will be raised when the
   coordinates for both latitude and longitude are out of bounds. 
"""

from .models import GeoEvent, InvalidCoordinateError

RAW_EVENTS = [
       ("Lapland", "Severe Frost", 5, 69.0, 21.0),
        ("Helsinki", "Intensive Sea Gales", 2, 60.1699, 24.9384),
        ("Tampere", "Thunderstorm", 3, 61.4997, 23.7725),
        ("Oulu", "Snowstorm", 4, 65.0121, 25.4651),
        ("Bad Coordinate", "UNKNOWN", 1, 60.4518, 22.2666),
    ]

def load_events() -> tuple[list[GeoEvent], list[str]]:
    events: list[GeoEvent] = []
    errors: list[str] = []
    for values in RAW_EVENTS:
        try:
            event = GeoEvent(*values)
            events.append(event)
        except InvalidCoordinateError as e:
            errors.append(f"Error creating event {values}: {e}")
    return events, errors