from pydantic import BaseModel, validator, field_validator
from shapely import Point


class Edge(BaseModel):
    point1 : Point
    point2 : Point

    @field_validator("point1","point2")
    def validate_points(cls, value):
        if value.x <= 0 or value.y <= 0:
            raise ValueError("Both x and y coordinates must be greater than 0.")
        return value

    def length(self):
        return self.point1.distance(self.point2)

    class Config:
        arbitrary_types_allowed = True # use this to support the Point from shapely



