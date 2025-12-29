"""
Statistical Analysis Module
Performs advanced statistical analysis and hypothesis testing
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple

class StatisticalAnalyzer:
    """Advanced statistical analysis for simulation results"""
    
    def __init__(self):
        """Initialize analyzer"""
        self.confidence_level = 0.95
    
    def perform_anova(self, results: Dict[str, Dict[str, Dict]]) -> Dict:
        """
        Perform ANOVA to test if policies have significantly different performance
        
        Args:
            results: Nested dict {policy: {scenario: {metrics}}}
            
        Returns:
            ANOVA results dictionary
        """
        anova_results = {}
        
        # For each metric
        metrics_list = ['average_delay', 'throughput', 'co2_emissions', 'average_speed']
        
        for metric in metrics_list:
            # Collect data for each policy
            policy_data = []
            policy_names = []
            
            for policy_name, scenarios in results.items():
                values = [scenario_data['metrics'].get(metric, 0) 
                         for scenario_data in scenarios.values()]
                policy_data.append(values)
                policy_names.append(policy_name)
            
            # Perform ANOVA
            if len(policy_data) > 1 and all(len(data) > 0 for data in policy_data):
                f_stat, p_value = stats.f_oneway(*policy_data)
                
                anova_results[metric] = {
                    'f_statistic': f_stat,
                    'p_value': p_value,
                    'significant': p_value < (1 - self.confidence_level),
                    'interpretation': self._interpret_anova(p_value)
                }
        
        return anova_results
    
    def _interpret_anova(self, p_value: float) -> str:
        """Interpret ANOVA results"""
        if p_value < 0.001:
            return "Highly significant difference between policies (p < 0.001)"
        elif p_value < 0.01:
            return "Very significant difference between policies (p < 0.01)"
        elif p_value < 0.05:
            return "Significant difference between policies (p < 0.05)"
        else:
            return "No significant difference between policies (p >= 0.05)"
    
    def calculate_confidence_intervals(self, 
                                      results: Dict[str, Dict[str, Dict]],
                                      confidence: float = 0.95) -> Dict:
        """
        Calculate confidence intervals for each policy metric
        
        Args:
            results: Simulation results
            confidence: Confidence level (default 95%)
            
        Returns:
            Dictionary of confidence intervals
        """
        ci_results = {}
        
        for policy_name, scenarios in results.items():
            ci_results[policy_name] = {}
            
            # Collect metrics across scenarios
            metrics_data = {}
            for scenario_name, data in scenarios.items():
                for metric, value in data['metrics'].items():
                    if metric not in metrics_data:
                        metrics_data[metric] = []
                    metrics_data[metric].append(value)
            
            # Calculate CI for each metric
            for metric, values in metrics_data.items():
                if len(values) > 1:
                    mean = np.mean(values)
                    std_err = stats.sem(values)
                    ci = stats.t.interval(confidence, len(values)-1, mean, std_err)
                    
                    ci_results[policy_name][metric] = {
                        'mean': mean,
                        'lower': ci[0],
                        'upper': ci[1],
                        'margin_of_error': (ci[1] - ci[0]) / 2
                    }
        
        return ci_results
    
    def perform_sensitivity_analysis(self,
                                    base_metrics: Dict,
                                    parameter_variations: Dict[str, List[float]]) -> pd.DataFrame:
        """
        Perform sensitivity analysis on policy parameters
        
        Args:
            base_metrics: Baseline performance metrics
            parameter_variations: Dict of {parameter: [variation_factors]}
            
        Returns:
            DataFrame with sensitivity results
        """
        sensitivity_data = []
        
        for param, factors in parameter_variations.items():
            for factor in factors:
                # Simulate parameter change impact
                varied_metrics = self._apply_parameter_variation(base_metrics, param, factor)
                
                sensitivity_data.append({
                    'parameter': param,
                    'variation_factor': factor,
                    'delay_change': ((varied_metrics['average_delay'] - base_metrics['average_delay']) / 
                                   base_metrics['average_delay'] * 100),
                    'throughput_change': ((varied_metrics['throughput'] - base_metrics['throughput']) / 
                                         base_metrics['throughput'] * 100),
                    'emissions_change': ((varied_metrics['co2_emissions'] - base_metrics['co2_emissions']) / 
                                        base_metrics['co2_emissions'] * 100)
                })
        
        return pd.DataFrame(sensitivity_data)
    
    def _apply_parameter_variation(self, base_metrics: Dict, parameter: str, factor: float) -> Dict:
        """Apply parameter variation to metrics (simplified model)"""
        varied_metrics = base_metrics.copy()
        
        # Simplified sensitivity model
        if 'signal' in parameter.lower() or 'timing' in parameter.lower():
            varied_metrics['average_delay'] *= (1 + (factor - 1) * 0.5)
            varied_metrics['throughput'] *= (1 - (factor - 1) * 0.3)
        elif 'speed' in parameter.lower():
            varied_metrics['average_speed'] *= factor
            varied_metrics['co2_emissions'] *= (1 + (factor - 1) * 0.4)
        elif 'capacity' in parameter.lower():
            varied_metrics['throughput'] *= factor
            varied_metrics['average_delay'] *= (1 / factor)
        
        return varied_metrics
    
    def calculate_correlation_matrix(self, results: Dict[str, Dict[str, Dict]]) -> pd.DataFrame:
        """
        Calculate correlation matrix between performance metrics
        
        Args:
            results: Simulation results
            
        Returns:
            Correlation matrix as DataFrame
        """
        # Collect all metrics
        all_data = []
        
        for policy_name, scenarios in results.items():
            for scenario_name, data in scenarios.items():
                all_data.append(data['metrics'])
        
        df = pd.DataFrame(all_data)
        
        # Select numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        # Calculate correlation
        correlation_matrix = df[numeric_cols].corr()
        
        return correlation_matrix
    
    def generate_statistical_report(self, 
                                    results: Dict[str, Dict[str, Dict]],
                                    anova_results: Dict = None) -> str:
        """
        Generate comprehensive statistical analysis report
        
        Args:
            results: Simulation results
            anova_results: Optional pre-computed ANOVA results
            
        Returns:
            Formatted report string
        """
        report = "# Statistical Analysis Report\n\n"
        
        # ANOVA Results
        if anova_results is None:
            anova_results = self.perform_anova(results)
        
        report += "## Analysis of Variance (ANOVA)\n\n"
        report += "Testing if policies have significantly different performance:\n\n"
        
        for metric, anova in anova_results.items():
            report += f"### {metric.replace('_', ' ').title()}\n"
            report += f"- **F-statistic:** {anova['f_statistic']:.3f}\n"
            report += f"- **P-value:** {anova['p_value']:.4f}\n"
            report += f"- **Result:** {anova['interpretation']}\n\n"
        
        # Confidence Intervals
        ci_results = self.calculate_confidence_intervals(results)
        
        report += "## Confidence Intervals (95%)\n\n"
        for policy_name, metrics in ci_results.items():
            report += f"### {policy_name}\n"
            for metric, ci in metrics.items():
                report += f"- **{metric}:** {ci['mean']:.2f} "
                report += f"[{ci['lower']:.2f}, {ci['upper']:.2f}] "
                report += f"(±{ci['margin_of_error']:.2f})\n"
            report += "\n"
        
        # Correlation Analysis
        corr_matrix = self.calculate_correlation_matrix(results)
        
        report += "## Metric Correlations\n\n"
        report += "Strong correlations (|r| > 0.7):\n\n"
        
        for i in range(len(corr_matrix)):
            for j in range(i+1, len(corr_matrix)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:
                    metric1 = corr_matrix.index[i]
                    metric2 = corr_matrix.columns[j]
                    report += f"- **{metric1}** ↔ **{metric2}:** r = {corr_value:.3f}\n"
        
        return report