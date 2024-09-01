from pydantic import BaseModel, conint
from shapely.geometry import Point as ShapelyPoint


class EnginePoint(BaseModel):
    x: conint(ge=0)
    y: conint(ge=0)



    def to_shapely_point(self) -> ShapelyPoint:
        return ShapelyPoint(self.x, self.y)