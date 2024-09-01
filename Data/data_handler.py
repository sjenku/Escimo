import json


class DataHandler:

    def __init__(self,file_path):
        # Open the JSON file
        with open(file_path, 'r') as file:
            # Load the JSON data into a Python dictionary
            data = json.load(file)
            self.x_limits = data["x_limits"]
            self.y_limits = data["y_limits"]
            self.start_x = data["start_x"]
            self.start_y = data["start_y"]
            self.target_x = data["target_x"]
            self.target_y = data["target_y"]
            self.iceberg_count = data["iceberg_count"]


