"""
LLM Prompt templates for policy generation and interpretation
"""

POLICY_GENERATION_PROMPT = """You are a traffic engineering expert specializing in climate-adaptive transportation policy design.

**Task**: Generate a structured traffic policy configuration based on the given objectives and constraints.

**Context**:
- Network Type: {network_type}
- Climate Scenario: {climate_scenario}
- Policy Objective: {policy_objective}
- Additional Constraints: {constraints}

**Policy Types Available**:
1. Signal Timing Optimization (cycle length, green splits, offsets)
2. Road Pricing Strategy (toll amounts, time-based pricing, zones)
3. Access Restriction (vehicle types, time windows, zones)
4. Speed Management (speed limits, variable speed zones)
5. Lane Management (HOV lanes, bus lanes, dynamic allocation)

**Requirements**:
- Policy must be feasible and implementable
- Consider climate stress impacts (capacity reduction, efficiency loss)
- Balance multiple objectives (delay, emissions, throughput)
- Provide specific, measurable parameters

**Output Format** (JSON):
{{
    "policy_name": "Descriptive policy name",
    "policy_type": "One of the policy types listed above",
    "description": "Brief description of the policy strategy",
    "parameters": {{
        "key1": value1,
        "key2": value2
    }},
    "expected_impacts": {{
        "delay": "expected change",
        "emissions": "expected change",
        "throughput": "expected change"
    }},
    "implementation_notes": "Practical considerations for implementation"
}}

Generate ONE comprehensive policy configuration that addresses the stated objective under the given climate scenario.
"""

INTERPRETATION_PROMPT = """You are a traffic engineering analyst providing insights on simulation results.

**Simulation Results**:
{results_summary}

**Policy Configuration**:
{policy_config}

**Climate Scenario**: {climate_scenario}

**Task**: Provide a clear, evidence-based interpretation of these results.

**Your analysis should include**:
1. **Performance Summary**: Key findings from the metrics
2. **Trade-off Analysis**: Identify any conflicts between objectives (e.g., reduced delay vs. higher emissions)
3. **Climate Resilience**: How well the policy performs under climate stress
4. **Practical Insights**: Actionable recommendations for policy refinement

**Important**:
- Base your interpretation ONLY on the provided simulation data
- Be specific and quantitative when discussing changes
- Avoid speculation beyond what the data shows
- Use professional, technical language appropriate for transportation planners

Provide your interpretation in a clear, structured format.
"""

POLICY_COMPARISON_PROMPT = """You are comparing multiple traffic policies under different climate scenarios.

**Policies Evaluated**:
{policies_summary}

**Performance Across Scenarios**:
{performance_data}

**Task**: Provide a comparative analysis highlighting:
1. Which policy performs best under each climate scenario
2. Which policy is most robust across all scenarios
3. Key trade-offs between policies
4. Recommendations for policy selection based on priorities

Focus on data-driven insights and practical implications for decision-makers.
"""