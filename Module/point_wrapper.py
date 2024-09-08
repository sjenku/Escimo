from pydantic import BaseModel
from shapely import Point

class PointWrapper(BaseModel):
    """
       a wrapper model for Point object from shapely package, used for
       support pydantic in another classes
       """
    x: float
    y: float

    @classmethod
    def from_point(cls, point: Point) -> 'PointWrapper':
        return cls(x=point.x, y=point.y)

    def point(self) -> Point:
        return Point(self.x, self.y)