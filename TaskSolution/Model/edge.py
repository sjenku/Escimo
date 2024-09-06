from pydantic import BaseModel, validator, field_validator
from shapely import Point, LineString


class Edge(BaseModel):
    point1 : Point
    point2 : Point

    class Config:
        arbitrary_types_allowed = True

    @field_validator("point1","point2")
    def validate_points(cls, value):
        if value.x < 0 or value.y < 0:
            raise ValueError("Both x and y coordinates must be greater than 0.")
        return value

    def length(self):
        return self.point1.distance(self.point2)

    def to_linestring(self):
        return LineString([self.point1, self.point2])

    def is_in_polygon(self,polygon):
        return polygon.contains(self.to_linestring()) or self.to_linestring().crosses(polygon) or self.to_linestring().overlaps(polygon)




