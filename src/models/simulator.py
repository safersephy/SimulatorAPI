class PeakShavingSimulator:
    def __init__(self, battery, energy_consumption_profile, time_interval_minutes=60):
        self.battery = battery
        self.energy_consumption_profile = energy_consumption_profile
        self.time_interval_h = time_interval_minutes / 60.0
        self.shaved_profile = []
        self.soc_profile = []

    def simulate(self, peak_threshold_kw):
        for demand in self.energy_consumption_profile:
            if demand > peak_threshold_kw:
                excess_power = demand - peak_threshold_kw
                available_power = self.battery.discharge(excess_power, self.time_interval_h)
                shaved_demand = demand - available_power
                if shaved_demand < peak_threshold_kw:
                    shaved_demand = peak_threshold_kw
            else:
                if self.battery.get_soc() < 1.0:
                    available_power = peak_threshold_kw - demand
                    charging_power = self.battery.charge(available_power, self.time_interval_h)
                    shaved_demand = demand + charging_power
                else:
                    shaved_demand = demand
            self.shaved_profile.append(shaved_demand)
            self.soc_profile.append(self.battery.get_soc())
