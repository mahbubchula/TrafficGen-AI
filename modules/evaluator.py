"""
Performance Evaluator
Calculates and analyzes traffic performance metrics from simulation results
"""

import pandas as pd
import numpy as np
from config.settings import METRICS

class PerformanceEvaluator:
    """Evaluate traffic simulation performance metrics"""
    
    def __init__(self):
        """Initialize performance evaluator"""
        self.metrics = METRICS
    
    def calculate_metrics(self, simulation_data: dict) -> dict:
        """
        Calculate performance metrics from simulation data
        
        Args:
            simulation_data: Dictionary containing simulation results
            
        Returns:
            Dictionary of calculated metrics
        """
        metrics = {}
        
        # Extract basic data
        vehicles = simulation_data.get('vehicles', [])
        total_time = simulation_data.get('simulation_time', 3600)
        
        if not vehicles:
            return self._get_empty_metrics()
        
        # Convert to DataFrame for easier processing
        df = pd.DataFrame(vehicles)
        
        # Average Delay (seconds)
        if 'delay' in df.columns:
            metrics['average_delay'] = df['delay'].mean()
        else:
            metrics['average_delay'] = 0.0
        
        # Throughput (vehicles/hour)
        completed_vehicles = len(df[df.get('completed', True)])
        metrics['throughput'] = (completed_vehicles / total_time) * 3600
        
        # CO2 Emissions (kg)
        if 'co2_emissions' in df.columns:
            metrics['co2_emissions'] = df['co2_emissions'].sum() / 1000  # Convert g to kg
        else:
            # Estimate based on travel time if not available
            # Average CO2: ~120g/km for typical vehicle
            if 'distance' in df.columns:
                total_distance = df['distance'].sum() / 1000  # Convert m to km
                metrics['co2_emissions'] = total_distance * 0.12  # kg
            else:
                metrics['co2_emissions'] = 0.0
        
        # Average Speed (km/h)
        if 'speed' in df.columns:
            metrics['average_speed'] = df['speed'].mean() * 3.6  # Convert m/s to km/h
        else:
            metrics['average_speed'] = 0.0
        
        # Total Travel Time (hours)
        if 'travel_time' in df.columns:
            metrics['total_travel_time'] = df['travel_time'].sum() / 3600  # Convert seconds to hours
        else:
            metrics['total_travel_time'] = 0.0
        
        return metrics
    
    def _get_empty_metrics(self) -> dict:
        """Return empty metrics structure"""
        return {
            'average_delay': 0.0,
            'throughput': 0.0,
            'co2_emissions': 0.0,
            'average_speed': 0.0,
            'total_travel_time': 0.0
        }
    
    def compare_policies(self, baseline_metrics: dict, policy_metrics: dict) -> dict:
        """
        Compare policy performance against baseline
        
        Args:
            baseline_metrics: Baseline scenario metrics
            policy_metrics: Policy scenario metrics
            
        Returns:
            Dictionary with comparison results
        """
        comparison = {}
        
        for metric_key in baseline_metrics.keys():
            baseline_value = baseline_metrics[metric_key]
            policy_value = policy_metrics[metric_key]
            
            # Calculate absolute and percentage change
            absolute_change = policy_value - baseline_value
            
            if baseline_value != 0:
                percent_change = (absolute_change / baseline_value) * 100
            else:
                percent_change = 0.0 if policy_value == 0 else 100.0
            
            # Determine if improvement (depends on metric)
            is_improvement = self._is_improvement(metric_key, absolute_change)
            
            comparison[metric_key] = {
                'baseline': baseline_value,
                'policy': policy_value,
                'absolute_change': absolute_change,
                'percent_change': percent_change,
                'is_improvement': is_improvement
            }
        
        return comparison
    
    def _is_improvement(self, metric_key: str, change: float) -> bool:
        """
        Determine if a change represents improvement
        
        Args:
            metric_key: Name of the metric
            change: Change value (policy - baseline)
            
        Returns:
            True if improvement, False otherwise
        """
        # Lower is better for these metrics
        lower_is_better = ['average_delay', 'co2_emissions', 'total_travel_time']
        
        # Higher is better for these metrics
        higher_is_better = ['throughput', 'average_speed']
        
        if metric_key in lower_is_better:
            return change < 0
        elif metric_key in higher_is_better:
            return change > 0
        else:
            return False
    
    def calculate_composite_score(self, metrics: dict, weights: dict = None) -> float:
        """
        Calculate weighted composite performance score
        
        Args:
            metrics: Performance metrics dictionary
            weights: Optional custom weights for each metric
            
        Returns:
            Composite score (0-100, higher is better)
        """
        if weights is None:
            # Default equal weights
            weights = {
                'average_delay': 0.25,
                'throughput': 0.25,
                'co2_emissions': 0.25,
                'average_speed': 0.25
            }
        
        # Normalize metrics to 0-100 scale (assuming reasonable ranges)
        normalized = {}
        
        # Average delay: 0-300 seconds (lower is better)
        delay = min(max(metrics.get('average_delay', 150), 0), 300)
        normalized['average_delay'] = (300 - delay) / 300 * 100
        
        # Throughput: 0-2000 vehicles/hour (higher is better)
        throughput = min(max(metrics.get('throughput', 0), 0), 2000)
        normalized['throughput'] = throughput / 2000 * 100
        
        # CO2 emissions: 0-1000 kg (lower is better)
        emissions = min(max(metrics.get('co2_emissions', 500), 0), 1000)
        normalized['co2_emissions'] = (1000 - emissions) / 1000 * 100
        
        # Average speed: 0-60 km/h (higher is better)
        speed = min(max(metrics.get('average_speed', 0), 0), 60)
        normalized['average_speed'] = speed / 60 * 100
        
        # Calculate weighted score
        score = sum(normalized.get(key, 0) * weight for key, weight in weights.items())
        
        return round(score, 2)
    
    def generate_summary_table(self, results_dict: dict) -> pd.DataFrame:
        """
        Generate summary table from multiple simulation results
        
        Args:
            results_dict: Dictionary of {scenario_name: metrics}
            
        Returns:
            Pandas DataFrame with formatted results
        """
        summary_data = []
        
        for scenario_name, metrics in results_dict.items():
            row = {
                'Scenario': scenario_name,
                'Avg Delay (s)': f"{metrics.get('average_delay', 0):.1f}",
                'Throughput (veh/h)': f"{metrics.get('throughput', 0):.0f}",
                'CO₂ (kg)': f"{metrics.get('co2_emissions', 0):.2f}",
                'Avg Speed (km/h)': f"{metrics.get('average_speed', 0):.1f}",
                'Total Travel Time (h)': f"{metrics.get('total_travel_time', 0):.2f}",
                'Score': f"{self.calculate_composite_score(metrics):.1f}"
            }
            summary_data.append(row)
        
        return pd.DataFrame(summary_data)
    
    def identify_best_policy(self, results_dict: dict, objective: str = 'composite') -> str:
        """
        Identify best performing policy based on objective
        
        Args:
            results_dict: Dictionary of {policy_name: metrics}
            objective: Optimization objective ('composite', 'delay', 'emissions', etc.)
            
        Returns:
            Name of best performing policy
        """
        if not results_dict:
            return None
        
        if objective == 'composite':
            scores = {name: self.calculate_composite_score(metrics) 
                     for name, metrics in results_dict.items()}
            return max(scores, key=scores.get)
        
        # For specific metrics
        metric_map = {
            'delay': 'average_delay',
            'emissions': 'co2_emissions',
            'throughput': 'throughput',
            'speed': 'average_speed'
        }
        
        metric_key = metric_map.get(objective, 'average_delay')
        is_lower_better = metric_key in ['average_delay', 'co2_emissions', 'total_travel_time']
        
        values = {name: metrics.get(metric_key, float('inf') if is_lower_better else 0) 
                 for name, metrics in results_dict.items()}
        
        if is_lower_better:
            return min(values, key=values.get)
        else:
            return max(values, key=values.get)