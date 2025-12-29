"""
Configuration settings for TrafficGen-AI
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"  # Fast and reliable for policy generation

# Simulation Settings
DEFAULT_SIMULATION_TIME = 3600  # seconds (1 hour)
SIMULATION_STEP_SIZE = 1.0  # seconds
WARMUP_TIME = 300  # seconds (5 minutes)

# Climate Stress Scenarios
CLIMATE_SCENARIOS = {
    "baseline": {
        "name": "Baseline (No Climate Stress)",
        "capacity_reduction": 0.0,
        "efficiency_loss": 0.0,
        "emission_factor": 1.0
    },
    "moderate": {
        "name": "Moderate Climate Stress",
        "capacity_reduction": 0.15,  # 15% capacity reduction
        "efficiency_loss": 0.10,  # 10% efficiency loss
        "emission_factor": 1.15  # 15% higher emissions
    },
    "severe": {
        "name": "Severe Climate Stress",
        "capacity_reduction": 0.30,  # 30% capacity reduction
        "efficiency_loss": 0.20,  # 20% efficiency loss
        "emission_factor": 1.30  # 30% higher emissions
    },
    "extreme": {
        "name": "Extreme Climate Stress",
        "capacity_reduction": 0.45,  # 45% capacity reduction
        "efficiency_loss": 0.35,  # 35% efficiency loss
        "emission_factor": 1.50  # 50% higher emissions
    }
}

# Policy Types
POLICY_TYPES = [
    "Signal Timing Optimization",
    "Road Pricing Strategy",
    "Access Restriction",
    "Speed Management",
    "Lane Management"
]

# Performance Metrics
METRICS = {
    "average_delay": "Average Delay (seconds)",
    "throughput": "Throughput (vehicles/hour)",
    "co2_emissions": "CO2 Emissions (kg)",
    "average_speed": "Average Speed (km/h)",
    "total_travel_time": "Total Travel Time (hours)"
}

# Streamlit Configuration
PAGE_TITLE = "TrafficGen-AI"
PAGE_ICON = "🚦"
LAYOUT = "wide"

# Colors for visualization
COLORS = {
    "baseline": "#2E86AB",
    "moderate": "#A23B72",
    "severe": "#F18F01",
    "extreme": "#C73E1D",
    "success": "#06A77D",
    "warning": "#F18F01",
    "danger": "#C73E1D"
}

# Theme Configuration
THEMES = {
    "light": {
        "primary_color": "#667eea",
        "secondary_color": "#764ba2",
        "background_color": "#ffffff",
        "text_color": "#000000",
        "card_background": "#f8f9fa"
    },
    "dark": {
        "primary_color": "#8b5cf6",
        "secondary_color": "#a78bfa",
        "background_color": "#1a1a2e",
        "text_color": "#ffffff",
        "card_background": "#16213e"
    }
}

# Advanced Features Flags
ENABLE_3D_VISUALIZATION = True
ENABLE_STATISTICAL_ANALYSIS = True
ENABLE_OPTIMIZATION = True
ENABLE_REPORT_GENERATION = True
ENABLE_ADVANCED_CHARTS = True

# Report Configuration
REPORT_AUTHOR = "MAHBUB HASSAN"
REPORT_INSTITUTION = "Chulalongkorn University"
REPORT_DEPARTMENT = "Transportation Engineering"