"""
Application Module

 -The constructor creates the canvas and a status panel.
 -The drawing loop projects every record before checking whether its pixel lies inside the regional box.
 -The status text exposes the difference between accepted input and visible output.
 
 The event feed is presented as a desktop operations view. The renderer also now receives validated events,
 with the status panel keeping rejected input observable. The canvas is drawn with a border to 
 indicate the geographic region of interest, and events are represented as blue dots with their names displayed next to them. 
 The status panel provides a summary of the total number of events, the number of visible events, and the number of hidden events.
"""

"""
For this project, the command center chosen to use as a reference for the other locations is Jyväskylä 
(Latitude 62.2426, Longitude 25.7473), which sits right in the middle of the other locations:

"""

import tkinter as tk
from .data import load_events
from .projection import project 
from .models import GeoEvent
from .style import marker_color
from .analyzer import nearest_events, within_bounds, within_radius
from .highlights import draw_nearest_rings


# GUI Class for the GeoWatch application
class GeoWatchApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GeoWatch Operations Analysis View")
        self.canvas = tk.Canvas(self, width=620, height = 500, bg="beige")
        self.canvas.pack(side="left", padx=20, pady=20)
        self.status = tk.Label(self, text="", anchor="w", justify="left")
        self.status.pack(side="right", padx=20, pady=20, fill="both", expand=True)
        self.__draw_queries()

    def __draw_queries(self) -> None:
        events, errors = load_events()
        center = GeoEvent("Command Center", "CENTER", 5, 62.2426, 25.7473)
        radius = within_radius(events, center, 250.0)
        bounds = within_bounds(events, 60.0, 63.0, 22.0, 26.0)
        nearest = nearest_events(events, center, 2)
        radius_names = {event.name for event in radius}
        bounds_names = {event.name for event in bounds}
        self.canvas.create_rectangle(40, 40, 580, 460, outline="#64748b", width=1)

        for event in events:
            x, y = project(event.longitude, event.latitude)
            color = marker_color(event, radius_names, bounds_names)
            self.canvas.create_oval(x - 7, y - 7, x + 7, y + 7, fill=color)
            self.canvas.create_text(x + 9, y, text=event.name, anchor="w")
            draw_nearest_rings(self.canvas, nearest)
        
        cx, cy = project(center.longitude, center.latitude)
        self.canvas.create_rectangle(cx - 7, cy - 7, cx + 7, cy + 7, fill="#2563eb")
        self.status.config(text=f"Radius matches: {len(radius)} \nBounds matches: {len(bounds)} \nRejected: {len(errors)}")
                

