import numpy as np

class Battery:
    def __init__(self, capacity_kwh, charge_power_kw, discharge_power_kw, efficiency=0.95, exp_coeff=0.1, charge_exp_coeff=5.0):
        self.capacity_kwh = capacity_kwh
        self.charge_power_kw = charge_power_kw
        self.discharge_power_kw = discharge_power_kw
        self.efficiency = efficiency
        self.exp_coeff = exp_coeff
        self.charge_exp_coeff = charge_exp_coeff
        self.soc = 1.0

    def discharge_curve(self, soc):
        if soc > 0.8:
            return np.exp(-self.exp_coeff * (soc - 0.8))
        elif 0.2 < soc <= 0.8:
            return 1.0
        else:
            return soc / 0.2

    def charge_curve(self, soc):
        if soc < 0.8:
            return 1.0
        else:
            return np.exp(-self.charge_exp_coeff * (soc - 0.8))

    def charge(self, power_kw, time_h):
        if self.soc < 1.0:
            charge_factor = self.charge_curve(self.soc)
            power_kw = min(power_kw, self.charge_power_kw * charge_factor)
            energy_to_charge = power_kw * time_h * self.efficiency
            self.soc = min(self.soc + energy_to_charge / self.capacity_kwh, 1.0)
            return power_kw
        else:
            return 0.0

    def discharge(self, power_kw, time_h):
        power_kw = min(power_kw, self.discharge_power_kw)
        discharge_factor = self.discharge_curve(self.soc)
        effective_power = power_kw * discharge_factor
        energy_to_discharge = effective_power * time_h / self.efficiency
        self.soc = max(self.soc - energy_to_discharge / self.capacity_kwh, 0.0)
        return effective_power

    def get_soc(self):
        return self.soc

    def get_remaining_energy_kwh(self):
        return self.soc * self.capacity_kwh
