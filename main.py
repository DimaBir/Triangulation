import uuid
import time

from helpers.samples_analyzer import analyze_samples
from triangulate_samples import triangulate_samples
from utils.json_utils import read_samples_from_dir
from helpers.clustering import clustering
from helpers.draw_plot import plot_scatter, plot_scatter_points, plot_scatter_pair_of_sensors

import os


def calculate_triangulation():

    # TODO: Ask input for a data?
    # Read data part
    script_dir_name = os.path.dirname(__file__)
    samples_dir_name = os.path.join(script_dir_name, './data')
    samples = read_samples_from_dir(samples_dir_name)

    # Calculate triangulation for N samples
    observed_points = triangulate_samples(samples)

    # Associate samples with pair of sensors that observed it, in order to calculate velocity
    sensor_pairs_data = analyze_samples(observed_points, 1000)

    # Clustering part
    clusters = clustering(sensor_pairs_data)

    # Calculate Centroids for clusters (distance and speed)
    for i in range(len(clusters)):
        clusters[i].calculate_mean_velocity()

    for i in range(len(clusters)):
        clusters[i].calculate_centroid()

    clusters_to_return = {
        'newClusters': [],
        'reportUpdates': []
    }
    for i in range(len(clusters)):
        clusters_to_return['newClusters'].append({
            "id": str(uuid.uuid4()),
            "timestamp": int(time.time()*1000.0),
            "pathId": None,
            "position": {
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
        clusters_to_return['newClusters'].append({
            "id": str(uuid.uuid4()),
            "timestamp": int(time.time() * 1000.0),
            "pathId": None,
            "position": {
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
        clusters_to_return['newClusters'].append({
            "id": str(uuid.uuid4()),
            "timestamp": int(time.time() * 1000.0),
            "pathId": None,
            "position": {
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
        clusters_to_return['reportUpdates'].append({
            "reportId": str(uuid.uuid4()),
            "oldClusterId": str(uuid.uuid4()),
            "newClusterId": str(uuid.uuid4()),
        })

    # plot_scatter(clusters)
    # plot_scatter_points(observed_points)
    # plot_scatter_pair_of_sensors(sensor_pairs_data, samples)

    # TODO: Ask Vova what to return and what is an API.
    print("For debug purposes")
    return clusters_to_return


if __name__ == '__main__':
    calculate_triangulation()