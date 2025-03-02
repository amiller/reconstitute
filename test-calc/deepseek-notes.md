LLM-BUILT CODING STYLE

CONCEPT
LLM-built is a new coding paradigm where the repository consists primarily of prompts and build scripts. The prompts are detailed specifications that, when fed to an LLM during the build process, generate the actual application code.

REPO STRUCTURE
llm-calculator/
├── prompts/
│   ├── calculator-ui.prompt
│   ├── business-logic.prompt
│   ├── styling.prompt
│   └── tests.prompt
├── build/
│   ├── generate_code.py
│   └── post-process.sh
├── Makefile
└── generated/
    ├── index.html
    ├── app.js
    ├── style.css
    └── tests/

CORE COMPONENTS
Prompt Files: Natural language specifications that will be fed to LLM
Build Scripts: Orchestrate code generation and assembly
Makefile: Defines build pipeline with LLM invocation points
Generated Code: Never edited manually, always regenerated from prompts

KEY DESIGN PRINCIPLES
Prompt-Driven Development: All application code is generated from prompt files
Build-Time Generation: Code is created during build process, not checked into repo
Reproducible Builds: Same prompts + same LLM version = identical output
Prompt Versioning: Prompts are the true source code

SAMPLE WORKFLOW
1. User runs 'make build'
2. Makefile calls LLM API with prompts
3. Generated code is validated and assembled
4. Post-processing scripts apply final touches
5. Production-ready bundle is created

CALCULATOR-SPECIFIC CONSIDERATIONS
UI Prompts should specify:
  - Button layout (standard calculator grid)
  - Input/output display
  - Operation symbols
Business Logic Prompts:
  - Order of operations
  - Error handling
  - Edge cases (division by zero, decimal points)
Styling Prompts:
  - Mobile-responsive design
  - Theme system
  - Interactive states

EXAMPLE PROMPT STRUCTURE (calculator-ui.prompt)
Generate a HTML5 calculator interface with:
- Display screen at top showing current input and result
- Grid layout with 4 columns
- Number buttons 0-9
- Operation buttons: +, -, ×, ÷
- Additional buttons: . (decimal), =, C (clear), ± (negate)
- ARIA accessibility labels
- Semantic HTML structure

BUILD PROCESS CHALLENGES
Ensuring LLM output consistency
Handling API rate limits/costs
Validation of generated code
Version pinning for LLM model
Caching strategies for development
