import random
import numpy as np
from shapely import MultiPoint, Point


class Engine:

    def __init__(self,start_pos,
                 end_pos,
                 num_of_polygons_range,
                 num_of_points_in_polygon_range,
                 polygon_radius_range,
                 surface_size):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.number_of_polygons = random.randint(num_of_polygons_range["from"],num_of_polygons_range["to"])
        self.num_of_points_in_polygon_range = num_of_points_in_polygon_range
        self.polygon_radius_range = polygon_radius_range
        self.surface_size = surface_size
        self.polygons = []


    def print(self):
        print("it's printing....")
        print("start_pos",self.start_pos,
              "end_pos",self.end_pos,
              "num_of_polygons",self.number_of_polygons,
              "num_of_points_in_polygon_range",self.num_of_points_in_polygon_range,
              "polygon_radius_range",self.polygon_radius_range,
              "surface_size",self.surface_size)

# - calculate random number of polygons
    def get_number_of_polygons(self)->int:
        return self.number_of_polygons

    def create_point_around_center(self,center_point,max_radius)->Point:
        # generate a random angle between 0 and 2*pi
        angle = np.random.uniform(0, 2 * np.pi)

        # generate a random radius between 0 and max_radius, ensuring uniform distribution
        radius = np.sqrt(np.random.uniform(0, max_radius ** 2))

        # convert polar coordinates (radius, angle) to cartesian coordinates (x, y)
        x = center_point.x + radius * np.cos(angle)
        y = center_point.y + radius * np.sin(angle)

        return Point(x,y)

    def create_polygon(self):
        """
           Create a polygon using the params given to the engine class.

           Returns:
           list[tuple[int, int]] : the points used to create a polygon
           TODO: write the type of convex_hull

           """

        # calculate random number of points from the given range
        points_in_polygon = random.randint(
            self.num_of_points_in_polygon_range["from"],
            self.num_of_points_in_polygon_range["to"])

        # calculate random max radius from the given range
        max_radius = random.randint(
            self.polygon_radius_range["from"],
            self.polygon_radius_range["to"])

        # random center point
        padding = int(self.surface_size/10) # insure that the center point not too close to surface borders
        center_point_x = random.randint(padding,self.surface_size - padding)
        center_point_y = random.randint(padding, self.surface_size - padding)
        center_point = Point(center_point_x, center_point_y)

        # create points for the polygon relative to the center and radius
        points = []
        for i in range(points_in_polygon):

            point = self.create_point_around_center(center_point,max_radius)

            # Ensure the point is within bounds
            while not (0 <= point.x <= self.surface_size) or not(0 <= point.y <= self.surface_size):
                point = self.create_point_around_center(center_point,max_radius)

            # add point
            points.append(point)

        # use convex_hull to wrap this points into a polygon
        multipoint = MultiPoint(points)
        convex_hull = multipoint.convex_hull

        return points,convex_hull

    def create_valid_polygon(self):

        points, new_polygon = self.create_polygon()
        valid = False

        # check if overlapping
        if len(self.polygons) != 0:
            # for every polygon that exist, check if not overlapping, if does, create a new one and check again
            while not valid:
                valid = True  # assume it's valid unless proven otherwise
                for another_polygon in self.polygons:
                    if (new_polygon.intersects(another_polygon) or
                            new_polygon.contains(self.start_pos) or
                            new_polygon.contains(self.end_pos)):
                        points , new_polygon = self.create_polygon()
                        valid = False # set to False to retry with a new polygon
                        break

        self.polygons.append(new_polygon)
        return points,new_polygon

    def get_metadata(self):
        data = {
            "x_limits": self.surface_size,
            "y_limits": self.surface_size,
            "start_x": self.start_pos.x,
            "start_y": self.start_pos.y,
            "target_x": self.end_pos.x,
            "target_y": self.end_pos.y,
            "icebergs_count":self.number_of_polygons,
            }

        icebergs = []  # list to store all iceberg dictionaries
        for iceberg_number, polygon in enumerate(self.polygons, start=1):
            points_dict = {}

            # iterate through the coordinates of the convex hull (polygon)
            for index, (x, y) in enumerate(polygon.exterior.coords[:-1], start=1):
                key = f"point{index}"
                points_dict[key] = {"x": x, "y": y}

            # create a dictionary for the current iceberg
            iceberg_dict = {
                "iceberg_number": iceberg_number,
                "iceberg_points": points_dict
            }

            # Add the iceberg dictionary to the list of icebergs
            icebergs.append(iceberg_dict)

        data["icebergs"] = icebergs

        return data

