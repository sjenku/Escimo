import math
import random
from math import dist
from turtle import Vec2D

import numpy as np
from scipy.constants import point
from shapely import MultiPoint, Point, Polygon
from pydantic import BaseModel, conint, model_validator
from shapely.lib import distance

from Module.engine_data import EngineData
from Module.iceberg import Iceberg
from Module.iceberg_points import IcebergPoints
from Module.point_wrapper import PointWrapper
from Module.polygon_wrapper import PolygonWrapper
from Module.range import Range

# helper function that creates a point around a center_point no further than the max_radius
def create_point_around_center(center_point, max_radius) -> Point:

    # generate a random angle between 0 and 2*pi
    angle = np.random.uniform(0, 2 * np.pi)

    # generate a random radius between 0 and max_radius, ensuring uniform distribution
    radius = np.sqrt(np.random.uniform(0, max_radius ** 2))

    # convert polar coordinates (radius, angle) to cartesian coordinates (x, y)
    x = center_point.x + radius * np.cos(angle)
    y = center_point.y + radius * np.sin(angle)

    return Point(x,y)


class EngineEskimo(BaseModel):
    """
    EngineEskimo is a class that responsible to create all the calculations necessary for 'Creating the Problem'
    meaning by that, EngineEskimo calculates and creates the Polygons on random locations
    """


    start_pos: Point  # start position of the point from which we need to move toward the target
    end_pos: Point  # end position is a position of the target
    number_of_polygons_range: Range # the min and max number of polygons that can be created
    num_of_points_in_polygon_range : Range # the min and max points that each polygon creat from
    polygon_radius_range : Range
    surface_size : conint(ge=0)
    polygons: list[Polygon] = []
    _number_of_polygons: int = 0


    def __init__(self, **data):
        super().__init__(**data)


    class Config:
        arbitrary_types_allowed = True # we need this to support the Point type


    @model_validator(mode='after')
    def generate_number_of_polygons(self):
        self._number_of_polygons = self.number_of_polygons_range.get_random()


    def print(self) -> None:
        print("it's printing....")
        print("start_pos",self.start_pos,
              "end_pos",self.end_pos,
              "num_of_polygons",self.number_of_polygons,
              "num_of_points_in_polygon_range",self.num_of_points_in_polygon_range,
              "polygon_radius_range",self.polygon_radius_range,
              "surface_size",self.surface_size)

    # calculate random number of polygons
    def get_number_of_polygons(self) -> int:
        return self._number_of_polygons

    def create_polygon(self) -> (list[Point],Polygon):
        """
           Create a polygon using the params given to the engine class.

           Returns:
           list[tuple[int, int]] : the points used to create a polygon.
           Polygon: the polygon object that been created with cunvex_hull

        """

        # calculate random number of points from the given range
        points_in_polygon = random.randint(
            self.num_of_points_in_polygon_range.from_,
            self.num_of_points_in_polygon_range.to)

        # calculate random max radius from the given range
        max_radius = random.randint(
            self.polygon_radius_range.from_,
            self.polygon_radius_range.to)

        # random center point
        padding = int(self.surface_size/10) # insure that the center point not too close to surface borders
        center_point_x = random.randint(padding,self.surface_size - padding)
        center_point_y = random.randint(padding, self.surface_size - padding)
        center_point = Point(center_point_x, center_point_y)

        # create points for the polygon relative to the center and radius
        points = []
        for i in range(points_in_polygon):

            point = create_point_around_center(center_point,max_radius)

            # Ensure the point is within bounds
            while not (0 <= point.x <= self.surface_size) or not(0 <= point.y <= self.surface_size):
                point = create_point_around_center(center_point,max_radius)

            # add point
            points.append(point)

        # use convex_hull to wrap this points into a polygon
        # multipoint = MultiPoint(points)
        # convex_hull = multipoint.convex_hull
        convex_hull = self._graham_scan(points)
        wrapper = PolygonWrapper.from_polygon(convex_hull)

        return points,convex_hull

    def create_valid_polygon(self) -> (list[Point],Polygon):

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


    def get_data(self) -> EngineData:
        icebergs = []
        for iceberg_number, polygon in enumerate(self.polygons, start=1):

            coords_dict = {}
            point_counter = 1
            for coord in polygon.exterior.coords:
                key = f'point{point_counter}'
                coords_dict[key] = PointWrapper(x = coord[0], y = coord[1])
                point_counter += 1

            icebergs.append(Iceberg(
                iceberg_number = iceberg_number,
                iceberg_points = IcebergPoints(coords_dict)
            ))

        data = EngineData(
            x_limits = self.surface_size,
            y_limits = self.surface_size,
            start_x = self.start_pos.x,
            start_y = self.start_pos.y,
            target_x = self.end_pos.x,
            target_y = self.end_pos.y,
            icebergs_count = self._number_of_polygons,
            icebergs = icebergs
            )

        return data



    def get_metadata(self) -> dict:
        data = {
            "x_limits": self.surface_size,
            "y_limits": self.surface_size,
            "start_x": self.start_pos.x,
            "start_y": self.start_pos.y,
            "target_x": self.end_pos.x,
            "target_y": self.end_pos.y,
            "icebergs_count":self._number_of_polygons,
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

            # add the iceberg dictionary to the list of icebergs
            icebergs.append(iceberg_dict)

        data["icebergs"] = icebergs

        return data

    def _graham_scan(self,points) -> Polygon:
        p0 = min(points,key=lambda p:(p.y,p.x)) # get the point that have the lowest y value
        sorted_points = sorted(points,key=lambda p:(self._polar_angle(p0,p),distance(p0,p)))
        hull_points = []

        for i in range(len(sorted_points)):
            while len(hull_points) > 2 and not self._is_counter_clock_wise(hull_points[-2],hull_points[-1],sorted_points[i]):
                hull_points.pop()
            hull_points.append(sorted_points[i])

        polygon = Polygon(hull_points)
        return polygon



    @staticmethod
    def _polar_angle(point_a,point_b) -> float:
        angle_radians = math.atan2(point_b.y - point_a.y,point_b.x - point_a.x)
        return math.degrees(angle_radians)

    @staticmethod
    def _is_counter_clock_wise(a,b,c) -> bool:
        vector_v = b.x-a.x,b.y-a.y
        vector_w = c.x-a.x,c.y-a.y
        area = vector_v[0] * vector_w[1] - vector_v[1] * vector_w[0]

        if area >= 0:
            return True
        else:
            return False