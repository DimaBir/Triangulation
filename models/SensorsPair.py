class SensorsPair:
    def __init__(self, sensor1_id, sensor2_id):
        """
        Represents pair of sensors, contains collection of relevant samples and velocity of observed object.

        :param sensor1_id: ID of first sensor in pair;
        :param sensor2_id: ID of second sensor in pair.
        """
        self.sensors_id = {"Sensor1 ID": sensor1_id, "Sensor2 ID": sensor2_id}
        self.samples = []
        self.velocity = None

    def add_sample(self, sample):
        """
        Adds new sample to the collection.
        :param sample: New sample
        """
        self.samples.append(sample)
        self.velocity = self.update_velocity(sample)

    def update_velocity(self, sample):
        from helpers.calculation import calculate_velocity
        """
        Updates velocity of observation object of pair of sensors

        :param sample: New sample that add to the system
        :return: Dictionary of velocity calculated in [m/sec], relatively to the first observed sample, in 3 axes.
        """
        # If sample is first, its velocity is zero
        if len(self.samples) == 1:
            self.samples[-1].set_velocity({
                    "dy": 0.0,
                    "dx": 0.0,
                    "dz": 0.0
                }
            )
            return None

        first_element = self.samples[0]

        # Update velocity of last observed point relatively to the first observed point
        velocity = calculate_velocity(sample.geo_point, sample.timestamp, first_element.geo_point,
                                      first_element.timestamp)
        self.samples[-1].set_velocity(velocity)

        return velocity
