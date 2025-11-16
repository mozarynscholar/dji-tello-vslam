import xml.etree.ElementTree as ET
import pyproj


def convert_gps_to_xy(gps_coords):
    # Define Lambert Conformal Conic projection parameters for Poland
    proj_params = {
        'proj': 'lcc',          # Lambert Conformal Conic Projection
        'ellps': 'WGS84',       # Ellipsoid
        'lat_1': 52.1,            # First standard parallel
        'lat_2': 52.11,            # Second standard parallel
        'lat_0': 52.1011912,            # Latitude of origin
        'lon_0': 21.0514366,            # Central meridian
        'x_0': 0,               # False easting
        'y_0': 0                # False northing
    }

    # Define the Lambert Conformal Conic projection
    lcc = pyproj.Proj(proj_params)

    # Convert each GPS coordinate to Cartesian
    cartesian_coords = []
    for lon, lat in gps_coords:
        x, y = lcc(lon, lat)
        cartesian_coords.append((x, y))

    return cartesian_coords


def read_kml_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    coordinates = []

    for placemark in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
        for line_string in placemark.findall('.//{http://www.opengis.net/kml/2.2}LineString'):
            coords_str = line_string.find('.//{http://www.opengis.net/kml/2.2}coordinates').text.strip()
            coords = [tuple(map(float, c.split(','))) for c in coords_str.split()]
            coordinates.extend(coords)

    return coordinates

def generate_time_unix(start_unix_time, num_points):
    return [start_unix_time + i*2.6285 for i in range(num_points)]

def save_to_file(filename, time_values, xy_coords):
    with open(filename, 'w') as f:
        for i in range(len(time_values)):
            f.write(str(time_values[i]) + ' ' + str(xy_coords[i][0]) + ' 0.0 ' + str(xy_coords[i][1]) + ' 0.0 0.0 0.0 1.0\n')

# Example KML file
kml_filename = 'wokol_osiedla_modif.kml'

# Read GPS coordinates from KML file
gps_coords = read_kml_file(kml_filename)

# Convert GPS coordinates to XY plane with the first point as the origin
xy_coords = convert_gps_to_xy(gps_coords)

# Generate time values (every second starting from current time)
num_points = len(xy_coords)
start_unix_time = float(1711773543.763)  # current time in Unix timestamp

time_values = generate_time_unix(start_unix_time, num_points)

# Save to text file
output_filename = 'wokol_osiedla.txt'
save_to_file(output_filename, time_values, xy_coords)

print("Data saved to", output_filename)
