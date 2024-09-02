
from pydantic import BaseModel, conint, Field
from Model.polygon_wrapper import PolygonWrapper



class Iceberg(BaseModel):
    iceberg_number: conint(ge = 0)
    iceberg_points: PolygonWrapper






    