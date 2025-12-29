"""
LLM-based Traffic Policy Generator
Uses Groq API to generate structured policy configurations
"""

import json
from groq import Groq
from config.settings import GROQ_API_KEY, GROQ_MODEL
from config.prompts import POLICY_GENERATION_PROMPT

class PolicyGenerator:
    """Generate traffic policy configurations using LLM"""
    
    def __init__(self, api_key=None):
        """
        Initialize the policy generator
        
        Args:
            api_key: Groq API key (optional, defaults to config)
        """
        self.api_key = api_key or GROQ_API_KEY
        if not self.api_key:
            raise ValueError("Groq API key not found. Please set GROQ_API_KEY in .env file")
        
        self.client = Groq(api_key=self.api_key)
        self.model = GROQ_MODEL
    
    def generate_policy(self, 
                       network_type: str,
                       climate_scenario: str,
                       policy_objective: str,
                       constraints: str = "None") -> dict:
        """
        Generate a traffic policy configuration
        
        Args:
            network_type: Type of network (e.g., "Urban arterial", "Highway corridor")
            climate_scenario: Climate stress level
            policy_objective: Main objective (e.g., "Minimize delay", "Reduce emissions")
            constraints: Additional constraints or requirements
            
        Returns:
            Dictionary containing policy configuration
        """
        
        # Format the prompt
        prompt = POLICY_GENERATION_PROMPT.format(
            network_type=network_type,
            climate_scenario=climate_scenario,
            policy_objective=policy_objective,
            constraints=constraints
        )
        
        try:
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a traffic engineering expert. Always respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Extract and parse response
            response_text = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()
            
            # Parse JSON
            policy_config = json.loads(response_text)
            
            # Add metadata
            policy_config["generation_metadata"] = {
                "network_type": network_type,
                "climate_scenario": climate_scenario,
                "policy_objective": policy_objective,
                "constraints": constraints,
                "model_used": self.model
            }
            
            return policy_config
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse LLM response as JSON: {e}\nResponse: {response_text}")
        except Exception as e:
            raise Exception(f"Error generating policy: {e}")
    
    def generate_multiple_policies(self,
                                   network_type: str,
                                   climate_scenario: str,
                                   policy_objectives: list,
                                   constraints: str = "None") -> list:
        """
        Generate multiple policy configurations for different objectives
        
        Args:
            network_type: Type of network
            climate_scenario: Climate stress level
            policy_objectives: List of policy objectives
            constraints: Additional constraints
            
        Returns:
            List of policy configurations
        """
        policies = []
        
        for objective in policy_objectives:
            try:
                policy = self.generate_policy(
                    network_type=network_type,
                    climate_scenario=climate_scenario,
                    policy_objective=objective,
                    constraints=constraints
                )
                policies.append(policy)
            except Exception as e:
                print(f"Warning: Failed to generate policy for objective '{objective}': {e}")
                continue
        
        return policies
    
    def validate_policy(self, policy: dict) -> tuple:
        """
        Validate policy configuration structure
        
        Args:
            policy: Policy configuration dictionary
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        required_fields = ["policy_name", "policy_type", "description", "parameters"]
        
        for field in required_fields:
            if field not in policy:
                return False, f"Missing required field: {field}"
        
        if not isinstance(policy["parameters"], dict):
            return False, "Parameters must be a dictionary"
        
        return True, "Policy configuration is valid"