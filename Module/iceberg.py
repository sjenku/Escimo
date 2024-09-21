from pydantic import BaseModel, conint
from shapely import Polygon

from Module.iceberg_points import IcebergPoints


class Iceberg(BaseModel):
    """
    an Iceberg model is holding the representation of a Polygon points with an unique number
    """
    iceberg_number: conint(ge = 0)
    iceberg_points: IcebergPoints


    def to_polygon(self) -> Polygon:
        coords = []
        coords_dict = self.iceberg_points.root
        for _,point_wrapper in coords_dict.items():
            coords.append(point_wrapper.point())
        polygon = Polygon(coords)
        return polygon




