"""
Climate Scenario Manager
Handles climate stress scenario definitions and applications
"""

from config.settings import CLIMATE_SCENARIOS

class ClimateScenarioManager:
    """Manage climate stress scenarios for traffic simulation"""
    
    def __init__(self):
        """Initialize climate scenario manager"""
        self.scenarios = CLIMATE_SCENARIOS
    
    def get_scenario(self, scenario_name: str) -> dict:
        """
        Get climate scenario configuration
        
        Args:
            scenario_name: Name of the scenario (baseline, moderate, severe, extreme)
            
        Returns:
            Dictionary containing scenario parameters
        """
        if scenario_name not in self.scenarios:
            raise ValueError(f"Unknown scenario: {scenario_name}. Available: {list(self.scenarios.keys())}")
        
        return self.scenarios[scenario_name]
    
    def get_all_scenarios(self) -> dict:
        """Get all available climate scenarios"""
        return self.scenarios
    
    def get_scenario_names(self) -> list:
        """Get list of available scenario names"""
        return list(self.scenarios.keys())
    
    def apply_capacity_reduction(self, base_capacity: float, scenario_name: str) -> float:
        """
        Apply capacity reduction based on climate scenario
        
        Args:
            base_capacity: Base road capacity (vehicles/hour)
            scenario_name: Climate scenario name
            
        Returns:
            Adjusted capacity under climate stress
        """
        scenario = self.get_scenario(scenario_name)
        reduction = scenario["capacity_reduction"]
        return base_capacity * (1 - reduction)
    
    def apply_efficiency_loss(self, base_speed: float, scenario_name: str) -> float:
        """
        Apply efficiency loss to vehicle speeds
        
        Args:
            base_speed: Base vehicle speed (km/h)
            scenario_name: Climate scenario name
            
        Returns:
            Adjusted speed under climate stress
        """
        scenario = self.get_scenario(scenario_name)
        loss = scenario["efficiency_loss"]
        return base_speed * (1 - loss)
    
    def get_emission_factor(self, scenario_name: str) -> float:
        """
        Get emission multiplication factor for scenario
        
        Args:
            scenario_name: Climate scenario name
            
        Returns:
            Emission factor multiplier
        """
        scenario = self.get_scenario(scenario_name)
        return scenario["emission_factor"]
    
    def get_scenario_summary(self, scenario_name: str) -> str:
        """
        Get human-readable summary of scenario impacts
        
        Args:
            scenario_name: Climate scenario name
            
        Returns:
            String summary of scenario
        """
        scenario = self.get_scenario(scenario_name)
        
        summary = f"""
**{scenario['name']}**

- **Capacity Reduction**: {scenario['capacity_reduction']*100:.0f}%
- **Efficiency Loss**: {scenario['efficiency_loss']*100:.0f}%
- **Emission Factor**: {scenario['emission_factor']:.2f}x

"""
        
        if scenario_name == "baseline":
            summary += "No climate stress applied. Normal operating conditions."
        elif scenario_name == "moderate":
            summary += "Moderate climate impacts: reduced road capacity due to heat stress, minor efficiency losses."
        elif scenario_name == "severe":
            summary += "Severe climate impacts: significant capacity constraints, notable efficiency degradation."
        elif scenario_name == "extreme":
            summary += "Extreme climate impacts: major infrastructure stress, substantial performance degradation."
        
        return summary
    
    def compare_scenarios(self, base_value: float, metric_name: str = "capacity") -> dict:
        """
        Compare impact across all scenarios
        
        Args:
            base_value: Base value to compare
            metric_name: Name of the metric being compared
            
        Returns:
            Dictionary with scenario comparisons
        """
        comparisons = {}
        
        for scenario_name, scenario in self.scenarios.items():
            if metric_name == "capacity":
                adjusted = base_value * (1 - scenario["capacity_reduction"])
            elif metric_name == "speed":
                adjusted = base_value * (1 - scenario["efficiency_loss"])
            elif metric_name == "emissions":
                adjusted = base_value * scenario["emission_factor"]
            else:
                adjusted = base_value
            
            comparisons[scenario_name] = {
                "base_value": base_value,
                "adjusted_value": adjusted,
                "change": adjusted - base_value,
                "percent_change": ((adjusted - base_value) / base_value * 100) if base_value != 0 else 0
            }
        
        return comparisons