class ObservedPoint:
    def __init__(self, geo_point, square_error, timestamp, sample1_ids, sample2_ids):
        """
        Represents triangulated parameters of observed point.

        :param geo_point: Geo Point of observed point;
        :param square_error: Square error of calculation;
        :param timestamp: Timestamp of observation;
        :param sample1_ids: ID Tuple of first sensor and sample;
        :param sample2_ids: ID Tuple of second sensor and sample.
        """
        self.geo_point = geo_point
        self.square_error = square_error
        self.timestamp = timestamp
        self.sample1_ids = sample1_ids
        self.sample2_ids = sample2_ids

        # TODO: tmp id, ask what format of id
        self.id = str(sample1_ids[1]) + str(sample2_ids[1])
        self.velocity = None

    def set_velocity(self, velocity):
        """
        Sets velocity of ObservedPoint.

        :param velocity: velocity value
        :return: None
        """
        self.velocity = velocity
