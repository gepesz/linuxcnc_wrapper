from pydantic import BaseModel

class MachineStatus(BaseModel):
    x_position: float
    y_position: float
    z_position: float
    is_running: bool
    error_code: int = 0
    message: str = "No errors"
