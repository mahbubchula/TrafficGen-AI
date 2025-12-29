"""
Advanced Visualization Module
3D charts, animations, and interactive visualizations
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from typing import Dict, List

class AdvancedVisualizer:
    """Create advanced interactive visualizations"""
    
    def __init__(self):
        """Initialize visualizer"""
        self.color_schemes = {
            'sequential': px.colors.sequential.Viridis,
            'diverging': px.colors.diverging.RdYlGn,
            'qualitative': px.colors.qualitative.Set2
        }
    
    def create_3d_performance_surface(self, results: Dict) -> go.Figure:
        """
        Create 3D surface plot of performance metrics
        
        Args:
            results: Simulation results
            
        Returns:
            3D surface plot figure
        """
        # Prepare data
        policies = list(results.keys())
        scenarios = list(list(results.values())[0].keys())
        
        # Create meshgrid
        X, Y = np.meshgrid(range(len(scenarios)), range(len(policies)))
        
        # Extract delay values
        Z = np.zeros((len(policies), len(scenarios)))
        for i, policy in enumerate(policies):
            for j, scenario in enumerate(scenarios):
                Z[i, j] = results[policy][scenario]['metrics'].get('average_delay', 0)
        
        fig = go.Figure(data=[go.Surface(
            x=X,
            y=Y,
            z=Z,
            colorscale='Viridis',
            colorbar=dict(title="Delay (s)")
        )])
        
        fig.update_layout(
            title='3D Performance Surface: Average Delay',
            scene=dict(
                xaxis_title='Scenario',
                yaxis_title='Policy',
                zaxis_title='Delay (s)',
                xaxis=dict(ticktext=scenarios, tickvals=list(range(len(scenarios)))),
                yaxis=dict(ticktext=[p[:15] for p in policies], tickvals=list(range(len(policies))))
            ),
            height=700
        )
        
        return fig
    
    def create_animated_timeline(self, results: Dict) -> go.Figure:
        """
        Create animated timeline showing policy performance evolution
        
        Args:
            results: Simulation results
            
        Returns:
            Animated timeline figure
        """
        # Prepare data for animation
        data = []
        
        for policy_name, scenarios in results.items():
            for i, (scenario_name, scenario_data) in enumerate(scenarios.items()):
                metrics = scenario_data['metrics']
                data.append({
                    'Policy': policy_name,
                    'Scenario': scenario_name,
                    'Step': i,
                    'Delay': metrics.get('average_delay', 0),
                    'Throughput': metrics.get('throughput', 0),
                    'Emissions': metrics.get('co2_emissions', 0)
                })
        
        df = pd.DataFrame(data)
        
        fig = px.scatter(
            df,
            x='Delay',
            y='Throughput',
            color='Policy',
            size='Emissions',
            animation_frame='Step',
            animation_group='Policy',
            hover_name='Policy',
            title='Animated Policy Performance Evolution',
            labels={'Delay': 'Average Delay (s)', 'Throughput': 'Throughput (veh/h)'}
        )
        
        fig.update_layout(height=600)
        
        return fig
    
    def create_sankey_diagram(self, results: Dict) -> go.Figure:
        """
        Create Sankey diagram showing policy-scenario-outcome relationships
        
        Args:
            results: Simulation results
            
        Returns:
            Sankey diagram figure
        """
        # Prepare nodes and links
        nodes = []
        links = {'source': [], 'target': [], 'value': []}
        
        # Create nodes: Policies -> Scenarios -> Performance Levels
        policies = list(results.keys())
        scenarios = list(set(s for r in results.values() for s in r.keys()))
        performance_levels = ['Excellent', 'Good', 'Fair', 'Poor']
        
        all_nodes = policies + scenarios + performance_levels
        node_dict = {name: i for i, name in enumerate(all_nodes)}
        
        # Create links
        for policy_name, policy_scenarios in results.items():
            for scenario_name, data in policy_scenarios.items():
                # Policy to Scenario
                links['source'].append(node_dict[policy_name])
                links['target'].append(node_dict[scenario_name])
                links['value'].append(10)
                
                # Scenario to Performance Level
                delay = data['metrics'].get('average_delay', 0)
                if delay < 30:
                    perf_level = 'Excellent'
                elif delay < 60:
                    perf_level = 'Good'
                elif delay < 90:
                    perf_level = 'Fair'
                else:
                    perf_level = 'Poor'
                
                links['source'].append(node_dict[scenario_name])
                links['target'].append(node_dict[perf_level])
                links['value'].append(delay / 10)
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=all_nodes,
                color=['#667eea'] * len(policies) + ['#764ba2'] * len(scenarios) + ['#06A77D', '#2E86AB', '#F18F01', '#C73E1D']
            ),
            link=dict(
                source=links['source'],
                target=links['target'],
                value=links['value']
            )
        )])
        
        fig.update_layout(
            title="Policy-Scenario-Performance Flow Diagram",
            height=600
        )
        
        return fig
    
    def create_parallel_coordinates(self, results: Dict) -> go.Figure:
        """
        Create parallel coordinates plot for multi-metric comparison
        
        Args:
            results: Simulation results
            
        Returns:
            Parallel coordinates figure
        """
        # Prepare data
        data = []
        
        for policy_name, scenarios in results.items():
            for scenario_name, scenario_data in scenarios.items():
                metrics = scenario_data['metrics']
                data.append({
                    'Policy': policy_name,
                    'Scenario': scenario_name,
                    'Delay': metrics.get('average_delay', 0),
                    'Throughput': metrics.get('throughput', 0),
                    'Emissions': metrics.get('co2_emissions', 0),
                    'Speed': metrics.get('average_speed', 0)
                })
        
        df = pd.DataFrame(data)
        
        fig = go.Figure(data=
            go.Parcoords(
                line=dict(
                    color=df.index,
                    colorscale='Viridis'
                ),
                dimensions=list([
                    dict(range=[df['Delay'].min(), df['Delay'].max()],
                         label='Delay (s)', values=df['Delay']),
                    dict(range=[df['Throughput'].min(), df['Throughput'].max()],
                         label='Throughput', values=df['Throughput']),
                    dict(range=[df['Emissions'].min(), df['Emissions'].max()],
                         label='Emissions (kg)', values=df['Emissions']),
                    dict(range=[df['Speed'].min(), df['Speed'].max()],
                         label='Speed (km/h)', values=df['Speed'])
                ])
            )
        )
        
        fig.update_layout(
            title='Parallel Coordinates: Multi-Metric Analysis',
            height=500
        )
        
        return fig
    
    def create_sunburst_chart(self, results: Dict) -> go.Figure:
        """
        Create sunburst chart for hierarchical performance visualization
        
        Args:
            results: Simulation results
            
        Returns:
            Sunburst chart figure
        """
        # Prepare hierarchical data
        labels = ['All Policies']
        parents = ['']
        values = [100]
        colors = ['#667eea']
        
        for policy_name, scenarios in results.items():
            # Add policy level
            labels.append(policy_name)
            parents.append('All Policies')
            policy_value = sum(s['metrics'].get('throughput', 0) for s in scenarios.values()) / len(scenarios)
            values.append(policy_value)
            colors.append('#764ba2')
            
            # Add scenario level
            for scenario_name, data in scenarios.items():
                labels.append(f"{policy_name}-{scenario_name}")
                parents.append(policy_name)
                values.append(data['metrics'].get('throughput', 0))
                colors.append('#2E86AB')
        
        fig = go.Figure(go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            marker=dict(colors=colors),
            branchvalues="total"
        ))
        
        fig.update_layout(
            title='Hierarchical Performance Analysis (Sunburst)',
            height=600
        )
        
        return fig
    
    def create_violin_plot(self, results: Dict, metric: str = 'average_delay') -> go.Figure:
        """
        Create violin plot for metric distribution analysis
        
        Args:
            results: Simulation results
            metric: Metric to analyze
            
        Returns:
            Violin plot figure
        """
        # Prepare data
        data = []
        
        for policy_name, scenarios in results.items():
            for scenario_name, scenario_data in scenarios.items():
                data.append({
                    'Policy': policy_name,
                    'Scenario': scenario_name,
                    'Value': scenario_data['metrics'].get(metric, 0)
                })
        
        df = pd.DataFrame(data)
        
        fig = go.Figure()
        
        for policy in df['Policy'].unique():
            policy_data = df[df['Policy'] == policy]
            
            fig.add_trace(go.Violin(
                y=policy_data['Value'],
                name=policy,
                box_visible=True,
                meanline_visible=True
            ))
        
        fig.update_layout(
            title=f'Distribution Analysis: {metric.replace("_", " ").title()}',
            yaxis_title=metric.replace('_', ' ').title(),
            height=500
        )
        
        return fig
    
    def create_treemap(self, results: Dict) -> go.Figure:
        """
        Create treemap for performance hierarchy visualization
        
        Args:
            results: Simulation results
            
        Returns:
            Treemap figure
        """
        # Prepare data
        labels = []
        parents = []
        values = []
        colors = []
        
        for policy_name, scenarios in results.items():
            # Policy level
            labels.append(policy_name)
            parents.append("")
            policy_avg = np.mean([s['metrics'].get('throughput', 0) for s in scenarios.values()])
            values.append(policy_avg)
            colors.append(policy_avg)
            
            # Scenario level
            for scenario_name, data in scenarios.items():
                labels.append(f"{scenario_name}")
                parents.append(policy_name)
                throughput = data['metrics'].get('throughput', 0)
                values.append(throughput)
                colors.append(throughput)
        
        fig = go.Figure(go.Treemap(
            labels=labels,
            parents=parents,
            values=values,
            marker=dict(
                colorscale='Viridis',
                cmid=np.mean(colors),
                colorbar=dict(title="Throughput")
            ),
            textinfo="label+value"
        ))
        
        fig.update_layout(
            title='Performance Treemap (by Throughput)',
            height=600
        )
        
        return fig