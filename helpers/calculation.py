import numpy as np


def calculate_distance(geo_point1, geo_point2):
    """
    Calculates distance between two geo points of observed object.

    :param geo_point1: Latitude and Longitude of first point;
    :param geo_point2: Latitude and Longitude of second point;
    :return: Distance between two points in meters.
    """
    # Degrees to Meters
    DEG2METER = 0.00001

    lat1 = geo_point1["Latitude"]
    lon1 = geo_point1["Longitude"]
    alt1 = geo_point1["Altitude"]

    lat2 = geo_point2["Latitude"]
    lon2 = geo_point2["Longitude"]
    alt2 = geo_point2["Altitude"]

    # Difference converted from degrees to metres.
    diff_lon = (lon2 - lon1)/DEG2METER
    diff_lat = (lat2 - lat1)/DEG2METER
    diff_alt = (alt2 - alt1)

    distance = {"dx": diff_lon, "dy": diff_lat, "dz": diff_alt}
    return distance


def euclidean_distance(geo_point1, geo_point2):
    """
    Calculates euclidean distance.

    :param geo_point1: Geo Point 1 in Lat, Lon, Alt;
    :param geo_point2: Geo Point 2 in Lat, Lon, Alt;
    :return: Euclidean distance (in meters).
    """
    # Degrees to Meters
    DEG2METER = 0.00001

    lat1 = geo_point1["Latitude"]
    lon1 = geo_point1["Longitude"]
    alt1 = geo_point1["Altitude"]

    lat2 = geo_point2["Latitude"]
    lon2 = geo_point2["Longitude"]
    alt2 = geo_point2["Altitude"]

    # Difference converted from degrees to metres.
    diff_lon = (lon2 - lon1) / DEG2METER
    diff_lat = (lat2 - lat1) / DEG2METER
    diff_alt = (alt2 - alt1)

    distance = np.sqrt(np.power(diff_lon, 2) + np.power(diff_lat, 2) + np.power(diff_alt, 2))
    return distance


def calculate_velocity(geo_point1, timestamp1, geo_point2, timestamp2):
    """
    Calculates velocity of observed object.

    :param geo_point1: Geo Coordinates of first sampling
    :param timestamp1: Timestamp of first sampling
    :param geo_point2: Geo Coordinates of second sampling
    :param timestamp2: Timestamp of second sampling
    :return: Returns velocity (metres/sec) of object
    """
    # Distance(x, y, z) [m]
    distance = calculate_distance(geo_point1, geo_point2)

    # Time [sec]
    delta_time = abs(timestamp1 - timestamp2)/1000000

    if delta_time == 0.0:
        longitude_velocity = 0.0
        latitude_velocity = 0.0
        altitude_velocity = 0.0
    else:
        altitude_velocity = distance["dz"] / delta_time
        latitude_velocity = distance["dy"] / delta_time
        longitude_velocity = distance["dx"] / delta_time

    # Velocity [m/sec]
    velocity = {
        "dy": longitude_velocity,
        "dx": latitude_velocity,
        "dz": altitude_velocity
    }
    return velocity
