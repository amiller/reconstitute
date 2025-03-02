# LLM-Built Calculator

A demonstration of LLM-built coding style, where application code is generated from natural language prompts using Large Language Models.

## Concept

This repository showcases a new coding paradigm where:
- The repository consists primarily of prompts and build scripts
- Application code is generated at build time by an LLM
- The prompts serve as the "true source code" of the application
- Changes to the application are made by modifying prompts, not the generated code

## Key Features

### Sequential Generation with Context Sharing

The code generation follows a sequential process where each step provides context to the next:

1. **HTML Generation**: First, the UI is generated from the UI prompt
2. **JavaScript Generation**: The business logic is generated with knowledge of the HTML structure
3. **CSS Generation**: The styling is generated with knowledge of both HTML and JavaScript
4. **Test Generation**: Tests are created with the full application context

This ensures that all parts of the application are aware of each other and properly integrated.

## Repository Structure

```
llm-calculator/
├── prompts/               # Natural language specifications
│   ├── calculator-ui.prompt    # UI specifications
│   ├── business-logic.prompt   # Calculator functionality
│   ├── styling.prompt          # Visual design and CSS
│   └── tests.prompt            # Test specifications
├── build/                 # Build system
│   ├── generate_code.py        # Code generation script
│   └── post-process.sh         # Post-processing script
├── Makefile               # Build orchestration
├── package.json           # JavaScript dependencies for testing
├── requirements.txt       # Python dependencies
├── .env                   # Configuration settings (API keys, etc.)
├── .env.template          # Template for .env file
├── generated/             # Generated code (not edited manually)
│   ├── index.html              # Generated HTML
│   ├── app.js                  # Generated JavaScript
│   ├── style.css               # Generated CSS
│   └── tests/                  # Generated tests
└── README.md              # This file
```

## Getting Started

### Prerequisites

- Python 3.6+
- LLM API key (from OpenAI or compatible service)
- Node.js and npm (for running tests)
- Optional: code formatting tools like `prettier`, `html-beautify`, etc.

### Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/llm-calculator.git
   cd llm-calculator
   ```

2. Set up the project:
   ```
   make setup
   ```
   This will create a `.env` file from the template.

3. Install Python dependencies:
   ```
   make install-deps
   ```
   This will install required packages from `requirements.txt`.

4. Install JavaScript testing dependencies:
   ```
   npm install
   ```
   This will install Jest and other test dependencies.

5. Edit the `.env` file to add your LLM API key:
   ```
   LLM_API_KEY=your_api_key_here
   ```

6. Optionally configure other settings in the `.env` file:
   ```
   # Use a different model
   LLM_MODEL=gpt-4
   
   # Use a different API endpoint
   LLM_API_ENDPOINT=https://your-endpoint.com/v1/chat/completions
   ```

### Building the Application

To generate the calculator application from prompts:

```
make build
```

This will:
1. Generate HTML from the UI prompt
2. Generate JavaScript with awareness of the HTML structure
3. Generate CSS with awareness of both HTML and JavaScript
4. Generate tests with awareness of the complete application
5. Post-process the generated files
6. Place the results in the `generated` directory

### Running the Application

To start a development server:

```
make serve
```

This will start a Python HTTP server at http://localhost:8000 where you can view and use the calculator.

### Running Tests

To run the tests for the calculator:

```
make test
```

or:

```
npm test
```

The tests are generated in the `generated/tests/` directory and test the calculator's functionality based on the requirements in the test prompt.

## Development Workflow

1. Modify prompt files in the `prompts/` directory to change application requirements
2. Run `make build` to regenerate the application code
3. Test the application using `make serve`
4. Run tests with `make test` to verify functionality
5. Iterate by adjusting prompts and regenerating

## Advanced Usage

### Changing LLM Model

To change the LLM model, edit the `LLM_MODEL` setting in your `.env` file:

```
LLM_MODEL=gpt-4
```

### Cleaning Generated Files

To remove all generated files:

```
make clean
```

## Contributing

This is a demonstration project. Feel free to fork and experiment with your own prompts and build processes.

## License

[MIT License](LICENSE)

## Acknowledgements

- This project demonstrates the concept of "LLM-built coding" as a new paradigm
- Inspired by various AI-assisted coding approaches and applications 