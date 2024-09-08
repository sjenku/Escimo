from typing import Dict

from pydantic import BaseModel, RootModel

from Module.point_wrapper import PointWrapper


class IcebergPoints(RootModel[Dict[str, PointWrapper]]):
    pass