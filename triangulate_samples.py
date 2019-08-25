from models.ObservedPoint import ObservedPoint
from triangulate_d import triangulate_d

import numpy as np
import itertools
import math


def triangulate_samples(samples, time_delta=100000000, min_range=0.0, max_range=500.0):
    """
    Calculates triangulation for each sample of N sensors.

    :param samples: Dictionary: Key = Sensor; Value = List of samples of sensor;
    CONFIGURABLE PARAMS:
    :param time_delta: Threshold for difference between timestamps of samples. 1000000 = 1 sec
    :param min_range: Minimal range from sensor to the observed point, in meters, DEFAULT = 0.0[m];
    :param max_range: Maximal range from sensor to the observed point, in meters, DEFAULT = 500.0[m];
    :return: List of ObservedPoints: {Geo_Point, Square Error, Timestamp of sampling,
                                    Sample1: tuple(sensor1_id, sample1_id), Sample2: tuple(sensor2_id, sample2_id)}.
    """
    results = []
    # Calculate triangulation for each sample from different sensors.
    # Example: Given A,B,C sensors with m,n,l samples respectively
    #          so check will be performed for: (A,B), (A,C), (B,C) pairs of sensors
    #          for each combination of samples (mxn), (mxl), (nxl) (x - cross product)
    for pair_of_sensors in itertools.combinations(samples, 2):
        for sample1 in samples[pair_of_sensors[0]]:
            for sample2 in samples[pair_of_sensors[1]]:

                if abs(int(sample1.timestamp) - int(sample2.timestamp)) >= time_delta:
                    continue

                # Sensor 1 parameters
                lat1 = sample1.sensor_geo_location.latitude
                alt1 = sample1.sensor_geo_location.altitude
                lon1 = sample1.sensor_geo_location.longitude
                az1 = sample1.sensor_orientation.true_heading
                el1 = (np.pi - math.acos(sample1.sensor_orientation.gravity)) * 180 / np.pi

                # Sensor 2 parameters
                lat2 = sample2.sensor_geo_location.latitude
                alt2 = sample2.sensor_geo_location.altitude
                lon2 = sample2.sensor_geo_location.longitude
                az2 = sample2.sensor_orientation.true_heading
                el2 = (np.pi - math.acos(sample2.sensor_orientation.gravity)) * 180 / np.pi

                # Calculate triangulation
                geo_point, err2, r = triangulate_d(lat1, lon1, alt1, lat2, lon2, alt2, az1, el1, az2, el2)

                # Check if range from both sensors to point in proper range [min_range, max_range]
                if not min_range <= r[0][0] <= max_range or \
                   not min_range <= r[1][0] <= max_range:
                    continue

                results.append(ObservedPoint(geo_point, err2, sample1.timestamp, (sample1.sensor_id, sample1.sample_id),
                                             (sample2.sensor_id, sample2.sample_id)))

    return results
