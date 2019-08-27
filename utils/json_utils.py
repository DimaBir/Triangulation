from models.Sample import Sample

import json
import os
import re


def read_samples_from_dir(directory_path):
    """
    Reads samples from given directory.

    :param directory_path: absolute path to directory with samples as JSON;
    :return: Dictionary: Key: sensor id; Value: collection of samples os current sensor.
    """
    sensors_and_samples = {}
    files_in_dir = os.listdir(directory_path)
    sensors = [i for i in files_in_dir if i.endswith('.json')]

    for sensor in sensors:
        sensors_and_samples[sensor] = read_json(os.path.join(directory_path, sensor))

    return sensors_and_samples


def is_in_samples(sample_id, samples):
    """
    Utility functions that checks if sample already exist in collection.

    :param sample_id: Sample_ID of new sample;
    :param samples: List of already read samples;
    :return: True if sample is in list, else False.
    """
    for sample in samples:
        if sample_id == sample.sample_id:
            return True
    return False


def read_json(file_path):
    """
    Reads JSON file and collects samples.

    :param file_path: Absolute path to JSON file of samples;
    :return: Returns list of samples.
    """
    samples = []
    with open(file_path) as json_file:
        data = json.load(json_file)
        basename = os.path.basename(file_path)
        sensor_id = os.path.splitext(basename)[0]
        sensor_id = re.sub("\D", "", sensor_id)
        for p in data["observedSpots"]:
            timestamp = p["timestamp"]
            altitude = p["location"]["altitude"]
            latitude = p["location"]["latitude"]
            longitude = p["location"]["longitude"]
            gravity = p["orientation"]["gravity"][1]
            true_heading = p["orientation"]["trueHeading"]

            if not is_in_samples(str(sensor_id) + str(timestamp), samples):
                samples.append(Sample(sensor_id, timestamp, altitude, latitude, longitude, gravity, true_heading))

    return samples
