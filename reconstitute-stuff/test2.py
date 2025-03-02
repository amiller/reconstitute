from dataclasses import dataclass
from typing import List, Dict
import openai
from dotenv import load_dotenv
import os
import json
from openai import OpenAI

@dataclass
class SemanticSignature:
    """Represents the essential semantic information of a software component"""
    public_interfaces: List[str]
    type_definitions: List[str]
    critical_algorithms: List[Dict]
    dependency_refs: Dict[str, str]
    behavioral_constraints: List[str]

class AICompressor:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def compress(self, source_code: str) -> str:
        """Use GPT to analyze and compress code semantically"""
        prompt = f"""Analyze this code and create a semantic compression that captures:
1. Public interfaces (function and class signatures)
2. Type definitions
3. Critical algorithms and their patterns
4. Dependencies
5. Behavioral constraints (from docstrings and assertions)

Return a JSON object with these exact keys: 
{{
    "public_interfaces": [],
    "type_definitions": [],
    "critical_algorithms": [], 
    "dependency_refs": {{}},
    "behavioral_constraints": []
}}

Source code:
{source_code}
"""
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        # Parse the response into a SemanticSignature
        result = json.loads(response.choices[0].message.content)
        return SemanticSignature(**result)

class AIReconstructor:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def reconstruct(self, signature: SemanticSignature) -> str:
        """Reconstruct implementation from semantic signature"""
        prompt = """Given this semantic specification, generate complete Python code:

Public Interfaces:
{interfaces}

Type Definitions:
{types}

Critical Algorithms:
{algorithms}

Dependencies:
{deps}

Behavioral Constraints:
{constraints}

Generate idiomatic Python code that implements this specification.
Return only the implementation code without explanations."""

        # Format the components for the prompt
        interfaces = "\n".join(f"- {i}" for i in signature.public_interfaces)
        types = "\n".join(f"- {t}" for t in signature.type_definitions)
        algorithms = "\n".join(f"- {a}" for a in signature.critical_algorithms)
        deps = "\n".join(f"- {k}: {v}" for k, v in signature.dependency_refs.items())
        constraints = "\n".join(f"- {c}" for c in signature.behavioral_constraints)

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user", 
                "content": prompt.format(
                    interfaces=interfaces,
                    types=types,
                    algorithms=algorithms,
                    deps=deps,
                    constraints=constraints
                )
            }]
        )
        
        return response.choices[0].message.content

def main():
    # Sample code
    python_code = """
class RungeKutta4Solver:
    def __init__(self):
        self.t = 0
        self.y = 0
        self.h = 0.01  # Step size

    def derivative(self, t, y):
        # Example ODE: dy/dt = -2t*y 
        return -2 * t * y

    def step(self):
        # Classical RK4 implementation
        k1 = self.derivative(self.t, self.y)
        k2 = self.derivative(self.t + self.h/2, self.y + self.h*k1/2)
        k3 = self.derivative(self.t + self.h/2, self.y + self.h*k2/2)
        k4 = self.derivative(self.t + self.h, self.y + self.h*k3)
        
        # Update solution
        self.y += self.h * (k1 + 2*k2 + 2*k3 + k4) / 6
        self.t += self.h
        return self.t, self.y

    def solve_until(self, t_final, y0=1.0):
        # Initialize
        self.t = 0
        self.y = y0
        results = [(self.t, self.y)]
        
        # Solve step by step
        while self.t < t_final:
            t, y = self.step()
            results.append((t, y))
            
        return results

def test_rk4():
    # Create solver
    solver = RungeKutta4Solver()
    
    # Solve ODE: dy/dt = -2t*y from t=0 to t=2
    # Analytical solution: y = exp(-t²)
    results = solver.solve_until(2.0)
    
    # Compare with analytical solution
    for t, y_numerical in results[::20]:  # Print every 20th point
        y_analytical = math.exp(-t*t)
        print(f"t={t:.2f}, numerical={y_numerical:.6f}, analytical={y_analytical:.6f}, "
              f"error={abs(y_numerical-y_analytical):.2e}")
"""
    
    # Create compressor and reconstructor
    compressor = AICompressor()
    reconstructor = AIReconstructor()
    
    # Compress
    signature = compressor.compress(python_code)
    print("Semantic Signature:")
    print(json.dumps(signature.__dict__, indent=2))
    
    # Reconstruct
    reconstructed = reconstructor.reconstruct(signature)
    print("\nReconstructed Code:")
    print(reconstructed)

if __name__ == "__main__":
    main() 