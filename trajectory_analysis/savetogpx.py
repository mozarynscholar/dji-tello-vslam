import math
import gpxpy
import gpxpy.gpx
import pyproj

def read_xy_file(filename):
    xy_coords = []
    with open(filename, 'r') as file:
        for line in file:
            values = [float(x) for i, x in enumerate(line.strip().split()) if i == 1 or i == 3]
            xy_coords.append(values)
    return xy_coords


def convert_xy_to_gps(xy_coords):
    # Define the projection parameters (Lambert Conformal Conic)
    proj_params = {
        'proj': 'lcc',
        'lat_1': 52.1,
        'lat_2': 52.11,
        'lat_0': 52.10111378,
        'lon_0': 21.05131274,
        'x_0': 0,
        'y_0': 0,
        'ellps': 'WGS84'
    }

    # Define the Lambert Conformal Conic projection
    lcc = pyproj.Proj(proj_params)

    # Convert each Cartesian coordinate to GPS
    gps_coords = []
    for x, y in xy_coords:
        lon, lat = pyproj.transform(lcc, pyproj.Proj(init='EPSG:4326'), x, y)
        gps_coords.append((lon, lat))

    # Return GPS coordinates
    return gps_coords

def save_to_gpx(gps_coords, output_filename):
    gpx = gpxpy.gpx.GPX()

    # Create GPX track
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    # Create GPX segment
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    # Add points to the segment
    for lon, lat in gps_coords:
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(latitude=lat, longitude=lon))

    # Save to GPX file
    with open(output_filename, 'w') as f:
        f.write(gpx.to_xml())

# Input file
input_filename = 'ktraj.tum'

# Read XY coordinates from file
xy_coords = read_xy_file(input_filename)

# Starting GPS coordinates (for mapping XY coordinates)
start_lon = 21.05131274  # Provide your start longitude
start_lat = 52.10111378  # Provide your start latitude

# Convert XY coordinates to GPS coordinates
gps_coords = convert_xy_to_gps(xy_coords)

# Output GPX file
output_filename = 'lotdronamapa.gpx'

# Save GPS coordinates to GPX file
save_to_gpx(gps_coords, output_filename)

print("Data saved to", output_filename)
