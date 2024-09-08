from pydantic import BaseModel, conint

from TaskSolution.Model.iceberg import Iceberg


class InputData(BaseModel):
    """
    InputData model responsible to hold the data that created by EngineEskimo
    """
    x_limits: conint(ge = 0)
    y_limits: conint(ge = 0)
    start_x: float
    start_y: float
    target_x: float
    target_y: float
    icebergs_count:conint(ge = 0)
    icebergs: list[Iceberg]


