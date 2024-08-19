from fastapi import APIRouter, HTTPException
from src.schemas.simulation import SimulationRequest, SimulationResponse
from src.models.simulator import PeakShavingSimulator
from src.models.battery import Battery

router = APIRouter()

@router.post("/simulate", response_model=SimulationResponse)
def simulate(request: SimulationRequest):
    try:
        # Initialize battery
        battery = Battery(
            capacity_kwh=request.battery.capacity_kwh,
            charge_power_kw=request.battery.charge_power_kw,
            discharge_power_kw=request.battery.discharge_power_kw,
            efficiency=request.battery.efficiency,
            exp_coeff=request.battery.exp_coeff,
            charge_exp_coeff=request.battery.charge_exp_coeff
        )
        
        # Initialize simulator
        simulator = PeakShavingSimulator(
            battery=battery,
            energy_consumption_profile=request.energy_consumption_profile,
            time_interval_minutes=request.time_interval_minutes
        )
        
        # Run simulation
        simulator.simulate(request.peak_threshold_kw)
        
        return SimulationResponse(
            shaved_profile=simulator.shaved_profile,
            soc_profile=simulator.soc_profile
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
