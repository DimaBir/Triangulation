class Cluster:
    def __init__(self, points):
        """
        Represents cluster object.

        :param points: Points list, that belongs to current cluster.
        """
        self.points = points
        self.mean_velocity = None
        self.mean_geo_location = None

    def __getitem__(self, key):
        """
        Gets item by key, a object['key']
        :param key: parameter of object
        :return: value of object
        """
        return getattr(self, key)

    def calculate_centroid(self):
        """
        Calculates centroid of the cluster. And updates mean_geo_location.

        :return: None
        """
        lat_sum = 0.0
        lon_sum = 0.0
        alt_sum = 0.0
        for point in self.points:
            lat_sum = lat_sum + point.geo_point['Latitude']
            lon_sum = lon_sum + point.geo_point['Longitude']
            alt_sum = alt_sum + point.geo_point['Altitude']
        if len(self.points) != 0:
            self.mean_geo_location = {
                "Latitude": lat_sum / len(self.points),
                "Longitude": lon_sum / len(self.points),
                "Altitude": alt_sum / len(self.points)
            }
            return

    def calculate_mean_velocity(self):
        """
        Calculates and updates mean velocity in all 3 axes for current cluster.

        :return: None
        """
        velocity_sum_dx = 0.0
        velocity_sum_dy = 0.0
        velocity_sum_dz = 0.0
        for point in self.points:
            velocity_sum_dx = velocity_sum_dx + point.velocity['dx']
            velocity_sum_dy = velocity_sum_dy + point.velocity['dy']
            velocity_sum_dz = velocity_sum_dz + point.velocity['dz']
        if len(self.points) != 0:
            self.mean_velocity = {
                "dx": velocity_sum_dx / len(self.points),
                "dy": velocity_sum_dy / len(self.points),
                "dz": velocity_sum_dz / len(self.points)
            }
