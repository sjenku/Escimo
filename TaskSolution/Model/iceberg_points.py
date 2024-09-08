from pydantic import BaseModel

from TaskSolution.Model.coords import Coords


class IcebergPoints(BaseModel):
    coords: Coords