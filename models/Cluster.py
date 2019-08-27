class Cluster:
    def __init__(self, points):
        """
        Represents cluster object.

        :param points: Points list, that belongs to current cluster.
        """
        self.points = points
        self.reports_ids = None
        self.beginTimestamp = None
        self.endTimestamp = None
        self.mean_velocity = None
        self.mean_geo_location = None
        self.set_parameters()

    def __getitem__(self, key):
        """
        Gets item by key, a object['key']
        :param key: parameter of object
        :return: value of object
        """
        return getattr(self, key)

    def set_parameters(self):
        """

        :return:
        """
        unique = []
        min_timestamp = None
        max_timestamp = None
        for point in self.points:

            # Find oldest sample
            if min_timestamp is None or point.timestamp <= min_timestamp:
                min_timestamp = point.timestamp

            # Find youngest sample
            if max_timestamp is None or point.timestamp >= max_timestamp:
                max_timestamp = point.timestamp

            if point.sample1_ids[0] not in unique:
                unique.append(point.sample1_ids[0])
            if point.sample2_ids[0] not in unique:
                unique.append(point.sample2_ids[0])

        self.beginTimestamp = min_timestamp
        self.endTimestamp = max_timestamp
        self.reports_ids = unique

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
