"""
SUMO Traffic Simulator Integration
Handles SUMO simulation execution and data collection
"""

import os
import random
import xml.etree.ElementTree as ET
from typing import Dict, List
import traci
import sumolib
from config.settings import (
    DEFAULT_SIMULATION_TIME,
    SIMULATION_STEP_SIZE,
    WARMUP_TIME
)

class SUMOSimulator:
    """Interface for SUMO traffic microsimulation"""
    
    def __init__(self, network_dir: str = "sumo_networks"):
        """
        Initialize SUMO simulator
        
        Args:
            network_dir: Directory containing SUMO network files
        """
        self.network_dir = network_dir
        self.sumo_binary = sumolib.checkBinary('sumo')  # Use 'sumo-gui' for visualization
        self.simulation_running = False
        self.current_step = 0
        
    def create_simple_network(self, network_name: str = "simple_grid") -> str:
        """
        Create a simple grid network for testing
        
        Args:
            network_name: Name for the network files
            
        Returns:
            Path to network configuration file
        """
        network_path = os.path.join(self.network_dir, network_name)
        os.makedirs(network_path, exist_ok=True)
        
        # Create nodes file
        nodes_file = os.path.join(network_path, f"{network_name}.nod.xml")
        self._create_grid_nodes(nodes_file)
        
        # Create edges file
        edges_file = os.path.join(network_path, f"{network_name}.edg.xml")
        self._create_grid_edges(edges_file)
        
        # Create network using netconvert (simplified - requires SUMO installation)
        net_file = os.path.join(network_path, f"{network_name}.net.xml")
        
        # Note: This requires SUMO's netconvert tool
        # For now, we'll create a simplified network structure
        
        return network_path
    
    def _create_grid_nodes(self, filename: str, grid_size: int = 3):
        """Create a simple grid of nodes"""
        root = ET.Element("nodes")
        
        spacing = 200  # meters between nodes
        
        for i in range(grid_size):
            for j in range(grid_size):
                node = ET.SubElement(root, "node")
                node.set("id", f"n{i}_{j}")
                node.set("x", str(i * spacing))
                node.set("y", str(j * spacing))
        
        tree = ET.ElementTree(root)
        tree.write(filename, encoding='utf-8', xml_declaration=True)
    
    def _create_grid_edges(self, filename: str, grid_size: int = 3):
        """Create edges connecting grid nodes"""
        root = ET.Element("edges")
        
        # Horizontal edges
        for i in range(grid_size):
            for j in range(grid_size - 1):
                edge = ET.SubElement(root, "edge")
                edge.set("id", f"e{i}_{j}_h")
                edge.set("from", f"n{i}_{j}")
                edge.set("to", f"n{i}_{j+1}")
                edge.set("numLanes", "2")
                edge.set("speed", "13.89")  # ~50 km/h
        
        # Vertical edges
        for i in range(grid_size - 1):
            for j in range(grid_size):
                edge = ET.SubElement(root, "edge")
                edge.set("id", f"e{i}_{j}_v")
                edge.set("from", f"n{i}_{j}")
                edge.set("to", f"n{i+1}_{j}")
                edge.set("numLanes", "2")
                edge.set("speed", "13.89")
        
        tree = ET.ElementTree(root)
        tree.write(filename, encoding='utf-8', xml_declaration=True)
    
    def generate_traffic_demand(self, 
                               network_path: str,
                               num_vehicles: int = 100,
                               demand_pattern: str = "uniform") -> str:
        """
        Generate traffic demand (routes) for simulation
        
        Args:
            network_path: Path to network directory
            num_vehicles: Number of vehicles to generate
            demand_pattern: Traffic demand pattern ('uniform', 'peak', 'random')
            
        Returns:
            Path to route file
        """
        route_file = os.path.join(network_path, "routes.rou.xml")
        
        root = ET.Element("routes")
        
        # Define vehicle type
        vtype = ET.SubElement(root, "vType")
        vtype.set("id", "car")
        vtype.set("accel", "2.6")
        vtype.set("decel", "4.5")
        vtype.set("sigma", "0.5")
        vtype.set("length", "5")
        vtype.set("maxSpeed", "15")
        
        # Generate routes (simplified - in real scenario, use actual network)
        edges = ["e0_0_h", "e0_1_h", "e1_0_v", "e1_1_v"]
        
        for i in range(num_vehicles):
            vehicle = ET.SubElement(root, "vehicle")
            vehicle.set("id", f"veh{i}")
            vehicle.set("type", "car")
            vehicle.set("depart", str(self._get_departure_time(i, num_vehicles, demand_pattern)))
            
            # Random route
            route = ET.SubElement(vehicle, "route")
            route.set("edges", " ".join(random.sample(edges, min(2, len(edges)))))
        
        tree = ET.ElementTree(root)
        tree.write(route_file, encoding='utf-8', xml_declaration=True)
        
        return route_file
    
    def _get_departure_time(self, vehicle_id: int, total_vehicles: int, pattern: str) -> float:
        """Calculate vehicle departure time based on demand pattern"""
        if pattern == "uniform":
            return vehicle_id * (DEFAULT_SIMULATION_TIME / total_vehicles)
        elif pattern == "peak":
            # Concentrate departures in peak hours
            peak_start = 900  # 15 minutes
            peak_duration = 1800  # 30 minutes
            return peak_start + random.uniform(0, peak_duration)
        else:  # random
            return random.uniform(0, DEFAULT_SIMULATION_TIME)
    
    def run_simulation(self,
                      config_file: str,
                      policy_config: dict = None,
                      climate_scenario: dict = None,
                      simulation_time: int = None) -> dict:
        """
        Run SUMO simulation and collect results
        
        Args:
            config_file: Path to SUMO configuration file
            policy_config: Traffic policy configuration
            climate_scenario: Climate stress scenario parameters
            simulation_time: Simulation duration in seconds
            
        Returns:
            Dictionary containing simulation results
        """
        sim_time = simulation_time or DEFAULT_SIMULATION_TIME
        
        # For this initial version, we'll generate synthetic data
        # In production, this would run actual SUMO simulation
        
        results = self._run_synthetic_simulation(
            policy_config=policy_config,
            climate_scenario=climate_scenario,
            simulation_time=sim_time
        )
        
        return results
    
    def _run_synthetic_simulation(self,
                                 policy_config: dict = None,
                                 climate_scenario: dict = None,
                                 simulation_time: int = 3600) -> dict:
        """
        Generate synthetic simulation data for testing
        (Replace with actual SUMO simulation in production)
        
        Args:
            policy_config: Policy configuration
            climate_scenario: Climate scenario parameters
            simulation_time: Simulation duration
            
        Returns:
            Synthetic simulation results
        """
        
        # Base performance values
        base_delay = 45.0
        base_throughput = 1200
        base_emissions = 450.0
        base_speed = 35.0
        base_travel_time = 1.5
        
        # Apply climate scenario impacts
        if climate_scenario:
            capacity_reduction = climate_scenario.get('capacity_reduction', 0)
            efficiency_loss = climate_scenario.get('efficiency_loss', 0)
            emission_factor = climate_scenario.get('emission_factor', 1.0)
            
            # Climate stress increases delay and emissions, reduces throughput and speed
            base_delay *= (1 + capacity_reduction)
            base_throughput *= (1 - capacity_reduction * 0.5)
            base_emissions *= emission_factor
            base_speed *= (1 - efficiency_loss)
            base_travel_time *= (1 + efficiency_loss)
        
        # Apply policy impacts (simplified)
        if policy_config:
            policy_type = policy_config.get('policy_type', '')
            
            if 'Signal' in policy_type:
                # Signal optimization reduces delay
                base_delay *= 0.85
                base_throughput *= 1.10
            elif 'Pricing' in policy_type:
                # Pricing reduces demand, improves flow
                base_delay *= 0.75
                base_throughput *= 0.90
                base_emissions *= 0.85
            elif 'Speed' in policy_type:
                # Speed management affects emissions and speed
                base_speed *= 0.95
                base_emissions *= 0.90
            elif 'Access' in policy_type:
                # Access restriction reduces volume
                base_throughput *= 0.80
                base_delay *= 0.70
                base_emissions *= 0.75
        
        # Add some randomness
        random_factor = random.uniform(0.95, 1.05)
        
        # Generate vehicle-level data
        num_vehicles = int(base_throughput * (simulation_time / 3600) * random_factor)
        vehicles = []
        
        for i in range(num_vehicles):
            vehicle = {
                'id': f'veh_{i}',
                'delay': max(0, random.gauss(base_delay, base_delay * 0.3)),
                'speed': max(0, random.gauss(base_speed / 3.6, 2)),  # m/s
                'travel_time': max(0, random.gauss(base_travel_time * 3600 / num_vehicles, 30)),
                'distance': random.uniform(500, 2000),  # meters
                'co2_emissions': random.uniform(50, 200),  # grams
                'completed': True
            }
            vehicles.append(vehicle)
        
        results = {
            'simulation_time': simulation_time,
            'vehicles': vehicles,
            'policy_applied': policy_config.get('policy_name', 'None') if policy_config else 'None',
            'climate_scenario': climate_scenario.get('name', 'Baseline') if climate_scenario else 'Baseline'
        }
        
        return results
    
    def apply_policy_to_network(self, policy_config: dict, network_path: str):
        """
        Apply policy configuration to network
        (This would modify SUMO network files based on policy)
        
        Args:
            policy_config: Policy configuration
            network_path: Path to network files
        """
        # Placeholder for policy application logic
        # In production, this would modify:
        # - Traffic light programs (for signal timing)
        # - Edge speeds (for speed management)
        # - Vehicle types (for access restrictions)
        # - Additional files (for road pricing)
        pass
    
    def cleanup(self):
        """Clean up SUMO simulation resources"""
        if self.simulation_running:
            try:
                traci.close()
                self.simulation_running = False
            except:
                pass