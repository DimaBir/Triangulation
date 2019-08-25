class SensorGeoLocation:
    def __init__(self, altitude, latitude, longitude):
        self.altitude = altitude
        self.latitude = latitude
        self.longitude = longitude


class SensorOrientation:
    def __init__(self, gravity, true_heading):
        self.gravity = gravity
        self.true_heading = true_heading


class Sample:
    def __init__(self, sensor_id, timestamp, altitude, latitude, longitude, gravity, true_heading):
        """
        Represents observed sample of sensor.

        :param sensor_id: Id of sensor that made this sample;
        :param timestamp: Time of sampling;
        :param altitude: Altitude of sensor;
        :param latitude: Latitude of sensor;
        :param longitude: Longitude of sensor;
        :param gravity: Vertical Axis of Gravity;
        :param true_heading: True Heading.
        """
        self.sensor_id = sensor_id
        self.sample_id = str(sensor_id) + str(timestamp)
        # TODO: Add SensorID and Sample ID, ask format of ids!
        self.timestamp = timestamp
        self.sensor_geo_location = SensorGeoLocation(altitude, latitude, longitude)
        self.sensor_orientation = SensorOrientation(gravity, true_heading)
