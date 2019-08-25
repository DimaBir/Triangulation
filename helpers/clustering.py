from helpers.calculation import euclidean_distance
from models.Cluster import Cluster
from models.Graph import Graph
from itertools import permutations

def clustering(sensor_pairs_data):
    """
    Implements Clustering Algorithm. Complexity: O(|points^2|)
    :param sensor_pairs_data: collection of points have been spread to pairs of sensors, that observed them
    :return: list of clusters, each cluster contains geo_location of its centroid and its velocity
    """

    # Throw all points in one collection,
    points = []
    for pair_of_sensors in sensor_pairs_data:
        for sample in pair_of_sensors.samples:
            points.append(sample)

    # Create edges between points, where euclidean distance is less than distance threshold
    # TODO: Need to be optimized
    graph = Graph(len(points))
    for indexes in permutations(range(len(points)), 2):
        i = indexes[0]
        j = indexes[1]
        if euclidean_distance(points[i].geo_point, points[j].geo_point) <= graph.distance_metric:
            graph.add_edge(i, j)

    # Create Strongly Connected Components for created graph
    scc_of_point_ids = graph.get_sccs()

    # Create clusters from strongly connected components
    clusters = []
    for scc in scc_of_point_ids:
        scc_of_objects = []
        for id in scc:
            scc_of_objects.append(points[id])
        clusters.append(Cluster(scc_of_objects))

    return clusters




