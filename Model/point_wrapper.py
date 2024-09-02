from pydantic import BaseModel
from shapely import Point

# use this class to support Point class with pydantic
class PointWrapper(BaseModel):
    x: float
    y: float

    @classmethod
    def from_point(cls, point: Point) -> 'PointWrapper':
        return cls(x=point.x, y=point.y)

    def point(self) -> Point:
        return Point(self.x, self.y)