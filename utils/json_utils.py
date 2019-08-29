from models.Sample import Sample

import os
import re
import json
import uuid


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
        sensors_and_samples[sensor] = read_json_from_file(os.path.join(directory_path, sensor))

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


def read_json_from_file(file_path):
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


def create_samples_dictionary(reports):
    """
    Creates collection from dictionary

    :param reports: dictionary, that was created from post request JSON
    :return: collection of Sample objects
    """
    samples = {}

    if reports is not None:
        for report in reports['reports']:
            report_id = report['id']
            read_samples = []
            for data in report['data']:
                timestamp = data['timestamp']

                # Origin
                altitude = data['origin']['altitude']
                latitude = data['origin']['latitude']
                longitude = data['origin']["longitude"]

                # Orientation
                gravity = data["orientation"]["gravity"]["y"]
                true_heading = data["orientation"]["trueHeading"]

                # Make sure that collection is distinct
                if not is_in_samples(str(report_id) + str(timestamp), read_samples):
                    read_samples.append(
                        Sample(report_id, timestamp, altitude, latitude, longitude, gravity, true_heading)
                    )
            samples[report_id] = read_samples
    return samples


def cluster_to_json(clusters):
    """
    Transforms Cluster object to json file

    :param clusters:
    :return:
    """
    clusters_to_return = {
        'clusters': []
    }
    for i in range(len(clusters)):
        clusters_to_return['clusters'].append({
            "id": str(uuid.uuid4()),
            "beginTimestamp": clusters[i].beginTimestamp,
            "endTimestamp": clusters[i].endTimestamp,
            "reportsIds": clusters[i].reports_ids,
            "location": {
                "latitude": clusters[i]['mean_geo_location']['Latitude'],
                "longitude": clusters[i]['mean_geo_location']['Longitude'],
                "altitude": clusters[i]['mean_geo_location']['Altitude'],
            },
            "velocity": {
                "dx": clusters[i]['mean_velocity']['dx'],
                "dy": clusters[i]['mean_velocity']['dy'],
                "dz": clusters[i]['mean_velocity']['dz']
            }
        })

    return clusters_to_return
