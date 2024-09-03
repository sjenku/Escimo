from typing import Tuple
from pydantic import BaseModel, validator, field_serializer
from shapely import Polygon


class PolygonWrapper(BaseModel):
    """
    a wrapper model for Polygon object from shapely package, used for
    support pydantic in another classes
    """
    coords: list[list[Tuple[float, float]]]

    @field_serializer("coords")
    def serialize_coords(self,value):
        custom_json = {}
        point_counter = 1
        for pol in value:
            for coord in pol:
                key = f'point{point_counter}'
                custom_json[key] = {'x': coord[0], 'y': coord[1]}
                point_counter += 1
        return custom_json

    def to_polygon(self) -> Polygon:
        if not self.coords:
            raise ValueError("No coordinates to create Polygon")
        # create the Polygon object from the coordinates
        return Polygon(self.coords[0])

    @classmethod
    def from_polygon(cls, polygon: Polygon) -> "PolygonWrapper":
        # convert Polygon to coordinates list and create a PolygonWrapper instance
        coords = [list(polygon.exterior.coords)]
        return cls(coords=coords)
