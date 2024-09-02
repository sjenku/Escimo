from pydantic import conint, BaseModel
from Model.point_wrapper import PointWrapper
from Model.range import Range


class Configurations(BaseModel):

    start_position:PointWrapper
    end_position:PointWrapper
    number_of_polygons_range: Range
    number_of_points_in_polygon_range: Range
    polygon_radius_range : Range
    surface_size : conint(ge = 0)

