import uuid
import time
import json

from models.Sample import Sample
from helpers.samples_analyzer import analyze_samples
from triangulate_samples import triangulate_samples
from utils.json_utils import read_samples_from_dir, is_in_samples
from helpers.clustering import clustering
from helpers.draw_plot import plot_scatter, plot_scatter_points, plot_scatter_pair_of_sensors

import os


def calculate_triangulation(use_new=True, reports: dict = None, plot_cluster=False, square_error_threshold=1000):

    # Read data part
    # Read from JSON
    samples = {}
    if use_new:
        reports = None
        with open('sampleJSON.json') as json_file:
            reports = json.load(json_file)
        for report in reports['reports']:
            report_id = report['id']
            read_samples = []
            for data in report['data']:
                timestamp = data['timestamp']
                altitude = data['origin']['altitude']
                latitude = data['origin']['latitude']
                longitude = data['origin']["longitude"]
                # TODO: dont forget to change to data["origin"]["gravity"]["y"]
                gravity = data["orientation"]["gravity"][1]
                true_heading = data["orientation"]["trueHeading"]

                if not is_in_samples(str(report_id) + str(timestamp), read_samples):
                    read_samples.append(
                        Sample(report_id, timestamp, altitude, latitude, longitude, gravity, true_heading)
                    )
            samples[report_id] = read_samples
    else:
        # Read from dir
        script_dir_name = os.path.dirname(__file__)
        samples_dir_name = os.path.join(script_dir_name, 'data')
        samples = read_samples_from_dir(samples_dir_name)

    # Calculate triangulation for N samples
    observed_points = triangulate_samples(samples)
    if not observed_points:
        print('TYPE' + str(type(observed_points)))
        return

    # Associate samples with pair of sensors that observed it, in order to calculate velocity
    sensor_pairs_data = analyze_samples(observed_points, square_error_threshold)

    # Clustering part
    clusters = clustering(sensor_pairs_data)

    # Calculate Centroids for clusters (distance and speed)
    for i in range(len(clusters)):
        clusters[i].calculate_mean_velocity()

    for i in range(len(clusters)):
        clusters[i].calculate_centroid()

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
    if plot_cluster:
        plot_scatter(clusters)
    # plot_scatter_points(observed_points)
    # plot_scatter_pair_of_sensors(sensor_pairs_data, samples)

    return clusters_to_return


if __name__ == '__main__':
    calculate_triangulation()
