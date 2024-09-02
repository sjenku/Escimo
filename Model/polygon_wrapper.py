from typing import Tuple

from pydantic import BaseModel, validator
from shapely import Polygon

class PolygonWrapper(BaseModel):
    coordinates: list[list[Tuple[float, float]]]

    class Config:
        json_encoders = {
            list[list[Tuple[float, float]]]: lambda p: flatten_coordinates(p)  # Example encoder
        }

    def to_polygon(self) -> Polygon:
        if not self.coordinates:
            raise ValueError("No coordinates to create Polygon")
        # Create the Polygon object from the coordinates
        return Polygon(self.coordinates[0])

    @classmethod
    def from_polygon(cls, polygon: Polygon) -> "PolygonWrapper":
        # Convert Polygon to coordinates list and create a PolygonWrapper instance
        coordinates = [list(polygon.exterior.coords)]
        return cls(coordinates=coordinates)


def flatten_coordinates(polygon_wrapper: PolygonWrapper) -> dict:
    """
        Helper function to flatten coordinates into a custom JSON structure.
    """
    print("flatten_coordinates")
    custom_json = {}
    point_counter = 1
    for pol in polygon_wrapper.coordinates:
        for coord in pol:
            key = f'point{point_counter}'
            custom_json[key] = {'x': coord[0], 'y': coord[1]}
            point_counter += 1
    return custom_json