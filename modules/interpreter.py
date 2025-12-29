"""
Result Interpreter
Uses LLM to provide human-readable interpretations of simulation results
"""

import json
from groq import Groq
from config.settings import GROQ_API_KEY, GROQ_MODEL
from config.prompts import INTERPRETATION_PROMPT, POLICY_COMPARISON_PROMPT

class ResultInterpreter:
    """Generate interpretations of simulation results using LLM"""
    
    def __init__(self, api_key=None):
        """
        Initialize the result interpreter
        
        Args:
            api_key: Groq API key (optional, defaults to config)
        """
        self.api_key = api_key or GROQ_API_KEY
        if not self.api_key:
            raise ValueError("Groq API key not found. Please set GROQ_API_KEY in .env file")
        
        self.client = Groq(api_key=self.api_key)
        self.model = GROQ_MODEL
    
    def interpret_results(self, 
                         policy_config: dict,
                         metrics: dict,
                         climate_scenario: str,
                         baseline_metrics: dict = None) -> str:
        """
        Generate interpretation of simulation results
        
        Args:
            policy_config: Policy configuration used
            metrics: Performance metrics from simulation
            climate_scenario: Climate scenario name
            baseline_metrics: Optional baseline metrics for comparison
            
        Returns:
            String containing interpretation
        """
        
        # Prepare results summary
        results_summary = self._format_results_summary(metrics, baseline_metrics)
        
        # Prepare policy configuration summary
        policy_summary = self._format_policy_summary(policy_config)
        
        # Format the prompt
        prompt = INTERPRETATION_PROMPT.format(
            results_summary=results_summary,
            policy_config=policy_summary,
            climate_scenario=climate_scenario
        )
        
        try:
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a traffic engineering analyst providing clear, evidence-based interpretations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
                max_tokens=1500
            )
            
            # Extract interpretation
            interpretation = response.choices[0].message.content.strip()
            
            return interpretation
            
        except Exception as e:
            return f"Error generating interpretation: {e}"
    
    def compare_multiple_policies(self,
                                  policies_results: dict,
                                  climate_scenarios: list) -> str:
        """
        Generate comparative analysis of multiple policies
        
        Args:
            policies_results: Dict of {policy_name: {scenario: metrics}}
            climate_scenarios: List of scenario names evaluated
            
        Returns:
            String containing comparative analysis
        """
        
        # Format policies summary
        policies_summary = self._format_multiple_policies(policies_results)
        
        # Format performance data
        performance_data = self._format_performance_comparison(policies_results, climate_scenarios)
        
        # Format the prompt
        prompt = POLICY_COMPARISON_PROMPT.format(
            policies_summary=policies_summary,
            performance_data=performance_data
        )
        
        try:
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a traffic engineering analyst comparing policy alternatives."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
                max_tokens=2000
            )
            
            # Extract interpretation
            interpretation = response.choices[0].message.content.strip()
            
            return interpretation
            
        except Exception as e:
            return f"Error generating comparison: {e}"
    
    def _format_results_summary(self, metrics: dict, baseline_metrics: dict = None) -> str:
        """Format metrics into readable summary"""
        summary = "**Performance Metrics:**\n"
        
        for key, value in metrics.items():
            metric_name = key.replace('_', ' ').title()
            
            if isinstance(value, float):
                summary += f"- {metric_name}: {value:.2f}\n"
            else:
                summary += f"- {metric_name}: {value}\n"
        
        if baseline_metrics:
            summary += "\n**Comparison to Baseline:**\n"
            for key in metrics.keys():
                if key in baseline_metrics:
                    change = metrics[key] - baseline_metrics[key]
                    percent_change = (change / baseline_metrics[key] * 100) if baseline_metrics[key] != 0 else 0
                    metric_name = key.replace('_', ' ').title()
                    summary += f"- {metric_name}: {change:+.2f} ({percent_change:+.1f}%)\n"
        
        return summary
    
    def _format_policy_summary(self, policy_config: dict) -> str:
        """Format policy configuration into readable summary"""
        summary = f"**Policy Name:** {policy_config.get('policy_name', 'Unknown')}\n"
        summary += f"**Policy Type:** {policy_config.get('policy_type', 'Unknown')}\n"
        summary += f"**Description:** {policy_config.get('description', 'No description')}\n\n"
        
        if 'parameters' in policy_config:
            summary += "**Parameters:**\n"
            for key, value in policy_config['parameters'].items():
                param_name = key.replace('_', ' ').title()
                summary += f"- {param_name}: {value}\n"
        
        return summary
    
    def _format_multiple_policies(self, policies_results: dict) -> str:
        """Format multiple policies for comparison"""
        summary = ""
        
        for idx, (policy_name, scenarios) in enumerate(policies_results.items(), 1):
            summary += f"\n**Policy {idx}: {policy_name}**\n"
            
            # Get first scenario to extract policy details
            first_scenario = list(scenarios.values())[0]
            if 'policy_config' in first_scenario:
                config = first_scenario['policy_config']
                summary += f"Type: {config.get('policy_type', 'Unknown')}\n"
                summary += f"Description: {config.get('description', 'N/A')}\n"
        
        return summary
    
    def _format_performance_comparison(self, policies_results: dict, scenarios: list) -> str:
        """Format performance data for comparison"""
        data = "**Performance Summary:**\n\n"
        
        for scenario in scenarios:
            data += f"**{scenario.upper()} Scenario:**\n"
            
            for policy_name, results in policies_results.items():
                if scenario in results:
                    metrics = results[scenario].get('metrics', {})
                    data += f"- {policy_name}:\n"
                    data += f"  * Avg Delay: {metrics.get('average_delay', 0):.1f}s\n"
                    data += f"  * Throughput: {metrics.get('throughput', 0):.0f} veh/h\n"
                    data += f"  * CO₂: {metrics.get('co2_emissions', 0):.2f} kg\n"
            
            data += "\n"
        
        return data
    
    def generate_executive_summary(self, 
                                   best_policy: str,
                                   key_findings: list,
                                   recommendations: list) -> str:
        """
        Generate executive summary of analysis
        
        Args:
            best_policy: Name of best performing policy
            key_findings: List of key findings
            recommendations: List of recommendations
            
        Returns:
            Formatted executive summary
        """
        summary = "# Executive Summary\n\n"
        
        summary += f"**Recommended Policy:** {best_policy}\n\n"
        
        summary += "## Key Findings\n"
        for idx, finding in enumerate(key_findings, 1):
            summary += f"{idx}. {finding}\n"
        
        summary += "\n## Recommendations\n"
        for idx, rec in enumerate(recommendations, 1):
            summary += f"{idx}. {rec}\n"
        
        return summary