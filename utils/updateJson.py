import json
import os


def update_json(file_path):

    # Read
    with open(file_path, "r") as json_file:
        data = json.load(json_file)

    i = 0
    first_timestamp = None

    # Update
    for p in data["observedSpots"]:

        if i == 0:
            first_timestamp = p["timestamp"]
            i += 1

        p["timestamp"] -= first_timestamp


    # Write
    with open(file_path, "w") as json_file:
        json.dump(data, json_file)


def update_samples_from_dir(directory_path):

    files_in_dir = os.listdir(directory_path)
    sensors = [i for i in files_in_dir if i.endswith('.json')]

    for sensor in sensors:
        update_json(os.path.join(directory_path, sensor))


if __name__ == "__main__":
    script_dir_name = os.path.dirname(__file__)
    samples_dir_name = os.path.join(script_dir_name, '..\..\data')
    update_samples_from_dir(samples_dir_name)