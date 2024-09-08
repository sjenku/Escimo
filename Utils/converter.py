from shapely import Polygon

from Module.iceberg import Iceberg


class Converter:

    @classmethod
    def to_polygon(cls,iceberg:Iceberg) -> Polygon:
        coords = []
        coords_dict = iceberg.iceberg_points.root
        for _,point_wrapper in coords_dict.items():
            coords.append(point_wrapper.point())
        polygon = Polygon(coords)
        return polygon