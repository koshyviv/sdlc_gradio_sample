import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL')

PROMPTS = {
    "requirements_to_hld": """As a senior software architect, analyze these requirements and create a comprehensive high-level design. 
Include both textual description and a Graphviz diagram.

For the diagram, use dot notation. Wrap the diagram in ```dot tags.
Example diagram format:
```dot
digraph G {{
    A -> B;
    B -> C;
    B -> D;
}}
```

Requirements:
{requirements}

Format your response in this order:
1. System Architecture Overview (with Graphviz diagram)
2. Main Components
3. Data Flow
4. Technology Stack
5. Integration Points""",

    "hld_to_technical": """As a technical lead, convert this high-level design into a detailed technical specification.
Include both textual description and detailed technical diagrams using Graphviz.

Create diagrams for:
1. Component relationships
2. Data flow
3. Class diagram (if applicable)

Use ```dot notation for diagrams.

High-Level Design:
{hld}

Format your response with proper technical details, considerations, and relevant diagrams.""",

    "technical_to_code": """As a senior software developer, generate a complete codebase structure based on this technical design. Include:
1. Directory Structure
2. Main Code Files
3. Configuration Files
4. Test Cases
5. Documentation

Technical Design:
{technical_design}

Format your response as a detailed code implementation plan."""
}

SYSTEM_MESSAGES = {
    "requirements": "You are a senior business analyst helping to create clear and structured software requirements.",
    "hld": "You are a senior software architect creating high-level design documents.",
    "technical": "You are a technical lead creating detailed technical specifications.",
    "code": "You are a senior software developer generating production-ready code."
}
