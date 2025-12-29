# 🚦 TrafficGen-AI Ultimate Edition

**Advanced AI-Powered Climate-Adaptive Traffic Policy Generation and Analysis Platform**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Research](https://img.shields.io/badge/Research-Grade-purple.svg)](https://github.com/mahbubchula)

A cutting-edge research framework that integrates Large Language Models with traffic microsimulation, multi-objective optimization, and advanced statistical analysis to revolutionize climate-adaptive transportation policy design.

---

## 🌟 Ultimate Features

### 🤖 **Advanced AI Capabilities**
- **LLM-Powered Policy Generation** using Llama 3.3 70B via Groq API
- **Natural Language Interpretation** of simulation results
- **Automated Insights Generation** with context-aware recommendations
- **Multi-Agent Optimization** for policy refinement

### 🎯 **Multi-Objective Optimization**
- **Pareto Frontier Analysis** to identify non-dominated solutions
- **Dominance Ranking** for policy comparison
- **Hypervolume Calculation** for solution quality assessment
- **Trade-off Visualization** between conflicting objectives

### 📈 **Statistical Analysis Suite**
- **ANOVA Hypothesis Testing** for policy significance
- **Confidence Interval Estimation** (95% CI)
- **Correlation Analysis** between performance metrics
- **Sensitivity Testing** for parameter variations

### 🌡️ **Climate Scenario Modeling**
- **4 Climate Stress Levels**: Baseline, Moderate, Severe, Extreme
- **Capacity Reduction Modeling** (0-45% reduction)
- **Efficiency Loss Simulation** (0-35% degradation)
- **Emission Factor Adjustment** (1.0x - 1.5x increase)

### 🎨 **Premium Visualizations**
- **3D Performance Surfaces** for spatial analysis
- **Parallel Coordinates** for multi-metric comparison
- **Sankey Flow Diagrams** for relationship visualization
- **Sunburst Charts** for hierarchical data
- **Treemaps** for performance hierarchy
- **Violin Plots** for distribution analysis
- **Animated Timelines** showing evolution
- **Interactive Heatmaps** with drill-down capabilities

### 📄 **Professional Reporting**
- **Automated Report Generation** with publication-ready formatting
- **Executive Summaries** for stakeholders
- **Methodology Documentation** for reproducibility
- **Multi-Format Export** (Markdown, Text, CSV, JSON)

### 🌓 **Enhanced User Experience**
- **Dark/Light Theme Toggle** for visual comfort
- **Real-Time Progress Tracking** during simulations
- **Interactive Dashboards** with comprehensive analytics
- **One-Click Export** to multiple formats
- **Session Statistics** tracking

---

## 🎯 Use Cases

- **PhD and Master's Research** in transportation engineering
- **Q1 Journal Publication** preparation
- **International Conference Presentations**
- **Climate Resilience Planning** for cities
- **Policy Impact Assessment** studies
- **Sustainable Mobility Research**
- **Transportation Infrastructure Planning**
- **Academic Teaching** and demonstrations

---

## 🛠️ Installation

### Prerequisites

- **Python 3.8+** (recommended: Python 3.11)
- **Groq API Key** ([Get one free here](https://console.groq.com/))
- **SUMO** (Optional - for full simulation capabilities)
- **Git** for version control

### Quick Setup

1. **Clone the repository**
```bash
git clone https://github.com/mahbubchula/TrafficGen-AI.git
cd TrafficGen-AI
```

2. **Create virtual environment** (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

Replace `your_groq_api_key_here` with your actual Groq API key.

5. **Run the application**
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## 📖 Complete User Guide

### 1️⃣ **Policy Generation**

1. Navigate to **"🔧 Policy Generation"** page
2. Configure your policy:
   - Select network type (Urban Arterial, Highway, Grid, etc.)
   - Choose climate scenario (Baseline, Moderate, Severe, Extreme)
   - Define policy objective (Minimize delay, Reduce emissions, etc.)
   - Add constraints (budget, timeline, restrictions)
3. Click **"🚀 Generate Policy with AI"**
4. Review AI-generated policy configuration
5. Generate multiple policies for comparison

### 2️⃣ **Simulation & Evaluation**

1. Navigate to **"⚡ Simulation & Evaluation"**
2. Select policies to evaluate (multi-select)
3. Choose climate scenarios for testing
4. Configure simulation parameters:
   - Simulation time (600-7200 seconds)
   - Number of vehicles (50-1000)
   - Number of runs for averaging
5. Click **"▶️ Run Simulation"**
6. Monitor real-time progress
7. Review performance summary

### 3️⃣ **Results Analysis**

Navigate to **"📊 Results Analysis"** for:
- **Performance Comparison** across policies and scenarios
- **AI-Powered Interpretation** with natural language insights
- **Interactive Visualizations** (bar charts, heatmaps)
- **Export Options** (JSON, CSV)

### 4️⃣ **Multi-Objective Optimization**

Navigate to **"🎯 Multi-Objective Optimization"** to:
- Identify **Pareto optimal solutions**
- View **dominance rankings**
- Analyze **trade-offs** between objectives
- Calculate **hypervolume** for solution quality
- Download **optimization reports**

### 5️⃣ **Statistical Analysis**

Navigate to **"📈 Statistical Analysis"** for:
- **ANOVA testing** for policy significance
- **Confidence intervals** (95% CI)
- **Correlation matrices** between metrics
- **Statistical reports** with interpretations

### 6️⃣ **Advanced Visualizations**

Navigate to **"🎨 Advanced Visualizations"** to explore:
- **3D Performance Surfaces**
- **Parallel Coordinates**
- **Sankey Diagrams**
- **Sunburst Charts**
- **Treemaps**
- **Violin Plots**

### 7️⃣ **Report Generation**

Navigate to **"📄 Report Generation"** to:
- Configure report metadata (researcher, institution)
- Include statistical analysis
- Include optimization results
- Generate comprehensive markdown reports
- Download publication-ready documents

---

## 🏗️ Project Structure
```
TrafficGen-AI/
├── app.py                          # Main Streamlit application (Ultimate Edition)
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── .gitignore                      # Git ignore rules
├── .env                           # Environment variables (API keys)
│
├── modules/                       # Core functionality modules
│   ├── __init__.py
│   ├── policy_generator.py        # LLM-based policy generation
│   ├── climate_scenarios.py       # Climate stress modeling
│   ├── sumo_simulator.py          # Traffic simulation interface
│   ├── evaluator.py               # Performance evaluation
│   ├── interpreter.py             # Result interpretation
│   ├── optimizer.py               # Multi-objective optimization (NEW)
│   ├── analytics.py               # Statistical analysis (NEW)
│   ├── report_generator.py        # Automated reports (NEW)
│   └── advanced_visualizations.py # Premium charts (NEW)
│
├── config/                        # Configuration files
│   ├── __init__.py
│   ├── settings.py                # Application settings
│   └── prompts.py                 # LLM prompt templates
│
├── sumo_networks/                 # SUMO network files
└── assets/                        # Static assets (images, etc.)
```

---

## 🔬 Methodology

### **1. Policy Generation Framework**
- Uses Groq API with Llama 3.3 70B model
- Generates structured JSON policy configurations
- Validates policy parameters and constraints
- Context-aware prompting for climate scenarios

### **2. Climate Stress Scenarios**

| Scenario | Capacity Reduction | Efficiency Loss | Emission Factor |
|----------|-------------------|-----------------|-----------------|
| **Baseline** | 0% | 0% | 1.00x |
| **Moderate** | 15% | 10% | 1.15x |
| **Severe** | 30% | 20% | 1.30x |
| **Extreme** | 45% | 35% | 1.50x |

### **3. Performance Metrics**
- **Average Delay** (seconds) - Lower is better
- **Throughput** (vehicles/hour) - Higher is better
- **CO₂ Emissions** (kg) - Lower is better
- **Average Speed** (km/h) - Higher is better
- **Total Travel Time** (hours) - Lower is better
- **Composite Score** (0-100) - Weighted aggregate

### **4. Statistical Methods**
- **ANOVA** (Analysis of Variance) for hypothesis testing
- **95% Confidence Intervals** for uncertainty quantification
- **Pearson Correlation** for metric relationships
- **Sensitivity Analysis** for parameter impact

### **5. Multi-Objective Optimization**
- **Pareto Frontier** identification
- **Dominance-based ranking**
- **Hypervolume indicator** for solution quality
- **Trade-off analysis** visualization

---

## 📊 Sample Output

### **Generated Policy Example**
```json
{
  "policy_name": "Adaptive Signal Optimization for Climate Resilience",
  "policy_type": "Signal Timing Optimization",
  "description": "Dynamic signal timing adjusted for climate stress with predictive capabilities",
  "parameters": {
    "cycle_length": 90,
    "green_split_main": 0.65,
    "green_split_minor": 0.35,
    "offset_optimization": true,
    "adaptive_threshold": 0.8
  },
  "expected_impacts": {
    "delay": "15-20% reduction under moderate stress",
    "emissions": "10-12% reduction",
    "throughput": "8-10% improvement"
  },
  "implementation_notes": "Requires adaptive traffic signal controllers with real-time data integration"
}
```

### **Performance Results Table**

| Policy | Scenario | Avg Delay (s) | Throughput (veh/h) | CO₂ (kg) | Score |
|--------|----------|---------------|-------------------|----------|-------|
| Adaptive Signals | Baseline | 42.3 | 1245 | 387.2 | 87.5 |
| Adaptive Signals | Moderate | 51.8 | 1156 | 421.6 | 79.2 |
| Road Pricing | Baseline | 38.7 | 1089 | 342.5 | 82.1 |
| Access Control | Severe | 67.4 | 987 | 478.3 | 68.9 |

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create your feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### **Areas for Contribution**
- Real SUMO network integration
- Additional visualization types
- Machine learning model integration
- Real-time traffic data APIs
- Multi-language support
- Mobile responsiveness improvements

---

## 📝 Research & Citation

This framework supports cutting-edge research on climate-adaptive transportation systems. If you use **TrafficGen-AI Ultimate Edition** in your research, please cite:
```bibtex
@software{hassan2025trafficgen_ultimate,
  author = {Hassan, Mahbub},
  title = {TrafficGen-AI Ultimate: An Advanced Large Language Model-Assisted 
           Framework for Climate-Adaptive Traffic Policy Generation and 
           Microsimulation-Based Evaluation},
  year = {2025},
  version = {2.0},
  publisher = {GitHub},
  institution = {Chulalongkorn University},
  address = {Bangkok, Thailand},
  url = {https://github.com/mahbubchula/TrafficGen-AI}
}
```

---

## ⚠️ Limitations & Disclaimers

### **Current Limitations**
- Simplified network representations in current implementation
- Synthetic simulation data for demonstration purposes
- LLM output variability requires human oversight
- Single replication per scenario (future: Monte Carlo)
- Limited to predefined climate stress parameters

### **Important Notes**
- This tool is for **research and educational purposes**
- Requires domain expertise for policy implementation
- Not intended for direct operational deployment without validation
- Policies should be reviewed by qualified traffic engineers
- Climate scenarios are based on literature estimates

### **Future Enhancements**
- Real SUMO network file support
- Integration with real-world traffic datasets
- Multi-objective optimization with genetic algorithms
- Expanded climate modeling approaches
- Real-time policy adaptation capabilities
- Cloud-based distributed simulation

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### **MIT License Summary**
- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ✅ Private use allowed
- ⚠️ Liability and warranty limitations apply

---

## 👨‍🔬 Author & Developer

### **Mahbub Hassan**
**Transportation Engineering Researcher**  
Chulalongkorn University, Bangkok, Thailand

#### **Research Interests**
- Climate-adaptive transportation systems
- AI applications in traffic management
- Sustainable mobility solutions
- Transit network optimization
- Electric vehicle infrastructure
- Data-driven policy design

#### **Connect**
- 📧 Email: mahbub.hassan@ieee.org
- 🔗 GitHub: [@mahbubchula](https://github.com/mahbubchula)
- 📚 Google Scholar: [Mahbub Hassan](https://scholar.google.com/)
- 💼 LinkedIn: [Mahbub Hassan](https://linkedin.com/)
- 🎓 ResearchGate: [Mahbub Hassan](https://researchgate.net/)

---

## 🙏 Acknowledgments

Special thanks to:

- **[Groq](https://groq.com/)** for providing fast LLM inference API
- **[SUMO Development Team](https://eclipse.dev/sumo/)** for the traffic simulation platform
- **[Streamlit](https://streamlit.io/)** for the amazing web framework
- **[Plotly](https://plotly.com/)** for interactive visualizations
- **Chulalongkorn University** for research support and resources
- **Transportation Engineering Community** for valuable feedback

---

## 📧 Support & Contact

### **For Questions or Issues**
- 🐛 **Bug Reports**: [Open an issue](https://github.com/mahbubchula/TrafficGen-AI/issues)
- 💡 **Feature Requests**: [Start a discussion](https://github.com/mahbubchula/TrafficGen-AI/discussions)
- 📧 **Email**: mahbub.hassan@ieee.org

### **For Collaboration**
Interested in collaboration on:
- Research projects
- Academic publications
- Tool development
- Data sharing

Please reach out via email with your proposal!

---

## 🌍 Impact & Applications

**TrafficGen-AI Ultimate Edition** has been designed to support:

### **Academic Research**
- PhD dissertations on climate-adaptive transportation
- Master's theses on AI in traffic management
- Journal publications (Q1/Q2 target)
- Conference presentations (IEEE, TRB, etc.)

### **Policy & Planning**
- Urban transportation planning
- Climate resilience strategies
- Sustainable mobility policies
- Infrastructure investment decisions

### **Education**
- Graduate-level transportation courses
- AI and optimization workshops
- Traffic simulation training
- Research methodology demonstrations

---

## 🚀 Quick Start Checklist

- [ ] Install Python 3.8+
- [ ] Clone repository
- [ ] Create virtual environment
- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Get Groq API key from https://console.groq.com/
- [ ] Create `.env` file with API key
- [ ] Run `streamlit run app.py`
- [ ] Generate first policy
- [ ] Run simulation
- [ ] Explore visualizations
- [ ] Generate report
- [ ] Star the repository ⭐

---

## 📈 Version History

### **v2.0 - Ultimate Edition** (Current)
- ✨ Multi-objective optimization with Pareto analysis
- ✨ Statistical analysis suite (ANOVA, CI, correlation)
- ✨ Advanced visualizations (3D, Sankey, Parallel Coordinates)
- ✨ Automated report generation
- ✨ Dark/Light theme toggle
- ✨ Enhanced UI/UX with animations

### **v1.0 - Initial Release**
- 🎉 LLM-based policy generation
- 🎉 Climate scenario modeling
- 🎉 SUMO integration
- 🎉 Basic visualizations
- 🎉 Performance evaluation

---

<div align="center">

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=mahbubchula/TrafficGen-AI&type=Date)](https://star-history.com/#mahbubchula/TrafficGen-AI&Date)

---

### Built with ❤️ for sustainable and climate-resilient transportation systems

**© 2025 Mahbub Hassan | Chulalongkorn University**

**TrafficGen-AI Ultimate Edition v2.0**

[⬆ Back to Top](#-trafficgen-ai-ultimate-edition)

</div>