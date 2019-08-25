from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
import matplotlib.pyplot as plt


def plot_scatter(clusters):
    # Draw 3D plot
    colors = ['g', 'r', 'c', 'm', 'y']
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i in range(len(clusters)):
        # X - Lat
        x = []

        # Y - Lon
        y = []

        # Z - Alt
        z = []
        for point in clusters[i].points:
            x.append(point.geo_point['Latitude'] / 0.00001)
            y.append(point.geo_point['Longitude'] / 0.00001)
            z.append(point.geo_point['Altitude'])

        # Centroid
        centroid_location_lat = clusters[i].mean_geo_location['Latitude']
        centroid_location_lon = clusters[i].mean_geo_location['Longitude']
        centroid_location_alt = clusters[i].mean_geo_location['Altitude']
        ax.scatter(
            centroid_location_lat / 0.00001,
            centroid_location_lon / 0.00001,
            centroid_location_alt,
            c='r', marker='*', s=20*2**3)
        ax.text(
            centroid_location_lat / 0.00001,
            centroid_location_lon / 0.00001,
            centroid_location_alt + 0.25,
            "[" + str("%.5f" % round(centroid_location_lat, 5)) + "]" +
            "[" + str("%.5f" % round(centroid_location_lon, 5)) + "]" +
            "[" + str("%.5f" % round(centroid_location_alt, 5)) + "]"
        )

        a = Arrow3D([centroid_location_lat / 0.00001, (centroid_location_lat / 0.00001) + (clusters[i].mean_velocity['dx'])*100],
                    [centroid_location_lon / 0.00001, (centroid_location_lon / 0.00001) + (clusters[i].mean_velocity['dy'])*100],
                    [centroid_location_alt, centroid_location_alt + (clusters[i].mean_velocity['dz'])*100],
                    mutation_scale=20, lw=1, arrowstyle="-|>", color="b")

        ax.add_artist(a)

        ax.text(
            (centroid_location_lat / 0.00001) + (clusters[i].mean_velocity['dx']) * 100,
            (centroid_location_lon / 0.00001) + (clusters[i].mean_velocity['dy']) * 100,
            centroid_location_alt + (clusters[i].mean_velocity['dz']) * 100 + 0.125,
            "V", color='blue'
            #"[" + str("%.5f" % round(centroid_location_lat, 5)) + "]" +
            #"[" + str("%.5f" % round(centroid_location_lon, 5)) + "]" +
            #"[" + str("%.5f" % round(centroid_location_alt, 5)) + "]"
        )

        # Cluster
        ax.scatter(x, y, z, c=colors[i], marker='o')

    ax.set_xlabel('X [m]')
    ax.set_ylabel('Y [m]')
    ax.set_zlabel('Altitude [m]')

    plt.show()


def plot_scatter_pair_of_sensors(sensor_pairs, samples):

    # Samples collection of samples to het sensors location
    # Draw 3D plot
    colors = ['g', 'r', 'y', 'c', 'm']
    markers = ['o', '^', 'D', '1', 'x']
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i in range(len(sensor_pairs)):
        # X - Lat
        x = []

        # Y - Lon
        y = []

        # Z - Alt
        z = []
        for point in sensor_pairs[i].samples:
            x.append(point.geo_point['Latitude'] / 0.00001)
            y.append(point.geo_point['Longitude'] / 0.00001)
            z.append(point.geo_point['Altitude'])

        ax.scatter(x, y, z, c=colors[i], marker=markers[i], label='ID1: ' +
                   str(sensor_pairs[i].sensors_id['Sensor1 ID']) +
                   ', ID2: ' + str(sensor_pairs[i].sensors_id['Sensor2 ID']))

        # Sensor

        # Extract sensor position
        sensor_location = samples['sample00' + str(i+1) + '.json'][0].sensor_geo_location

        ax.scatter(
            sensor_location.latitude / 0.00001,
            sensor_location.longitude / 0.00001,
            sensor_location.altitude,
            c='k', marker='$' + str(samples['sample00' + str(i+1) + '.json'][0].sensor_id) + '$', s=20*2**4)

    ax.set_xlabel('X [m]')
    ax.set_ylabel('Y [m]')
    ax.set_zlabel('Altitude [m]')
    ax.legend()

    plt.show()


def plot_scatter_points(points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # X - Lat
    x = []

    # Y - Lon
    y = []

    # Z - Alt
    z = []

    for point in points:
        x.append(point.geo_point['Latitude'] / 0.00001)
        y.append(point.geo_point['Longitude'] / 0.00001)
        z.append(point.geo_point['Altitude'])

        # Cluster
        ax.scatter(x, y, z, c='r', marker='o')

    ax.set_xlabel('X [m]')
    ax.set_ylabel('Y [m]')
    ax.set_zlabel('Altitude [m]')

    plt.show()


class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)









