"""
The module serves to project coordinates onto the pixels of the screen. 

Projection works via: 
 - The fractions normalize each coordinate into its position across the geographic range.
 - The usable dimensions preserve a 40 pixel border around the plot.
 - The latitude expression starts from MAX_LAT to match the screen's downward y-axis.

"""



MIN_LAT, MAX_LAT = 59.0, 70.0
MIN_LON, MAX_LON = 20.0, 26.0
PADDING = 40

# Scale geographic coordinates into the canvas drawing area.
def project(longitude: float, latitude: float) -> tuple[int, int]:
    usable_width = 620 - (2 * PADDING)
    usable_height = 500 - (2 * PADDING)
    x_fraction = (longitude - MIN_LON) / (MAX_LON - MIN_LON)
    y_fraction = (MAX_LAT - latitude) / (MAX_LAT - MIN_LAT)
    x = PADDING + round(x_fraction * usable_width)
    y = PADDING + round(y_fraction * usable_height)
    return x, y

