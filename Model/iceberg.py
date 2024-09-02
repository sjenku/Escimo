
from pydantic import BaseModel, conint, Field
from Model.polygon_wrapper import PolygonWrapper



class Iceberg(BaseModel):
    iceberg_number: conint(ge = 0)
    polygon: PolygonWrapper = Field(..., alias='iceberg_points')





    