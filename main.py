import os

from helpers.clustering import clustering
from helpers.draw_plot import plot_scatter
from triangulate_samples import triangulate_samples
from helpers.samples_analyzer import analyze_samples
from utils.json_utils import read_samples_from_dir, create_samples_dictionary, cluster_to_json


def calculate_triangulation(read_from_file=False, reports: dict = None, plot_cluster=False, square_error_threshold=1000):

    samples = {}

    if reports is not None:
        samples = create_samples_dictionary(reports)
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

    if plot_cluster:
        plot_scatter(clusters)

    return cluster_to_json(clusters)


if __name__ == '__main__':
    calculate_triangulation()
