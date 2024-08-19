from pydantic import BaseModel
from typing import List

class BatteryConfig(BaseModel):
    capacity_kwh: float
    charge_power_kw: float
    discharge_power_kw: float
    efficiency: float = 0.95
    exp_coeff: float = 0.1
    charge_exp_coeff: float = 5.0

class SimulationRequest(BaseModel):
    battery: BatteryConfig
    energy_consumption_profile: List[float]
    time_interval_minutes: int = 60
    peak_threshold_kw: float

class SimulationResponse(BaseModel):
    shaved_profile: List[float]
    soc_profile: List[float]
