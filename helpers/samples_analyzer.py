from models.SensorsPair import SensorsPair


def is_belongs_to_sensor_pairs(sample, sensors_pair):
    """
    Utility functions that checks if sample was made by this Sensors Pair

    :param sample: Sample
    :param sensors_pair: Sensor Pairs object includes pair of sensors ids
    :return: True - if sample was made by this pair of sensors, False - else
    """
    if sample.sample1_ids[0] == sensors_pair.sensors_id["Sensor1 ID"] and \
       sample.sample2_ids[0] == sensors_pair.sensors_id["Sensor2 ID"] or \
       sample.sample2_ids[0] == sensors_pair.sensors_id["Sensor1 ID"] and \
       sample.sample1_ids[0] == sensors_pair.sensors_id["Sensor2 ID"]:
        return True

    return False


def distinct_sensors_pairs(samples):
    """
    Creates distinct pairs of sensors, for example, given A,B,C sensors, function returns, distinct pairs, such that:
    (A,B); (A,C); (B,C)

    :param samples: Collection of samples from all sensors
    :return: Collection of distinct Sensor Pairs
    """
    sensors_pairs = [SensorsPair(samples[0].sample1_ids[0], samples[0].sample2_ids[0])]
    for triangulated_samples in samples:
        exist = False
        for sensor_pair in sensors_pairs:
            exist = exist or is_belongs_to_sensor_pairs(triangulated_samples, sensor_pair)

        if not exist:
            sensors_pairs.append(SensorsPair(triangulated_samples.sample1_ids[0],
                                             triangulated_samples.sample2_ids[0]))

    return sensors_pairs


def fill_samples(samples, sensors_pairs, threshold):
    """
    Fill samples by pair of sensors that made the measurements, updates Sensors Pair collection.

    :param samples: Collection of all samples
    :param sensors_pairs: Collection of pairs of sensors
    :param threshold: Threshold for Square Error

    """
    for sample in samples:
        for sensor_pair in sensors_pairs:
            if is_belongs_to_sensor_pairs(sample, sensor_pair) and sample.square_error[0] <= threshold:
                sensor_pair.add_sample(sample)


def sort_samples(sensors_pairs):
    [sensor_pair.sort_samples() for sensor_pair in sensors_pairs]


def analyze_samples(samples, threshold):
    """
    Analyzes and collects data of the points for pairs of sensors.

    :param samples: List of samples;
    :param threshold: Threshold of Square Error, samples with less then are legal;
    :return: List of objects that represents pair of sensors and their samples.
    """

    # Create distinct sensor pairs
    sensors_pairs = distinct_sensors_pairs(samples)

    # Fill samples collections of sensors pairs
    fill_samples(samples, sensors_pairs, threshold)

    return sensors_pairs
