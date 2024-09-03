
from pydantic import BaseModel, conint, Field
from Model.polygon_wrapper import PolygonWrapper



class Iceberg(BaseModel):
    """
    an Iceberg model is holding the representation of a Polygon points with an unique number
    """
    iceberg_number: conint(ge = 0)
    iceberg_points: PolygonWrapper






    