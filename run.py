"""
run.py - executable entry point responsible for running the GeoWatch application.
An entry point guard is utulized so that when the guard begins the event loop, only run.py is executed directly.
Tests can import application modules without opening a window.
"""
from geowatch.app import GeoWatchApp  # Absolute import! No leading dots.

def main() -> None:
    app = GeoWatchApp()
    app.mainloop()

if __name__ == "__main__":
    main()
