import json

from shapely import Point


class Configurations:

    #TODO: self.start_position...

    def __init__(self,file_path):
        # Open the JSON file
        with open(file_path, 'r') as file:
            # Load the JSON data into a Python dictionary
            data = json.load(file)
            self.start_position = data["start_position"]
            self.end_position = data["end_position"]
            self.number_of_polygons_range = data["number_of_polygons_range"]
            self.number_of_points_in_polygon_range = data["number_of_points_in_polygon_range"]
            self.polygon_radius_range = data["polygon_radius_range"]
            self.surface_size = data["surface_size"]

    def get_start_position(self):
        return Point(self.start_position["x"],self.start_position["y"])

    def get_end_position(self):
        return Point(self.end_position["x"],self.end_position["y"])

    def get_number_of_polygons_range(self):
        return self.number_of_polygons_range

    def get_number_of_points_in_polygon_range(self):
        return self.number_of_points_in_polygon_range

    def get_polygon_radius_range(self):
        return self.polygon_radius_range

    def get_surface_size(self):
        return self.surface_size


