import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL')

PROMPTS = {
    "requirements_to_hld": """As a senior embedded systems architect, analyze these requirements and create a comprehensive high-level design for an embedded software system. 
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
4. Hardware Interfaces
5. Technology Stack
6. Integration Points""",

    "hld_to_technical": """As a technical lead for embedded systems, convert this high-level design into a detailed technical specification.
Include both textual description and detailed technical diagrams using Graphviz.

Create diagrams for:
1. Component relationships
2. Data flow
3. Hardware interfaces
4. Class diagram (if applicable)

Use ```dot notation for diagrams.

High-Level Design:
{hld}

Format your response with proper technical details, considerations, and relevant diagrams.""",

    "technical_to_code": '''As a senior embedded software developer, generate a complete C++ codebase structure based on this technical design.
Format your response as a valid JSON object containing file paths and their contents.

Technical Design:
{technical_design}

Expected format example:
{{
    "src/main.cpp": "#include <iostream>\\nint main() {{\\n    return 0;\\n}}\\n",
    "include/project_name.h": "#pragma once\\n\\n// Header content\\n",
    "src/project_name.cpp": "// Implementation\\n",
    "CMakeLists.txt": "cmake_minimum_required(VERSION 3.10)\\n",
    "README.md": "# Project\\n"
}}

Note: Use proper C++ coding standards and include necessary header guards, error handling, and initialization.
Generate complete, compilable code for an embedded system.
'''
}

SYSTEM_MESSAGES = {
    "requirements": "You are a senior business analyst helping to create clear and structured software requirements for embedded systems.",
    "hld": "You are a senior embedded systems architect creating high-level design documents.",
    "technical": "You are a technical lead creating detailed technical specifications for embedded systems.",
    "code": "You are a senior embedded software developer generating production-ready C++ code."
}
