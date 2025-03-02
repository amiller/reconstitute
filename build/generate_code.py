#!/usr/bin/env python3
"""
Code generation script for LLM-built Calculator

This script loads prompt files and sends them to an LLM API to generate 
the application code files for the calculator project.
"""

import os
import sys
import argparse
import json
import requests
import time
from pathlib import Path
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

# Configuration
DEFAULT_MODEL = os.environ.get("LLM_MODEL", "gpt-4-turbo")
DEFAULT_API_ENDPOINT = os.environ.get("LLM_API_ENDPOINT", "https://api.openai.com/v1/chat/completions")
PROMPT_DIR = Path("prompts")
OUTPUT_DIR = Path("generated")

def read_prompt_file(prompt_path):
    """Read contents of a prompt file"""
    with open(prompt_path, 'r') as f:
        return f.read().strip()

def call_llm_api(prompt, system_message="You are a code generator for a calculator application.", model=None, api_key=None, endpoint=None):
    """Call the LLM API with the given prompt"""
    # Use parameters or defaults from .env
    model = model or DEFAULT_MODEL
    endpoint = endpoint or DEFAULT_API_ENDPOINT
    
    if not api_key:
        api_key = os.environ.get('LLM_API_KEY')
        if not api_key:
            raise ValueError("API key not provided. Set the LLM_API_KEY in your .env file or pass it as an argument.")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,  # Lower temperature for more consistent code generation
        "max_tokens": 4000
    }
    
    print(f"  Calling LLM API with model: {model}...")
    start_time = time.time()
    
    try:
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        elapsed_time = time.time() - start_time
        print(f"  API call completed in {elapsed_time:.2f} seconds")
        
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error calling LLM API: {e}")
        raise

def generate_html(prompt):
    """Generate HTML code based on prompt"""
    print("  Generating standalone HTML without prior context...")
    system_prompt = "Generate only the HTML code for a calculator. Respond with ONLY the complete HTML file, no explanations or markdown."
    full_prompt = f"{system_prompt}\n\n{prompt}"
    return call_llm_api(full_prompt)

def generate_javascript(prompt, html_context):
    """Generate JavaScript code based on prompt and HTML context"""
    print("  Generating JavaScript with HTML context...")
    system_prompt = "Generate only the JavaScript code for a calculator. Respond with ONLY the complete JavaScript file, no explanations or markdown."
    
    context = f"""
I'll provide you with the HTML structure of a calculator application followed by requirements
for implementing its JavaScript business logic. Make sure your JavaScript code properly 
interacts with the HTML elements by using the correct IDs and classes.

Here's the HTML structure:
```html
{html_context}
```

Now, here are the requirements for the JavaScript business logic:
"""
    
    full_prompt = f"{context}\n{prompt}"
    return call_llm_api(full_prompt, system_message=system_prompt)

def generate_css(prompt, html_context, js_context):
    """Generate CSS code based on prompt, HTML, and JS context"""
    print("  Generating CSS with HTML and JavaScript context...")
    system_prompt = "Generate only the CSS code for a calculator. Respond with ONLY the complete CSS file, no explanations or markdown."
    
    context = f"""
I'll provide you with the HTML and JavaScript code for a calculator application followed by
requirements for implementing its CSS styling. Make sure your CSS properly styles
the HTML elements by using the correct IDs, classes, and elements.

Here's the HTML structure:
```html
{html_context}
```

Here's the JavaScript code:
```javascript
{js_context}
```

Now, here are the requirements for the CSS styling:
"""
    
    full_prompt = f"{context}\n{prompt}"
    return call_llm_api(full_prompt, system_message=system_prompt)

def generate_tests(prompt, html_context, js_context, css_context):
    """Generate test code based on prompt and all previous context"""
    print("  Generating tests with full application context...")
    system_prompt = "Generate only JavaScript test code for a calculator. Respond with ONLY the complete test file, no explanations or markdown."
    
    context = f"""
I'll provide you with the complete implementation of a calculator application (HTML, JavaScript, and CSS)
followed by requirements for implementing tests. Make sure your tests properly validate
the calculator's functionality by checking all specified requirements.

Here's the HTML structure:
```html
{html_context}
```

Here's the JavaScript code:
```javascript
{js_context}
```

Here's the CSS code:
```css
{css_context}
```

Now, here are the requirements for the tests:
"""
    
    full_prompt = f"{context}\n{prompt}"
    return call_llm_api(full_prompt, system_message=system_prompt)

def extract_code(llm_response):
    """Extract code from LLM response, handling potential code blocks"""
    # If response has markdown code blocks, extract the content
    if "```" in llm_response:
        # Find code between first ``` and last ```
        start = llm_response.find("```") + 3
        # Skip language identifier if present
        if llm_response[start:start+10].strip() and "\n" in llm_response[start:start+20]:
            start = llm_response.find("\n", start) + 1
        end = llm_response.rfind("```")
        return llm_response[start:end].strip()
    return llm_response.strip()

