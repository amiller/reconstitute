# Makefile for LLM-built Calculator

.PHONY: all clean build generate process serve deps-check env-check setup install-deps test

# Configuration
PYTHON = python3
SHELL = /bin/bash
GENERATED_DIR = generated
BUILD_DIR = build
PROMPT_DIR = prompts
ENV_FILE = .env
ENV_TEMPLATE = .env.template
REQUIREMENTS_FILE = requirements.txt
TEST_DIR = $(GENERATED_DIR)/tests

# Default target
all: build

# Install Python dependencies
install-deps:
	@echo "Installing Python dependencies..."
	@$(PYTHON) -m pip install -r $(REQUIREMENTS_FILE)
	@echo "Dependencies installed successfully"

# Check for required dependencies
deps-check:
	@echo "Checking dependencies..."
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo "Python 3 is required but not installed. Aborting."; exit 1; }
	@echo "Python OK. Run 'make install-deps' to install required packages."

# Check for LLM_API_KEY environment variable
env-check:
	@if [ -z "$$LLM_API_KEY" ]; then \
		echo "LLM_API_KEY environment variable is not set."; \
		echo "Please set the LLM_API_KEY environment variable before proceeding."; \
		exit 1; \
	fi
	@echo "LLM_API_KEY is set. Proceeding..."

# Make scripts executable
scripts-executable:
	@chmod +x $(BUILD_DIR)/generate_code.py
	@chmod +x $(BUILD_DIR)/post-process.sh

# Setup project
setup: deps-check env-check scripts-executable
	@echo "Project setup completed"
	@echo "Run 'make install-deps' to install Python dependencies"

# Generate code from prompts
generate: setup
	@echo "Generating code from prompts..."
	@$(BUILD_DIR)/generate_code.py
	@echo "Code generation completed"

# Process generated code
process: generate
	@echo "Post-processing generated code..."
	@$(BUILD_DIR)/post-process.sh
	@echo "Post-processing completed"

# Full build process
build: process
	@echo "Build completed successfully"
	@echo "Generated files are in the '$(GENERATED_DIR)' directory"
	@echo "Run 'make serve' to start a development server"

# Start development server
serve:
	@echo "Starting development server..."
	@$(BUILD_DIR)/post-process.sh --serve

# Run tests
test:
	@echo "Running calculator tests..."
	@if [ ! -d "$(TEST_DIR)" ]; then \
		echo "Test directory not found. Run 'make build' first to generate tests."; \
		exit 1; \
	fi
	@if command -v npm &> /dev/null && [ -f "package.json" ]; then \
		echo "Using npm to run tests..."; \
		npm test; \
	elif command -v jest &> /dev/null; then \
		echo "Using Jest to run tests..."; \
		jest $(TEST_DIR); \
	elif command -v mocha &> /dev/null; then \
		echo "Using Mocha to run tests..."; \
		mocha $(TEST_DIR); \
	else \
		echo "No JavaScript test runner found."; \
		echo "Please install Jest or Mocha to run tests:"; \
		echo "  npm install -g jest"; \
		echo "  - OR -"; \
		echo "  npm install -g mocha"; \
		exit 1; \
	fi

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	@rm -rf $(GENERATED_DIR)/*
	@echo "Clean completed"

# Show help
help:
	@echo "LLM-built Calculator Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  make setup        - Setup project (check dependencies and environment variables)"
	@echo "  make install-deps - Install required Python dependencies"
	@echo "  make build        - Generate and process all code (default)"
	@echo "  make generate     - Generate code from prompts"
	@echo "  make process      - Post-process the generated code"
	@echo "  make serve        - Start a development server"
	@echo "  make test         - Run the calculator tests"
	@echo "  make clean        - Remove all generated files"
	@echo "  make help         - Show this help message"
	@echo ""
	@echo "Configuration:"
	@echo "  Set the LLM_API_KEY environment variable to your API key"
	@echo ""
	@echo "Example usage:"
	@echo "  make setup        # First time setup"
	@echo "  make install-deps # Install dependencies"
	@echo "  make build        # Build the calculator application"
	@echo "  make test         # Run tests" 