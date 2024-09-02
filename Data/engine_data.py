from pydantic import BaseModel, conint
from Model.iceberg import Iceberg


class EngineData(BaseModel):
    x_limits: conint(ge = 0)
    y_limits: conint(ge = 0)
    start_x: float
    start_y: float
    target_x: float
    target_y: float
    icebergs_count:conint(ge = 0)
    icebergs: list[Iceberg]

