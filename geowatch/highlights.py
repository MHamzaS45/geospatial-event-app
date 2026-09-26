#################
# highlights.py
##################
"""
The module highlights the two nearest markers in the desktop app via a gold-ring renderer, that adds a second visual dimension
to the markings.  The nearest events are determined by the distance_km function in the analyzer module. The highlight function 
is called from the GeoWatchApp class in app.py, which is responsible for managing the GUI and user interactions.
"""

import tkinter as tk
from .models import GeoEvent
from .projection import project


def draw_nearest_rings(canvas: tk.Canvas, events: list[GeoEvent]) -> None:
    for event in events:
        x, y = project(event.longitude, event.latitude)
        canvas.create_oval(
            x - 11, y - 11, x + 11, y + 11, outline="#d4b13c", width=3
        )

