from pydantic import BaseModel, conint, Field
import random

class Range(BaseModel):
    from_: conint(ge=0) = Field(..., alias='from')  # Minimum value, must be >= 0
    to: conint(ge=0)      # Maximum value, must be >= 0

    def get_random_number_in_range(self) -> int:
        return random.randint(self.from_, self.to)
