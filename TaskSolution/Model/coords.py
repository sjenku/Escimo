from typing import Dict
from pydantic import BaseModel, RootModel

from Module.point_wrapper import PointWrapper


class Coords(RootModel[Dict[str, PointWrapper]]):
    pass