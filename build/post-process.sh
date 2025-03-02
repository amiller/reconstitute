#!/bin/bash
# Post-processing script for LLM-generated code

set -e  # Exit on any error

# Directory settings
GENERATED_DIR="generated"
HTML_FILE="$GENERATED_DIR/index.html"
JS_FILE="$GENERATED_DIR/app.js"
CSS_FILE="$GENERATED_DIR/style.css"
TEST_DIR="$GENERATED_DIR/tests"

echo "Starting post-processing of generated code..."

# Check if files exist
if [ ! -f "$HTML_FILE" ] || [ ! -f "$JS_FILE" ] || [ ! -f "$CSS_FILE" ]; then
    echo "Error: Required generated files are missing. Run the generation script first."
    exit 1
fi

# Format HTML
if command -v html-beautify &> /dev/null; then
    echo "Formatting HTML..."
    html-beautify -r "$HTML_FILE"
else
    echo "html-beautify not found, skipping HTML formatting."
fi

# Format JavaScript
if command -v prettier &> /dev/null; then
    echo "Formatting JavaScript..."
    prettier --write "$JS_FILE"
    
    # Format tests if they exist
    if [ -d "$TEST_DIR" ]; then
        prettier --write "$TEST_DIR/*.js"
    fi
else
    echo "prettier not found, skipping JS formatting."
fi

# Format CSS
if command -v stylelint &> /dev/null; then
    echo "Linting CSS..."
    stylelint "$CSS_FILE" --fix
elif command -v prettier &> /dev/null; then
    echo "Formatting CSS with prettier..."
    prettier --write "$CSS_FILE"
else
    echo "CSS formatters not found, skipping CSS formatting."
fi

# Check HTML validity
if command -v html-validator &> /dev/null; then
    echo "Validating HTML..."
    html-validator --file "$HTML_FILE" || echo "HTML validation found issues that may need manual fixing."
else
    echo "html-validator not found, skipping HTML validation."
fi

# Bundle the files (if needed)
echo "Creating basic index.html if needed..."
# Ensure the HTML file has proper references to CSS and JS
if ! grep -q "app.js" "$HTML_FILE"; then
    echo "Fixing JS reference in HTML..."
    sed -i 's/<\/body>/<script src="app.js"><\/script>\n<\/body>/g' "$HTML_FILE"
fi

if ! grep -q "style.css" "$HTML_FILE"; then
    echo "Fixing CSS reference in HTML..."
    sed -i 's/<\/head>/<link rel="stylesheet" href="style.css">\n<\/head>/g' "$HTML_FILE"
fi

echo "Post-processing complete."

# Optionally start a test server
if [ "$1" == "--serve" ]; then
    if command -v python3 &> /dev/null; then
        echo "Starting a test server at http://localhost:8000"
        cd "$GENERATED_DIR" && python3 -m http.server
    elif command -v python &> /dev/null; then
        echo "Starting a test server at http://localhost:8000"
        cd "$GENERATED_DIR" && python -m http.server
    else
        echo "Python not found, cannot start test server."
    fi
fi 