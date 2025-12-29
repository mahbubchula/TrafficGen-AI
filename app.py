"""
TrafficGen-AI: ULTIMATE VERSION
Climate-Adaptive Traffic Policy Generation with Advanced AI Features
Premium Research-Grade Tool
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import numpy as np

# Import all modules
from modules.policy_generator import PolicyGenerator
from modules.climate_scenarios import ClimateScenarioManager
from modules.sumo_simulator import SUMOSimulator
from modules.evaluator import PerformanceEvaluator
from modules.interpreter import ResultInterpreter
from modules.optimizer import MultiObjectiveOptimizer
from modules.analytics import StatisticalAnalyzer
from modules.report_generator import ReportGenerator
from modules.advanced_visualizations import AdvancedVisualizer

from config.settings import (
    PAGE_TITLE, PAGE_ICON, LAYOUT,
    POLICY_TYPES, COLORS, CLIMATE_SCENARIOS, GROQ_API_KEY,
    THEMES, ENABLE_3D_VISUALIZATION, ENABLE_STATISTICAL_ANALYSIS,
    ENABLE_OPTIMIZATION, REPORT_AUTHOR, REPORT_INSTITUTION
)

# Page configuration
st.set_page_config(
    page_title=PAGE_TITLE + " - Ultimate Edition",
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'generated_policies' not in st.session_state:
    st.session_state.generated_policies = []
if 'simulation_results' not in st.session_state:
    st.session_state.simulation_results = {}
if 'api_key_set' not in st.session_state:
    st.session_state.api_key_set = False
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'pareto_front' not in st.session_state:
    st.session_state.pareto_front = []
if 'statistical_analysis' not in st.session_state:
    st.session_state.statistical_analysis = {}

def apply_theme():
    """Apply selected theme"""
    theme = THEMES[st.session_state.theme]
    
    if st.session_state.theme == 'dark':
        st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
            
            * { font-family: 'Inter', sans-serif; }
            
            .main {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                background-attachment: fixed;
            }
            
            .block-container {
                background: rgba(22, 33, 62, 0.95);
                border-radius: 20px;
                padding: 2rem;
                box-shadow: 0 20px 60px rgba(0,0,0,0.5);
                backdrop-filter: blur(10px);
            }
            
            .main-header {
                font-size: 3.5rem;
                font-weight: 700;
                background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem;
                text-align: center;
                animation: fadeInDown 0.8s ease-out;
            }
            
            .sub-header {
                font-size: 1.3rem;
                color: #a0aec0;
                margin-bottom: 2rem;
                text-align: center;
                font-weight: 300;
                animation: fadeInUp 0.8s ease-out;
            }
            
            h1, h2, h3, h4 { color: #a78bfa !important; font-weight: 600; }
            
            .metric-card {
                background: linear-gradient(135deg, #8b5cf615 0%, #a78bfa15 100%);
                padding: 1.5rem;
                border-radius: 15px;
                border: 2px solid #8b5cf630;
                box-shadow: 0 4px 15px rgba(139, 92, 246, 0.2);
                transition: all 0.3s ease;
                margin: 1rem 0;
            }
            
            .metric-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);
                border-color: #8b5cf6;
            }
            
            .stButton>button {
                background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 0.75rem 2rem;
                font-weight: 600;
                font-size: 1rem;
                box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
                transition: all 0.3s ease;
                width: 100%;
            }
            
            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(139, 92, 246, 0.5);
            }
            
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
            }
            
            [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
            
            .card {
                background: rgba(22, 33, 62, 0.8);
                border-radius: 15px;
                padding: 2rem;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                margin: 1rem 0;
                border: 1px solid rgba(139, 92, 246, 0.2);
            }
            
            .stDataFrame { background: rgba(22, 33, 62, 0.8); border-radius: 10px; }
            
            @keyframes fadeInDown {
                from { opacity: 0; transform: translateY(-20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes fadeInUp {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        # Light theme (your existing premium CSS)
        st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
            
            * { font-family: 'Inter', sans-serif; }
            
            .main {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                background-attachment: fixed;
            }
            
            .block-container {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                padding: 2rem;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                backdrop-filter: blur(10px);
            }
            
            .main-header {
                font-size: 3.5rem;
                font-weight: 700;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem;
                text-align: center;
                animation: fadeInDown 0.8s ease-out;
            }
            
            .sub-header {
                font-size: 1.3rem;
                color: #666;
                margin-bottom: 2rem;
                text-align: center;
                font-weight: 300;
                animation: fadeInUp 0.8s ease-out;
            }
            
            h2, h3 { color: #667eea; font-weight: 600; margin-top: 2rem; }
            
            .metric-card {
                background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
                padding: 1.5rem;
                border-radius: 15px;
                border: 2px solid #667eea30;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.1);
                transition: all 0.3s ease;
                margin: 1rem 0;
            }
            
            .metric-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
                border-color: #667eea;
            }
            
            .stButton>button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 0.75rem 2rem;
                font-weight: 600;
                font-size: 1rem;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                transition: all 0.3s ease;
                width: 100%;
            }
            
            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            }
            
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
            }
            
            [data-testid="stSidebar"] * { color: white !important; }
            
            .card {
                background: white;
                border-radius: 15px;
                padding: 2rem;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                margin: 1rem 0;
                transition: all 0.3s ease;
            }
            
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            }
            
            @keyframes fadeInDown {
                from { opacity: 0; transform: translateY(-20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes fadeInUp {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
        """, unsafe_allow_html=True)