def save_file(content, output_path):
    """Save generated content to file"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(content)
    print(f"  Saved: {output_path} ({len(content)} bytes)")

def read_generated_file(file_path):
    """Read a generated file if it exists, return empty string otherwise"""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def generate_config_files():
    """Generate all necessary configuration files after generating the main code"""
    
    # Add generation of configuration files
    config_files = [
        {"name": "babel.config.js", "prompt": "Generate a babel configuration file for a JavaScript project using Jest for testing."},
        {"name": "jest.config.js", "prompt": "Generate a Jest configuration file for testing a vanilla JavaScript project."},
        {"name": "package.json", "prompt": "Generate a package.json file with all necessary dependencies for a JavaScript project using Jest for testing."}
    ]
    
    for config in config_files:
        # Get API key from environment variables
        api_key = os.environ.get('LLM_API_KEY')
        
        # Use the same call_llm_api function that's used elsewhere in the script
        system_message = "You are a helpful assistant that generates configuration files."
        response_content = call_llm_api(
            config["prompt"], 
            system_message=system_message, 
            model=DEFAULT_MODEL, 
            api_key=api_key
        )
        
        with open(config["name"], "w") as file:
            file.write(response_content)

def main():
    parser = argparse.ArgumentParser(description="Generate calculator app code from prompts using LLM")
    parser.add_argument("--model", help=f"LLM model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("--api-key", help="LLM API key (default: from .env file)")
    parser.add_argument("--endpoint", help=f"API endpoint (default: {DEFAULT_API_ENDPOINT})")
    args = parser.parse_args()
    
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR / "tests", exist_ok=True)
    
    try:
        print("\n" + "="*80)
        print(" LLM-BUILT CALCULATOR - SEQUENTIAL CODE GENERATION")
        print("="*80 + "\n")
        
        print(f"Using LLM model: {DEFAULT_MODEL}")
        print(f"Output directory: {OUTPUT_DIR}")
        
        # Step 1: Generate HTML from UI prompt
        print("\n[STEP 1/4] Generating HTML from UI prompt")
        ui_prompt = read_prompt_file(PROMPT_DIR / "calculator-ui.prompt")
        print(f"  Read prompt from: {PROMPT_DIR / 'calculator-ui.prompt'}")
        html_content = generate_html(ui_prompt)
        html_content = extract_code(html_content)
        html_path = OUTPUT_DIR / "index.html"
        save_file(html_content, html_path)
        print("  HTML generation complete")
        
        # Step 2: Generate JavaScript with HTML context
        print("\n[STEP 2/4] Generating JavaScript with HTML context")
        logic_prompt = read_prompt_file(PROMPT_DIR / "business-logic.prompt")
        print(f"  Read prompt from: {PROMPT_DIR / 'business-logic.prompt'}")
        js_content = generate_javascript(logic_prompt, html_content)
        js_content = extract_code(js_content)
        js_path = OUTPUT_DIR / "app.js"
        save_file(js_content, js_path)
        print("  JavaScript generation complete")
        
        # Step 3: Generate CSS with HTML and JS context
        print("\n[STEP 3/4] Generating CSS with HTML and JavaScript context")
        style_prompt = read_prompt_file(PROMPT_DIR / "styling.prompt")
        print(f"  Read prompt from: {PROMPT_DIR / 'styling.prompt'}")
        css_content = generate_css(style_prompt, html_content, js_content)
        css_content = extract_code(css_content)
        css_path = OUTPUT_DIR / "style.css"
        save_file(css_content, css_path)
        print("  CSS generation complete")
        
        # Step 4: Generate tests with all previous context
        print("\n[STEP 4/4] Generating tests with full application context")
        test_prompt = read_prompt_file(PROMPT_DIR / "tests.prompt")
        print(f"  Read prompt from: {PROMPT_DIR / 'tests.prompt'}")
        test_content = generate_tests(test_prompt, html_content, js_content, css_content)
        test_content = extract_code(test_content)
        test_path = OUTPUT_DIR / "tests/calculator.test.js"
        save_file(test_content, test_path)
        print("  Test generation complete")
        
        # Generate configuration files
        generate_config_files()
        
        print("\n" + "="*80)
        print(" CODE GENERATION COMPLETED SUCCESSFULLY")
        print("="*80 + "\n")
        print("Generated files:")
        print(f"  - HTML: {html_path}")
        print(f"  - JavaScript: {js_path}")
        print(f"  - CSS: {css_path}")
        print(f"  - Tests: {test_path}")
        print("\nNext steps:")
        print("  1. Run 'make serve' to start a development server")
        print("  2. Run 'make test' to run the tests")
        
    except Exception as e:
        print(f"\nError during code generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 