import math
import numpy as np


def triangulate_d(lat1, lon1, alt1, lat2, lon2, alt2, az1, el1, az2, el2):
    """
    Calculates the geo position of a target, by given geo points of two observers, azimuth and elevation to the target.
    REMARK: All angels are expected to be in Degrees!

    :param lat1: Latitude of first sensor;
    :param lon1: Longitude of first sensor;
    :param alt1: Altitude of first sensor;
    :param lat2: Latitude of second sensor;
    :param lon2: Longitude of second sensor;
    :param alt2: Altitude of second sensor;
    :param az1: Azimuth of first sensor;
    :param el1: Elevation of first sensor;
    :param az2: Azimuth of second sensor;
    :param el2: Elevation of second sensor;
    :return: Tuple of triangulated geo positions as dictionary, including altitude of the target and square error.
    """
    # Degrees to Radians
    DEG2RAD = np.pi / 180

    # Earth radius in meters
    Ra = 6378137

    # Simple conversion between GEO coordinates to Cartesian coordinates
    p1 = np.array([[lat1 * DEG2RAD * Ra, lon1 * DEG2RAD * Ra * math.cos(DEG2RAD * lat1), alt1]]).T
    p2 = np.array([[lat2 * DEG2RAD * Ra, lon2 * DEG2RAD * Ra * math.cos(DEG2RAD * lat1), alt2]]).T

    # Direction vector of first sensor
    u1 = np.array([
        [math.cos(DEG2RAD * az1) * math.cos(DEG2RAD * el1),
         math.sin(DEG2RAD * az1) * math.cos(DEG2RAD * el1),
         math.sin(DEG2RAD * el1)]
    ]).T

    # Direction vector of first sensor
    u2 = np.array([
        [math.cos(DEG2RAD * az2) * math.cos(DEG2RAD * el2),
         math.sin(DEG2RAD * az2) * math.cos(DEG2RAD * el2),
         math.sin(DEG2RAD * el2)]
    ]).T

    u11 = np.asscalar(np.dot(u1.T, u1))  # u1.T * u1
    u12 = np.asscalar(np.dot(u2.T, u1))  # u2.T * u1
    u22 = np.asscalar(np.dot(u2.T, u2))  # u2.T * u2

    # Difference in location between 2 sensors
    dp = p2 - p1

    # Ranges from 2 sensors
    r = np.dot(np.array([
        [u22, u12],
        [u12, u11]
    ]),
        np.array([
            [np.asscalar(np.dot(u1.T, dp))],
            [-np.asscalar(np.dot(u2.T, dp))]
        ])) / (u11 * u22 - np.power(u12, 2))

    # Minimal difference between 2 lines in cartesian coordinates
    err = np.dot(np.hstack((u1, -u2)), r) - dp

    # Square distance between 2 lines
    err2 = np.power(err[0], 2) + np.power(err[1], 2) + np.power(err[2], 2)

    # Triangulation point (can be more accurate by averaging 2 points)
    point = np.add(p1, np.dot(u1, r[0]).reshape(3, 1))

    # Converting back to GEO coordinates as a row
    geo_point_vec = np.array(
        [point[0] / Ra / DEG2RAD,                             # Latitude
         point[1] / Ra / math.cos(DEG2RAD * lat1) / DEG2RAD,  # Longitude
         point[2]]                                            # Altitude
    ).reshape(1, 3)

    geo_point = {
        "Latitude":  geo_point_vec[0][0],
        "Longitude": geo_point_vec[0][1],
        "Altitude":  geo_point_vec[0][2]
    }

    return geo_point, err2, r
