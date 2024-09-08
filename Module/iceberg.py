from pydantic import BaseModel, conint

from Module.iceberg_points import IcebergPoints


class Iceberg(BaseModel):
    """
    an Iceberg model is holding the representation of a Polygon points with an unique number
    """
    iceberg_number: conint(ge = 0)
    iceberg_points: IcebergPoints



