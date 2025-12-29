"""
Multi-Objective Optimization Module
Performs Pareto frontier analysis and optimization
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple

class MultiObjectiveOptimizer:
    """Advanced multi-objective optimization for policy evaluation"""
    
    def __init__(self):
        """Initialize optimizer"""
        self.objectives = ['average_delay', 'co2_emissions', 'throughput', 'average_speed']
        self.minimize_objectives = ['average_delay', 'co2_emissions']
        self.maximize_objectives = ['throughput', 'average_speed']
    
    def calculate_pareto_frontier(self, policies_metrics: Dict[str, Dict]) -> List[str]:
        """
        Calculate Pareto frontier - identify non-dominated solutions
        
        Args:
            policies_metrics: Dictionary of {policy_name: metrics_dict}
            
        Returns:
            List of policy names on the Pareto frontier
        """
        policy_names = list(policies_metrics.keys())
        n_policies = len(policy_names)
        
        # Create objective matrix
        objective_matrix = []
        for policy_name in policy_names:
            metrics = policies_metrics[policy_name]
            obj_values = []
            
            for obj in self.objectives:
                value = metrics.get(obj, 0)
                # Negate maximization objectives for consistent comparison
                if obj in self.maximize_objectives:
                    value = -value
                obj_values.append(value)
            
            objective_matrix.append(obj_values)
        
        objective_matrix = np.array(objective_matrix)
        
        # Find Pareto frontier
        pareto_front = []
        
        for i in range(n_policies):
            is_dominated = False
            
            for j in range(n_policies):
                if i != j:
                    # Check if solution i is dominated by solution j
                    if self._dominates(objective_matrix[j], objective_matrix[i]):
                        is_dominated = True
                        break
            
            if not is_dominated:
                pareto_front.append(policy_names[i])
        
        return pareto_front
    
    def _dominates(self, solution_a: np.ndarray, solution_b: np.ndarray) -> bool:
        """Check if solution A dominates solution B"""
        return np.all(solution_a <= solution_b) and np.any(solution_a < solution_b)
    
    def calculate_hypervolume(self, policies_metrics: Dict[str, Dict], reference_point: List[float] = None) -> float:
        """
        Calculate hypervolume indicator (quality of Pareto front)
        
        Args:
            policies_metrics: Dictionary of policy metrics
            reference_point: Reference point for hypervolume calculation
            
        Returns:
            Hypervolume value
        """
        if reference_point is None:
            # Use worst values as reference
            reference_point = []
            for obj in self.objectives:
                values = [m.get(obj, 0) for m in policies_metrics.values()]
                if obj in self.minimize_objectives:
                    reference_point.append(max(values) * 1.1)
                else:
                    reference_point.append(min(values) * 0.9)
        
        # Simplified hypervolume calculation
        pareto_policies = self.calculate_pareto_frontier(policies_metrics)
        
        if not pareto_policies:
            return 0.0
        
        # Normalize objectives
        normalized_volume = len(pareto_policies) / len(policies_metrics)
        
        return normalized_volume
    
    def rank_policies_by_dominance(self, policies_metrics: Dict[str, Dict]) -> Dict[str, int]:
        """
        Rank policies by dominance count
        
        Args:
            policies_metrics: Dictionary of policy metrics
            
        Returns:
            Dictionary of {policy_name: rank}
        """
        policy_names = list(policies_metrics.keys())
        dominance_count = {name: 0 for name in policy_names}
        
        # Create objective matrix
        objective_matrix = {}
        for policy_name in policy_names:
            metrics = policies_metrics[policy_name]
            obj_values = []
            
            for obj in self.objectives:
                value = metrics.get(obj, 0)
                if obj in self.maximize_objectives:
                    value = -value
                obj_values.append(value)
            
            objective_matrix[policy_name] = np.array(obj_values)
        
        # Count how many solutions dominate each solution
        for name_a in policy_names:
            for name_b in policy_names:
                if name_a != name_b:
                    if self._dominates(objective_matrix[name_b], objective_matrix[name_a]):
                        dominance_count[name_a] += 1
        
        # Convert to ranks (0 = best)
        ranks = {}
        sorted_policies = sorted(dominance_count.items(), key=lambda x: x[1])
        
        current_rank = 1
        for i, (policy, count) in enumerate(sorted_policies):
            if i > 0 and count > sorted_policies[i-1][1]:
                current_rank = i + 1
            ranks[policy] = current_rank
        
        return ranks
    
    def calculate_weighted_score(self, 
                                 metrics: Dict,
                                 weights: Dict[str, float] = None) -> float:
        """
        Calculate weighted aggregate score
        
        Args:
            metrics: Performance metrics
            weights: Custom weights for each objective
            
        Returns:
            Weighted score (0-100)
        """
        if weights is None:
            # Equal weights
            weights = {obj: 1.0/len(self.objectives) for obj in self.objectives}
        
        # Normalize and aggregate
        score = 0.0
        
        for obj in self.objectives:
            value = metrics.get(obj, 0)
            weight = weights.get(obj, 0)
            
            # Normalize to 0-100 scale
            if obj == 'average_delay':
                normalized = max(0, 100 - (value / 3))
            elif obj == 'throughput':
                normalized = min(100, (value / 20))
            elif obj == 'co2_emissions':
                normalized = max(0, 100 - (value / 10))
            elif obj == 'average_speed':
                normalized = min(100, (value / 0.6))
            else:
                normalized = 50
            
            score += normalized * weight
        
        return min(100, max(0, score))
    
    def generate_optimization_report(self, policies_metrics: Dict[str, Dict]) -> str:
        """
        Generate comprehensive optimization report
        
        Args:
            policies_metrics: Dictionary of policy metrics
            
        Returns:
            Formatted report string
        """
        pareto_front = self.calculate_pareto_frontier(policies_metrics)
        ranks = self.rank_policies_by_dominance(policies_metrics)
        hypervolume = self.calculate_hypervolume(policies_metrics)
        
        report = "# Multi-Objective Optimization Report\n\n"
        
        report += f"## Summary\n"
        report += f"- **Total Policies Evaluated:** {len(policies_metrics)}\n"
        report += f"- **Pareto Optimal Policies:** {len(pareto_front)}\n"
        report += f"- **Solution Quality (Hypervolume):** {hypervolume:.3f}\n\n"
        
        report += f"## Pareto Frontier\n"
        report += "These policies are non-dominated (cannot improve one objective without worsening another):\n\n"
        
        for i, policy in enumerate(pareto_front, 1):
            metrics = policies_metrics[policy]
            report += f"{i}. **{policy}**\n"
            report += f"   - Delay: {metrics.get('average_delay', 0):.1f}s\n"
            report += f"   - Throughput: {metrics.get('throughput', 0):.0f} veh/h\n"
            report += f"   - CO₂: {metrics.get('co2_emissions', 0):.2f} kg\n"
            report += f"   - Speed: {metrics.get('average_speed', 0):.1f} km/h\n\n"
        
        report += f"## Policy Rankings\n"
        report += "Ranked by dominance (lower rank = better):\n\n"
        
        sorted_ranks = sorted(ranks.items(), key=lambda x: x[1])
        for policy, rank in sorted_ranks[:5]:  # Top 5
            report += f"- **Rank {rank}:** {policy}\n"
        
        return report