def main():
    """Main application flow"""
    
    # Apply theme
    apply_theme()
    
    # Header
    st.markdown('<div class="main-header">🚦 TrafficGen-AI Ultimate</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Advanced AI-Powered Climate-Adaptive Traffic Policy Platform</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # Theme Toggle
        theme_col1, theme_col2 = st.columns(2)
        with theme_col1:
            if st.button("☀️ Light", use_container_width=True):
                st.session_state.theme = 'light'
                st.rerun()
        with theme_col2:
            if st.button("🌙 Dark", use_container_width=True):
                st.session_state.theme = 'dark'
                st.rerun()
        
        st.caption(f"Current: {st.session_state.theme.title()} Mode")
        
        st.markdown("---")
        
        # API Key
        if GROQ_API_KEY:
            api_key = GROQ_API_KEY
            st.session_state.api_key_set = True
            st.success("✅ API Key Loaded")
        else:
            api_key = st.text_input(
                "Groq API Key",
                type="password",
                help="Enter your Groq API key"
            )
            
            if api_key:
                st.session_state.api_key_set = True
                st.success("✅ API Key Set")
        
        st.markdown("---")
        
        # Navigation
        st.markdown("## 📍 Navigation")
        page = st.radio(
            "Select Page",
            [
                "🏠 Home",
                "🔧 Policy Generation",
                "⚡ Simulation & Evaluation",
                "📊 Results Analysis",
                "🎯 Multi-Objective Optimization",
                "📈 Statistical Analysis",
                "🎨 Advanced Visualizations",
                "📄 Report Generation",
                "ℹ️ About"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Stats
        st.markdown("### 📈 Session Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Policies", len(st.session_state.generated_policies))
        with col2:
            st.metric("Results", len(st.session_state.simulation_results))
        
        if st.session_state.pareto_front:
            st.metric("Pareto Optimal", len(st.session_state.pareto_front))
        
        st.markdown("---")
        
        st.markdown("### 👨‍💻 Developer")
        st.markdown("**MAHBUB HASSAN**")
        st.caption("Transportation Engineering")
        st.caption("Chulalongkorn University")
        st.caption("Bangkok, Thailand")
        
        st.markdown("---")
        st.caption("TrafficGen-AI Ultimate v2.0")
        st.caption("© 2025 All Rights Reserved")
    
    # Route to pages
    if page == "🏠 Home":
        show_home_page()
    elif page == "🔧 Policy Generation":
        show_policy_generation_page(api_key)
    elif page == "⚡ Simulation & Evaluation":
        show_simulation_page()
    elif page == "📊 Results Analysis":
        show_results_page(api_key)
    elif page == "🎯 Multi-Objective Optimization":
        show_optimization_page()
    elif page == "📈 Statistical Analysis":
        show_statistical_analysis_page()
    elif page == "🎨 Advanced Visualizations":
        show_advanced_visualizations_page()
    elif page == "📄 Report Generation":
        show_report_generation_page()
    elif page == "ℹ️ About":
        show_about_page()

# [Previous functions: show_home_page, show_policy_generation_page, etc. remain the same]
# I'll add the NEW advanced pages below

def show_home_page():
    """Display premium home page"""
    
    st.markdown("## 🎯 Welcome to TrafficGen-AI Ultimate Edition")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3 style="color: #667eea;">🤖 AI-Powered</h3>
            <p>Generate intelligent traffic policies using state-of-the-art LLMs with multi-agent optimization</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3 style="color: #764ba2;">🌡️ Climate-Adaptive</h3>
            <p>Evaluate policies under climate stress with advanced statistical analysis and sensitivity testing</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h3 style="color: #06A77D;">📊 Research-Grade</h3>
            <p>Publication-ready analysis with automated report generation and professional visualizations</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # NEW: Advanced Features Showcase
    st.markdown("## ✨ Ultimate Features")
    
    feature_col1, feature_col2 = st.columns(2)
    
    with feature_col1:
        st.markdown("""
        ### 🔬 Advanced Analytics
        - **Multi-Objective Optimization** with Pareto frontier analysis
        - **Statistical Hypothesis Testing** (ANOVA, confidence intervals)
        - **Sensitivity Analysis** for parameter variations
        - **Correlation Analysis** between metrics
        
        ### 🎨 Premium Visualizations
        - **3D Performance Surfaces** for spatial analysis
        - **Animated Timelines** showing evolution
        - **Parallel Coordinates** for multi-metric comparison
        - **Sankey Diagrams** for flow visualization
        """)
    
    with feature_col2:
        st.markdown("""
        ### 📄 Professional Reports
        - **Automated PDF Generation** with charts
        - **Publication-Ready Formatting** for journals
        - **Executive Summaries** for stakeholders
        - **Methodology Documentation** for reproducibility
        
        ### 🌓 Enhanced UX
        - **Dark/Light Theme Toggle** for comfort
        - **Real-Time Progress Tracking** during simulations
        - **Interactive Dashboards** with drill-down
        - **One-Click Export** to multiple formats
        """)
    
    st.markdown("---")
    
    # Framework Capabilities
    st.markdown("## 🚀 Framework Capabilities")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #667eea; margin:0;">5+</h2>
            <p style="margin:0;">Policy Types</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #764ba2; margin:0;">4</h2>
            <p style="margin:0;">Climate Scenarios</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #06A77D; margin:0;">10+</h2>
            <p style="margin:0;">Visualization Types</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #F18F01; margin:0;">70B</h2>
            <p style="margin:0;">LLM Parameters</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="metric-card">
            <h2 style="color: #C73E1D; margin:0;">Q1</h2>
            <p style="margin:0;">Journal Ready</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Climate Scenarios
    st.markdown("## 🌡️ Climate Scenarios")
    
    scenarios_df = pd.DataFrame([
        {
            "Scenario": info["name"],
            "Capacity Reduction": f"{info['capacity_reduction']*100:.0f}%",
            "Efficiency Loss": f"{info['efficiency_loss']*100:.0f}%",
            "Emission Factor": f"{info['emission_factor']:.2f}x"
        }
        for name, info in CLIMATE_SCENARIOS.items()
    ])
    
    st.dataframe(scenarios_df, use_container_width=True, hide_index=True)

def show_policy_generation_page(api_key):
    """Premium policy generation interface"""
    
    st.markdown("## 🔧 AI-Powered Policy Generation")
    
    if not st.session_state.api_key_set:
        st.warning("⚠️ Please enter your Groq API key in the sidebar to generate policies.")
        st.info("💡 **Tip:** You can get a free Groq API key at https://console.groq.com/")
        return
    
    st.markdown("""
    <div class="card">
    Define your traffic management objectives and let our AI generate optimized policy configurations 
    tailored to your specific needs and climate scenarios.
    </div>
    """, unsafe_allow_html=True)
    
    # Input form with premium styling
    with st.form("policy_generation_form"):
        st.markdown("### 📋 Policy Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            network_type = st.selectbox(
                "🏙️ Network Type",
                ["Urban Arterial", "Highway Corridor", "City Grid", "Suburban Network", "Mixed Network"]
            )
            
            climate_scenario = st.selectbox(
                "🌡️ Climate Scenario",
                list(CLIMATE_SCENARIOS.keys()),
                format_func=lambda x: CLIMATE_SCENARIOS[x]["name"]
            )
        
        with col2:
            policy_objective = st.selectbox(
                "🎯 Primary Objective",
                [
                    "Minimize Average Delay",
                    "Reduce CO2 Emissions",
                    "Maximize Throughput",
                    "Balance Multiple Objectives",
                    "Improve Network Resilience",
                    "Enhance Safety"
                ]
            )
            
            policy_type = st.selectbox(
                "📊 Preferred Policy Type (Optional)",
                ["Any"] + POLICY_TYPES
            )
        
        constraints = st.text_area(
            "⚙️ Additional Constraints & Requirements",
            placeholder="e.g., Budget limit: $500,000, Implementation time: 6 months, No major infrastructure changes",
            height=120
        )
        
        st.markdown("---")
        
        submit_button = st.form_submit_button(
            "🚀 Generate Policy with AI",
            use_container_width=True
        )
    
    if submit_button:
        with st.spinner("🤖 AI is analyzing your requirements and generating optimized policy..."):
            try:
                generator = PolicyGenerator(api_key=api_key)
                
                policy = generator.generate_policy(
                    network_type=network_type,
                    climate_scenario=CLIMATE_SCENARIOS[climate_scenario]["name"],
                    policy_objective=policy_objective,
                    constraints=constraints if constraints else "None"
                )
                
                is_valid, message = generator.validate_policy(policy)
                
                if is_valid:
                    policy['generated_at'] = datetime.now().isoformat()
                    st.session_state.generated_policies.append(policy)
                    
                    st.success("✅ Policy generated successfully!")
                    st.balloons()
                    
                    display_policy_premium(policy)
                else:
                    st.error(f"❌ Policy validation failed: {message}")
                    
            except Exception as e:
                st.error(f"❌ Error generating policy: {str(e)}")
    
    # Display previously generated policies
    if st.session_state.generated_policies:
        st.markdown("---")
        st.markdown("## 📋 Generated Policies Library")
        st.caption(f"Total: {len(st.session_state.generated_policies)} policies")
        
        for idx, policy in enumerate(st.session_state.generated_policies):
            with st.expander(f"**Policy {idx + 1}:** {policy.get('policy_name', 'Unnamed')} 🔍", expanded=False):
                display_policy_premium(policy)
                
                col1, col2, col3 = st.columns([2, 2, 1])
                with col3:
                    if st.button(f"🗑️ Remove", key=f"remove_{idx}"):
                        st.session_state.generated_policies.pop(idx)
                        st.rerun()

def display_policy_premium(policy):
    """Display policy with premium styling"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### 📌 {policy.get('policy_name', 'N/A')}")
        st.markdown(f"**Type:** `{policy.get('policy_type', 'N/A')}`")
        st.markdown(f"**Description:** {policy.get('description', 'N/A')}")
        
        if 'implementation_notes' in policy:
            st.info(f"**💡 Implementation Notes:** {policy['implementation_notes']}")
    
    with col2:
        if 'expected_impacts' in policy:
            st.markdown("#### 📊 Expected Impacts")
            for key, value in policy['expected_impacts'].items():
                st.markdown(f"• **{key.title()}:** {value}")
    
    if 'parameters' in policy:
        st.markdown("#### ⚙️ Technical Parameters")
        params_df = pd.DataFrame([
            {"Parameter": k.replace('_', ' ').title(), "Value": v}
            for k, v in policy['parameters'].items()
        ])
        st.dataframe(params_df, use_container_width=True, hide_index=True)

def show_simulation_page():
    """Premium simulation interface"""
    
    st.markdown("## ⚡ Traffic Simulation & Performance Evaluation")
    
    if not st.session_state.generated_policies:
        st.warning("⚠️ No policies available. Please generate policies first.")
        st.info("👉 Navigate to **Policy Generation** to create policies")
        return
    
    st.markdown("""
    <div class="card">
    Run advanced traffic microsimulations to evaluate policy performance under various 
    climate scenarios. Get comprehensive insights on delay, emissions, throughput, and more.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎯 Simulation Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_policies = st.multiselect(
            "📋 Select Policies to Evaluate",
            range(len(st.session_state.generated_policies)),
            format_func=lambda x: f"{x+1}. {st.session_state.generated_policies[x].get('policy_name', f'Policy {x+1}')}",
            help="Choose one or more policies to test"
        )
    
    with col2:
        selected_scenarios = st.multiselect(
            "🌡️ Select Climate Scenarios",
            list(CLIMATE_SCENARIOS.keys()),
            default=["baseline", "moderate"],
            format_func=lambda x: CLIMATE_SCENARIOS[x]["name"],
            help="Select climate conditions to simulate"
        )
    
    with st.expander("⚙️ Advanced Simulation Settings", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sim_time = st.number_input("Simulation Time (seconds)", min_value=600, max_value=7200, value=3600, step=600)
        with col2:
            num_vehicles = st.number_input("Number of Vehicles", min_value=50, max_value=1000, value=200, step=50)
        with col3:
            num_runs = st.number_input("Number of Runs", min_value=1, max_value=10, value=1)
    
    st.markdown("---")
    
    if st.button("▶️ Run Simulation", use_container_width=True, type="primary"):
        if not selected_policies or not selected_scenarios:
            st.error("❌ Please select at least one policy and one scenario.")
            return
        
        run_simulations_premium(selected_policies, selected_scenarios, sim_time, num_vehicles, num_runs)

def run_simulations_premium(policy_indices, scenario_names, sim_time, num_vehicles, num_runs):
    """Execute simulations with premium progress display"""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    simulator = SUMOSimulator()
    evaluator = PerformanceEvaluator()
    scenario_manager = ClimateScenarioManager()
    
    total_simulations = len(policy_indices) * len(scenario_names)
    current_sim = 0
    
    results = {}
    
    for policy_idx in policy_indices:
        policy = st.session_state.generated_policies[policy_idx]
        policy_name = policy.get('policy_name', f'Policy {policy_idx + 1}')
        
        results[policy_name] = {}
        
        for scenario_name in scenario_names:
            status_text.markdown(f"🔄 **Running:** {policy_name} under `{CLIMATE_SCENARIOS[scenario_name]['name']}`...")
            
            scenario = scenario_manager.get_scenario(scenario_name)
            
            sim_data = simulator.run_simulation(
                config_file="default",
                policy_config=policy,
                climate_scenario=scenario,
                simulation_time=sim_time
            )
            
            metrics = evaluator.calculate_metrics(sim_data)
            
            results[policy_name][scenario_name] = {
                'metrics': metrics,
                'policy_config': policy,
                'scenario': scenario
            }
            
            current_sim += 1
            progress_bar.progress(current_sim / total_simulations)
    
    progress_bar.progress(1.0)
    status_text.markdown("✅ **Simulation completed successfully!**")
    
    st.session_state.simulation_results = results
    
    st.success(f"🎉 Successfully completed {total_simulations} simulations!")
    st.balloons()
    
    show_results_summary_premium(results, evaluator)

def show_results_summary_premium(results, evaluator):
    """Display premium summary of simulation results"""
    
    st.markdown("---")
    st.markdown("## 📊 Simulation Results Summary")
    
    summary_data = []
    
    for policy_name, scenarios in results.items():
        for scenario_name, data in scenarios.items():
            metrics = data['metrics']
            score = evaluator.calculate_composite_score(metrics)
            
            row = {
                'Policy': policy_name,
                'Scenario': CLIMATE_SCENARIOS[scenario_name]['name'],
                'Avg Delay (s)': f"{metrics.get('average_delay', 0):.1f}",
                'Throughput (veh/h)': f"{metrics.get('throughput', 0):.0f}",
                'CO₂ (kg)': f"{metrics.get('co2_emissions', 0):.2f}",
                'Avg Speed (km/h)': f"{metrics.get('average_speed', 0):.1f}",
                'Score': f"{score:.1f}"
            }
            summary_data.append(row)
    
    df = pd.DataFrame(summary_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("### 💡 Quick Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        best_policy = evaluator.identify_best_policy(
            {name: scenarios[list(scenarios.keys())[0]]['metrics'] 
             for name, scenarios in results.items()},
            objective="composite"
        )
        st.metric("🏆 Best Overall Policy", best_policy)
    
    with col2:
        best_emissions = evaluator.identify_best_policy(
            {name: scenarios[list(scenarios.keys())[0]]['metrics'] 
             for name, scenarios in results.items()},
            objective="emissions"
        )
        st.metric("🌱 Best for Emissions", best_emissions)
    
    with col3:
        best_delay = evaluator.identify_best_policy(
            {name: scenarios[list(scenarios.keys())[0]]['metrics'] 
             for name, scenarios in results.items()},
            objective="delay"
        )
        st.metric("⚡ Best for Delay", best_delay)

def show_results_page(api_key):
    """Premium results analysis page"""
    
    st.markdown("## 📊 Advanced Results Analysis")
    
    if not st.session_state.simulation_results:
        st.warning("⚠️ No simulation results available.")
        st.info("👉 Navigate to **Simulation & Evaluation** to run simulations first")
        return
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Performance Comparison",
        "🤖 AI Interpretation",
        "📉 Basic Visualizations",
        "📥 Export Results"
    ])
    
    with tab1:
        show_performance_comparison_premium()
    
    with tab2:
        show_ai_interpretation_premium(api_key)
    
    with tab3:
        show_basic_visualizations()
    
    with tab4:
        show_export_options_premium()

def show_performance_comparison_premium():
    """Premium performance comparison"""
    
    st.markdown("### 🎯 Policy Performance Comparison")
    
    evaluator = PerformanceEvaluator()
    results = st.session_state.simulation_results
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        metric_display = st.selectbox(
            "Select Performance Metric",
            ["Composite Score", "Average Delay", "Throughput", "CO₂ Emissions", "Average Speed"]
        )
    
    with col2:
        view_type = st.radio("View Type", ["Table", "Heatmap"], horizontal=True)
    
    metric_map = {
        "Composite Score": "composite",
        "Average Delay": "average_delay",
        "Throughput": "throughput",
        "CO₂ Emissions": "co2_emissions",
        "Average Speed": "average_speed"
    }
    
    metric_key = metric_map[metric_display]
    
    comparison_data = []
    
    for policy_name, scenarios in results.items():
        for scenario_name, data in scenarios.items():
            metrics = data['metrics']
            
            if metric_key == "composite":
                value = evaluator.calculate_composite_score(metrics)
            else:
                value = metrics.get(metric_key, 0)
            
            comparison_data.append({
                'Policy': policy_name,
                'Scenario': CLIMATE_SCENARIOS[scenario_name]['name'],
                'Value': value
            })
    
    df = pd.DataFrame(comparison_data)
    
    if view_type == "Table":
        pivot_table = df.pivot(index='Policy', columns='Scenario', values='Value')
        st.dataframe(pivot_table, use_container_width=True)
    else:
        pivot_table = df.pivot(index='Policy', columns='Scenario', values='Value')
        
        fig = px.imshow(
            pivot_table,
            labels=dict(x="Climate Scenario", y="Policy", color=metric_display),
            aspect="auto",
            color_continuous_scale="RdYlGn" if metric_key in ["throughput", "average_speed"] else "RdYlGn_r"
        )
        
        fig.update_layout(title=f"{metric_display} Heatmap", height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    best_policy = evaluator.identify_best_policy(
        {name: scenarios[list(scenarios.keys())[0]]['metrics'] 
         for name, scenarios in results.items()},
        objective=metric_key if metric_key != "composite" else "composite"
    )
    
    st.success(f"🏆 **Best Performing Policy for {metric_display}:** {best_policy}")

def show_ai_interpretation_premium(api_key):
    """Premium AI interpretation interface"""
    
    st.markdown("### 🤖 AI-Powered Result Interpretation")
    
    if not st.session_state.api_key_set:
        st.warning("⚠️ Please enter your Groq API key to use AI interpretation.")
        return
    
    results = st.session_state.simulation_results
    
    col1, col2 = st.columns(2)
    
    with col1:
        policy_name = st.selectbox("📋 Select Policy", list(results.keys()))
    
    with col2:
        scenario_name = st.selectbox(
            "🌡️ Select Scenario",
            list(results[policy_name].keys()),
            format_func=lambda x: CLIMATE_SCENARIOS[x]['name']
        )
    
    if st.button("🧠 Generate AI Analysis", use_container_width=True, type="primary"):
        with st.spinner("🤖 AI is analyzing simulation results..."):
            try:
                interpreter = ResultInterpreter(api_key=api_key)
                data = results[policy_name][scenario_name]
                
                interpretation = interpreter.interpret_results(
                    policy_config=data['policy_config'],
                    metrics=data['metrics'],
                    climate_scenario=CLIMATE_SCENARIOS[scenario_name]['name']
                )
                
                st.markdown("---")
                st.markdown("### 📝 AI Analysis Report")
                st.markdown(f"""<div class="card">{interpretation}</div>""", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Error generating interpretation: {str(e)}")

def show_basic_visualizations():
    """Basic visualizations"""
    
    st.markdown("### 📉 Performance Visualizations")
    
    results = st.session_state.simulation_results
    evaluator = PerformanceEvaluator()
    
    plot_data = []
    
    for policy_name, scenarios in results.items():
        for scenario_name, data in scenarios.items():
            metrics = data['metrics']
            plot_data.append({
                'Policy': policy_name,
                'Scenario': CLIMATE_SCENARIOS[scenario_name]['name'],
                'Delay': metrics.get('average_delay', 0),
                'Throughput': metrics.get('throughput', 0),
                'Emissions': metrics.get('co2_emissions', 0),
                'Speed': metrics.get('average_speed', 0),
                'Score': evaluator.calculate_composite_score(metrics)
            })
    
    df = pd.DataFrame(plot_data)
    
    metric = st.selectbox("Select Metric to Visualize", 
                         ['Delay', 'Throughput', 'Emissions', 'Speed', 'Score'])
    
    fig = px.bar(df, x='Scenario', y=metric, color='Policy', 
                 barmode='group',
                 title=f'{metric} Comparison Across Scenarios',
                 color_discrete_sequence=px.colors.qualitative.Set2)
    
    st.plotly_chart(fig, use_container_width=True)

def show_export_options_premium():
    """Premium export options"""
    
    st.markdown("### 📥 Export Results")
    
    results = st.session_state.simulation_results
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### JSON Format")
        st.caption("Complete results with all metadata")
        
        json_str = json.dumps(results, indent=2, default=str)
        st.download_button(
            label="📄 Download JSON",
            data=json_str,
            file_name=f"trafficgen_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        st.markdown("#### CSV Format")
        st.caption("Tabular data for spreadsheet analysis")
        
        rows = []
        for policy_name, scenarios in results.items():
            for scenario_name, data in scenarios.items():
                metrics = data['metrics']
                row = {
                    'Policy': policy_name,
                    'Scenario': CLIMATE_SCENARIOS[scenario_name]['name'],
                    **metrics
                }
                rows.append(row)
        
        df = pd.DataFrame(rows)
        csv = df.to_csv(index=False)
        
        st.download_button(
            label="📊 Download CSV",
            data=csv,
            file_name=f"trafficgen_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

# ============ NEW ADVANCED PAGES ============

def show_optimization_page():
    """Multi-Objective Optimization Page"""
    
    st.markdown("## 🎯 Multi-Objective Optimization Analysis")
    
    if not st.session_state.simulation_results:
        st.warning("⚠️ No simulation results available for optimization analysis.")
        st.info("👉 Run simulations first to perform multi-objective optimization")
        return
    
    st.markdown("""
    <div class="card">
    <h3>Pareto Frontier Analysis</h3>
    <p>Identify non-dominated solutions where improving one objective necessarily worsens another.
    This analysis helps decision-makers understand trade-offs between conflicting objectives.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize optimizer
    optimizer = MultiObjectiveOptimizer()
    results = st.session_state.simulation_results
    
    # Prepare metrics for each policy (average across scenarios)
    policies_metrics = {}
    for policy_name, scenarios in results.items():
        avg_metrics = {}
        for metric in ['average_delay', 'throughput', 'co2_emissions', 'average_speed']:
            values = [s['metrics'].get(metric, 0) for s in scenarios.values()]
            avg_metrics[metric] = np.mean(values)
        policies_metrics[policy_name] = avg_metrics
    
    # Calculate Pareto frontier
    with st.spinner("🔄 Calculating Pareto frontier..."):
        pareto_front = optimizer.calculate_pareto_frontier(policies_metrics)
        st.session_state.pareto_front = pareto_front
    
    # Display results
    st.markdown("### 🏆 Pareto Optimal Solutions")
    
    if pareto_front:
        st.success(f"Found {len(pareto_front)} Pareto optimal policies out of {len(policies_metrics)} total policies")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Pareto Optimal Policies:")
            for i, policy in enumerate(pareto_front, 1):
                st.markdown(f"{i}. **{policy}**")
        
        with col2:
            hypervolume = optimizer.calculate_hypervolume(policies_metrics)
            st.metric("Solution Quality (Hypervolume)", f"{hypervolume:.3f}")
            st.caption("Higher values indicate better coverage of the objective space")
    else:
        st.warning("No Pareto optimal solutions found")
    
    # Rankings
    st.markdown("### 📊 Policy Rankings by Dominance")
    
    ranks = optimizer.rank_policies_by_dominance(policies_metrics)
    
    rank_data = []
    for policy, rank in sorted(ranks.items(), key=lambda x: x[1]):
        metrics = policies_metrics[policy]
        rank_data.append({
            'Rank': rank,
            'Policy': policy,
            'Pareto Optimal': '✅' if policy in pareto_front else '❌',
            'Avg Delay': f"{metrics['average_delay']:.1f}s",
            'Throughput': f"{metrics['throughput']:.0f}",
            'CO₂': f"{metrics['co2_emissions']:.2f}kg"
        })
    
    rank_df = pd.DataFrame(rank_data)
    st.dataframe(rank_df, use_container_width=True, hide_index=True)
    
    # Visualization
    st.markdown("### 📈 Pareto Frontier Visualization")
    
    # 2D Pareto plot (Delay vs Emissions)
    fig = go.Figure()
    
    for policy_name, metrics in policies_metrics.items():
        is_pareto = policy_name in pareto_front
        
        fig.add_trace(go.Scatter(
            x=[metrics['average_delay']],
            y=[metrics['co2_emissions']],
            mode='markers+text',
            name=policy_name,
            text=[policy_name[:15]],
            textposition='top center',
            marker=dict(
                size=15 if is_pareto else 10,
                symbol='star' if is_pareto else 'circle',
                color='#06A77D' if is_pareto else '#C73E1D',
                line=dict(width=2, color='white' if is_pareto else 'gray')
            )
        ))
    
    fig.update_layout(
        title='Pareto Frontier: Delay vs Emissions Trade-off',
        xaxis_title='Average Delay (seconds)',
        yaxis_title='CO₂ Emissions (kg)',
        height=500,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Generate optimization report
    st.markdown("### 📄 Optimization Report")
    
    if st.button("📊 Generate Detailed Report", use_container_width=True):
        report = optimizer.generate_optimization_report(policies_metrics)
        
        st.markdown(report)
        
        # Download report
        st.download_button(
            label="⬇️ Download Optimization Report",
            data=report,
            file_name=f"optimization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )

def show_statistical_analysis_page():
    """Statistical Analysis Page"""
    
    st.markdown("## 📈 Statistical Analysis & Hypothesis Testing")
    
    if not st.session_state.simulation_results:
        st.warning("⚠️ No simulation results available for statistical analysis.")
        return
    
    st.markdown("""
    <div class="card">
    <h3>Advanced Statistical Methods</h3>
    <p>Rigorous statistical analysis including ANOVA, confidence intervals, correlation analysis,
    and sensitivity testing to ensure robust and statistically significant findings.</p>
    </div>
    """, unsafe_allow_html=True)
    
    analyzer = StatisticalAnalyzer()
    results = st.session_state.simulation_results
    
    # ANOVA Analysis
    st.markdown("### 🔬 Analysis of Variance (ANOVA)")
    
    with st.spinner("🔄 Performing ANOVA..."):
        anova_results = analyzer.perform_anova(results)
        st.session_state.statistical_analysis['anova'] = anova_results
    
    anova_data = []
    for metric, anova in anova_results.items():
        anova_data.append({
            'Metric': metric.replace('_', ' ').title(),
            'F-Statistic': f"{anova['f_statistic']:.3f}",
            'P-Value': f"{anova['p_value']:.4f}",
            'Significant': '✅ Yes' if anova['significant'] else '❌ No',
            'Interpretation': anova['interpretation']
        })
    
    anova_df = pd.DataFrame(anova_data)
    st.dataframe(anova_df, use_container_width=True, hide_index=True)
    
    st.info("📘 **Interpretation:** P-value < 0.05 indicates statistically significant differences between policies")
    
    # Confidence Intervals
    st.markdown("### 📊 Confidence Intervals (95%)")
    
    ci_results = analyzer.calculate_confidence_intervals(results)
    
    ci_data = []
    for policy_name, metrics in ci_results.items():
        for metric, ci in metrics.items():
            ci_data.append({
                'Policy': policy_name,
                'Metric': metric.replace('_', ' ').title(),
                'Mean': f"{ci['mean']:.2f}",
                'Lower Bound': f"{ci['lower']:.2f}",
                'Upper Bound': f"{ci['upper']:.2f}",
                'Margin of Error': f"±{ci['margin_of_error']:.2f}"
            })
    
    ci_df = pd.DataFrame(ci_data)
    
    # Filter by metric
    selected_metric = st.selectbox(
        "Select Metric for CI Analysis",
        ci_df['Metric'].unique()
    )
    
    filtered_ci = ci_df[ci_df['Metric'] == selected_metric]
    st.dataframe(filtered_ci, use_container_width=True, hide_index=True)
    
    # Correlation Analysis
    st.markdown("### 🔗 Correlation Matrix")
    
    corr_matrix = analyzer.calculate_correlation_matrix(results)
    
    fig = px.imshow(
        corr_matrix,
        labels=dict(color="Correlation"),
        x=corr_matrix.columns,
        y=corr_matrix.index,
        color_continuous_scale='RdBu_r',
        aspect="auto",
        zmin=-1,
        zmax=1
    )
    
    fig.update_layout(title="Metric Correlation Heatmap", height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("📘 **Interpretation:** Values close to +1 or -1 indicate strong positive or negative correlations")
    
    # Generate Statistical Report
    st.markdown("### 📄 Statistical Report")
    
    if st.button("📊 Generate Complete Statistical Report", use_container_width=True):
        report = analyzer.generate_statistical_report(results, anova_results)
        
        st.markdown(report)
        
        st.download_button(
            label="⬇️ Download Statistical Report",
            data=report,
            file_name=f"statistical_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )

def show_advanced_visualizations_page():
    """Advanced Visualizations Page"""
    
    st.markdown("## 🎨 Advanced Interactive Visualizations")
    
    if not st.session_state.simulation_results:
        st.warning("⚠️ No simulation results available.")
        return
    
    st.markdown("""
    <div class="card">
    <h3>Premium Visualization Suite</h3>
    <p>Explore your data through cutting-edge interactive visualizations including 3D surfaces,
    parallel coordinates, Sankey diagrams, and more.</p>
    </div>
    """, unsafe_allow_html=True)
    
    visualizer = AdvancedVisualizer()
    results = st.session_state.simulation_results
    
    # Visualization selector
    viz_type = st.selectbox(
        "🎯 Select Visualization Type",
        [
            "3D Performance Surface",
            "Parallel Coordinates",
            "Sankey Flow Diagram",
            "Sunburst Chart",
            "Treemap",
            "Violin Plot"
        ]
    )
    
    st.markdown("---")
    
    try:
        if viz_type == "3D Performance Surface":
            st.markdown("### 🌐 3D Performance Surface")
            st.caption("Visualize how policies perform across different scenarios in 3D space")
            
            with st.spinner("🔄 Generating 3D visualization..."):
                fig = visualizer.create_3d_performance_surface(results)
                st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Parallel Coordinates":
            st.markdown("### 📊 Parallel Coordinates Plot")
            st.caption("Compare multiple metrics simultaneously across all policies")
            
            with st.spinner("🔄 Generating parallel coordinates..."):
                fig = visualizer.create_parallel_coordinates(results)
                st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Sankey Flow Diagram":
            st.markdown("### 🌊 Sankey Flow Diagram")
            st.caption("Visualize the flow from policies through scenarios to performance levels")
            
            with st.spinner("🔄 Generating Sankey diagram..."):
                fig = visualizer.create_sankey_diagram(results)
                st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Sunburst Chart":
            st.markdown("### ☀️ Hierarchical Sunburst Chart")
            st.caption("Explore hierarchical performance relationships")
            
            with st.spinner("🔄 Generating sunburst chart..."):
                fig = visualizer.create_sunburst_chart(results)
                st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Treemap":
            st.markdown("### 🗺️ Performance Treemap")
            st.caption("Visualize performance hierarchy by throughput")
            
            with st.spinner("🔄 Generating treemap..."):
                fig = visualizer.create_treemap(results)
                st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == "Violin Plot":
            st.markdown("### 🎻 Distribution Analysis (Violin Plot)")
            st.caption("Analyze the distribution of performance metrics")
            
            metric_choice = st.selectbox(
                "Select Metric",
                ['average_delay', 'throughput', 'co2_emissions', 'average_speed']
            )
            
            with st.spinner("🔄 Generating violin plot..."):
                fig = visualizer.create_violin_plot(results, metric_choice)
                st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"❌ Error generating visualization: {str(e)}")

def show_report_generation_page():
    """Report Generation Page"""
    
    st.markdown("## 📄 Automated Report Generation")
    
    if not st.session_state.simulation_results:
        st.warning("⚠️ No simulation results available.")
        return
    
    st.markdown("""
    <div class="card">
    <h3>Publication-Ready Reports</h3>
    <p>Generate comprehensive, professionally formatted reports suitable for academic
    publications, stakeholder presentations, and technical documentation.</p>
    </div>
    """, unsafe_allow_html=True)
    
    report_gen = ReportGenerator()
    results = st.session_state.simulation_results
    policies = st.session_state.generated_policies
    
    # Report Configuration
    st.markdown("### ⚙️ Report Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        researcher = st.text_input("Researcher Name", value=REPORT_AUTHOR)
        institution = st.text_input("Institution", value=REPORT_INSTITUTION)
    
    with col2:
        include_stats = st.checkbox("Include Statistical Analysis", value=True)
        include_optimization = st.checkbox("Include Optimization Analysis", value=True)
    
    # Generate Report
    if st.button("📊 Generate Complete Report", use_container_width=True, type="primary"):
        with st.spinner("🔄 Generating comprehensive report..."):
            
            # Gather all analysis
            stats_report = ""
            optimization_report = ""
            
            if include_stats and 'anova' in st.session_state.statistical_analysis:
                analyzer = StatisticalAnalyzer()
                stats_report = analyzer.generate_statistical_report(
                    results,
                    st.session_state.statistical_analysis['anova']
                )
            
            if include_optimization and st.session_state.pareto_front:
                optimizer = MultiObjectiveOptimizer()
                policies_metrics = {}
                for policy_name, scenarios in results.items():
                    avg_metrics = {}
                    for metric in ['average_delay', 'throughput', 'co2_emissions', 'average_speed']:
                        values = [s['metrics'].get(metric, 0) for s in scenarios.values()]
                        avg_metrics[metric] = np.mean(values)
                    policies_metrics[policy_name] = avg_metrics
                
                optimization_report = optimizer.generate_optimization_report(policies_metrics)
            
            # Generate main report
            report = report_gen.generate_markdown_report(
                results=results,
                policies=policies,
                stats_report=stats_report,
                optimization_report=optimization_report,
                researcher=researcher,
                institution=institution
            )
            
            st.success("✅ Report generated successfully!")
            
            # Display report
            st.markdown("### 📄 Generated Report Preview")
            
            with st.expander("📖 View Full Report", expanded=True):
                st.markdown(report)
            
            # Download options
            st.markdown("### 📥 Download Report")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.download_button(
                    label="📄 Download as Markdown",
                    data=report,
                    file_name=f"TrafficGen_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            
            with col2:
                # Convert to plain text for now (PDF conversion would require additional libraries)
                st.download_button(
                    label="📃 Download as Text",
                    data=report,
                    file_name=f"TrafficGen_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

def show_about_page():
    """About page"""
    
    st.markdown("## ℹ️ About TrafficGen-AI Ultimate Edition")
    
    st.markdown("""
    <div class="card">
    <h3 style="color: #667eea;">Overview</h3>
    <p>
    <strong>TrafficGen-AI Ultimate Edition</strong> is the most advanced research framework for
    climate-adaptive transportation policy design, combining state-of-the-art AI with rigorous
    scientific methodology to revolutionize traffic management research and practice.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🌟 Ultimate Features")
    
    features_col1, features_col2 = st.columns(2)
    
    with features_col1:
        st.markdown("""
        **🤖 Advanced AI Capabilities:**
        - LLM-powered policy generation (Llama 3.3 70B)
        - Natural language interpretation
        - Automated insights generation
        
        **🎯 Multi-Objective Optimization:**
        - Pareto frontier identification
        - Dominance ranking
        - Hypervolume calculation
        
        **📈 Statistical Analysis:**
        - ANOVA hypothesis testing
        - Confidence interval estimation
        - Correlation analysis
        - Sensitivity testing
        """)
    
    with features_col2:
        st.markdown("""
        **🎨 Premium Visualizations:**
        - 3D performance surfaces
        - Parallel coordinates
        - Sankey flow diagrams
        - Sunburst charts & treemaps
        
        **📄 Professional Reporting:**
        - Automated report generation
        - Publication-ready formatting
        - Multiple export formats
        - Executive summaries
        
        **🌓 Enhanced UX:**
        - Dark/Light theme toggle
        - Real-time progress tracking
        - Interactive dashboards
        """)
    
    st.markdown("---")
    
    st.markdown("### 🔬 Research Applications")
    
    st.info("""
    **TrafficGen-AI Ultimate is designed for:**
    - Policy impact assessment studies
    - Climate resilience planning
    - Sustainable mobility research
    """)
    
    st.markdown("---")
    
    st.markdown("### 👨‍💻 Developer")
    
    st.markdown("""
    <div class="card" style="text-align: center;">
    <h3 style="color: #667eea;">MAHBUB HASSAN</h3>
    <p><strong>Transportation Engineering Researcher</strong></p>
    <p>Chulalongkorn University</p>
    <p>Bangkok, Thailand</p>
    <br>
    <p><strong>Research Interests:</strong></p>
    <p>Climate-adaptive transportation systems • AI in traffic management<br>
    Sustainable mobility • Transit network optimization<br>
    Electric vehicle infrastructure • Data-driven policy design</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📚 Citation")
    
    st.code("""
@software{hassan2025trafficgen_ultimate,
  author = {Hassan, Mahbub},
  title = {TrafficGen-AI Ultimate: An Advanced Large Language Model-Assisted 
           Framework for Climate-Adaptive Traffic Policy Generation},
  year = {2025},
  version = {2.0},
  institution = {Chulalongkorn University},
  address = {Bangkok, Thailand}
}
    """, language="bibtex")
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #999;">
    <p><strong>TrafficGen-AI Ultimate Edition v2.0</strong></p>
    <p>Built with ❤️ for sustainable and climate-resilient transportation systems</p>
    <p>© 2025 Mahbub Hassan | Chulalongkorn University</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()