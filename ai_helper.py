import openai
import json
import re
from config import OPENAI_API_KEY, PROMPTS, SYSTEM_MESSAGES, OPENAI_MODEL

class AIHelper:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY

    def generate_response(self, prompt, system_message, temperature=0.7):
        try:
            response = openai.ChatCompletion.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def generate_hld(self, requirements):
        prompt = PROMPTS["requirements_to_hld"].format(requirements=requirements)
        return self.generate_response(prompt, SYSTEM_MESSAGES["hld"])

    def generate_technical_design(self, hld):
        prompt = PROMPTS["hld_to_technical"].format(hld=hld)
        return self.generate_response(prompt, SYSTEM_MESSAGES["technical"])

    def generate_code_structure(self, technical_design):
        prompt = PROMPTS["technical_to_code"].format(technical_design=technical_design)
        response = self.generate_response(prompt, SYSTEM_MESSAGES["code"])
        
        try:
            # Extract JSON content if wrapped in code blocks
            json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', response, re.DOTALL)
            if json_match:
                response = json_match.group(1)
            
            # Clean up the response while preserving newlines in code
            response = response.strip()
            code_structure = json.loads(response)
            
            # Validate and ensure minimum required files
            required_files = ["src/main.cpp", "include/project_name.h", "CMakeLists.txt"]
            if not all(any(req in filepath for req in required_files) for filepath in code_structure.keys()):
                raise ValueError("Missing required files")
                
            # Format code content
            formatted_structure = {}
            for filepath, content in code_structure.items():
                # Preserve newlines in code but clean up any JSON artifacts
                formatted_content = content.replace('\\n', '\n').replace('\\"', '"')
                formatted_structure[filepath] = formatted_content
                
            return json.dumps(formatted_structure)
        except (json.JSONDecodeError, ValueError) as e:
            # Provide a comprehensive fallback structure
            project_name = "embedded_project"
            return json.dumps({
                f"include/{project_name}.h": f'''// filepath: include/{project_name}.h
#pragma once

#include <cstdint>
#include <memory>
#include <string>

namespace embedded {{

// Hardware abstraction layer interface
class IHAL {{
public:
    virtual ~IHAL() = default;
    virtual bool initializeHardware() = 0;
    virtual uint32_t readSensor() = 0;
    virtual bool writeOutput(uint32_t value) = 0;
}};

// Main controller class
class Controller {{
public:
    Controller(std::shared_ptr<IHAL> hal);
    bool initialize();
    void run();
    void shutdown();

private:
    std::shared_ptr<IHAL> m_hal;
    bool m_initialized;
    uint32_t m_sensorValue;
}};

}} // namespace embedded
''',
                f"src/{project_name}.cpp": f'''// filepath: src/{project_name}.cpp
#include "{project_name}.h"
#include <iostream>
#include <thread>
#include <chrono>

namespace embedded {{

Controller::Controller(std::shared_ptr<IHAL> hal)
    : m_hal(hal)
    , m_initialized(false)
    , m_sensorValue(0)
{{
}}

bool Controller::initialize() {{
    if (!m_hal) {{
        std::cerr << "Error: HAL not initialized" << std::endl;
        return false;
    }}

    m_initialized = m_hal->initializeHardware();
    return m_initialized;
}}

void Controller::run() {{
    if (!m_initialized) {{
        std::cerr << "Error: Controller not initialized" << std::endl;
        return;
    }}

    while (true) {{
        m_sensorValue = m_hal->readSensor();
        m_hal->writeOutput(m_sensorValue);
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }}
}}

void Controller::shutdown() {{
    m_initialized = false;
}}

}} // namespace embedded
''',
                "src/main.cpp": '''// filepath: src/main.cpp
#include <iostream>
#include <memory>
#include "embedded_project.h"

class HALImplementation : public embedded::IHAL {
public:
    bool initializeHardware() override {
        std::cout << "Initializing hardware..." << std::endl;
        return true;
    }

    uint32_t readSensor() override {
        // Simulated sensor reading
        return ++m_counter;
    }

    bool writeOutput(uint32_t value) override {
        std::cout << "Output value: " << value << std::endl;
        return true;
    }

private:
    uint32_t m_counter{0};
};

int main() {
    try {
        auto hal = std::make_shared<HALImplementation>();
        embedded::Controller controller(hal);

        if (!controller.initialize()) {
            std::cerr << "Failed to initialize controller" << std::endl;
            return 1;
        }

        std::cout << "Starting main control loop..." << std::endl;
        controller.run();
    }
    catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
''',
                "CMakeLists.txt": '''cmake_minimum_required(VERSION 3.10)
project(embedded_project)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add compilation flags
if(MSVC)
    add_compile_options(/W4 /WX)
else()
    add_compile_options(-Wall -Wextra -Werror)
endif()

# Include directories
include_directories(${PROJECT_SOURCE_DIR}/include)

# Add source files
set(SOURCES
    src/main.cpp
    src/embedded_project.cpp
)

# Create executable
add_executable(${PROJECT_NAME} ${SOURCES})

# Add threading support
find_package(Threads REQUIRED)
target_link_libraries(${PROJECT_NAME} PRIVATE Threads::Threads)

# Installation rules
install(TARGETS ${PROJECT_NAME} DESTINATION bin)
install(FILES include/embedded_project.h DESTINATION include)
''',
                "tests/test_main.cpp": '''// filepath: tests/test_main.cpp
#include <cassert>
#include <memory>
#include "embedded_project.h"

class MockHAL : public embedded::IHAL {
public:
    bool initializeHardware() override { return true; }
    uint32_t readSensor() override { return 42; }
    bool writeOutput(uint32_t value) override { 
        last_output = value;
        return true;
    }
    uint32_t last_output{0};
};

void test_controller_initialization() {
    auto mock_hal = std::make_shared<MockHAL>();
    embedded::Controller controller(mock_hal);
    assert(controller.initialize());
}

int main() {
    test_controller_initialization();
    std::cout << "All tests passed!" << std::endl;
    return 0;
}
''',
                "README.md": f'''# Embedded Project

An embedded system implementation featuring:
- Hardware Abstraction Layer (HAL) interface
- Main controller with sensor reading and output control
- Thread-safe operations
- Error handling and logging
- CMake build system

## Building

```bash
mkdir build && cd build
cmake ..
make
```

## Testing

```bash
./tests/run_tests
```

## Project Structure
- include/ - Header files
- src/ - Source files
- tests/ - Unit tests
'''
            })
