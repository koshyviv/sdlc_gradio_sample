import gradio as gr
import os
import shutil
import zipfile
import json
from ai_helper import AIHelper
from datetime import datetime
import re
import graphviz

class SDLCApp:
    def __init__(self):
        self.ai_helper = AIHelper()
        self.persistent_storage = {
            "requirements": "",
            "hld": "",
            "technical_design": "",
            "project_name": "",
            "timestamp": ""
        }
        self.current_structure = {}
        self.create_interface()

    def extract_and_render_graphviz(self, text):
        # Extract Graphviz diagram and convert to image
        diagram_match = re.search(r'```dot(.*?)```', text, re.DOTALL)
        if diagram_match:
            diagram = diagram_match.group(1).strip()
            graph = graphviz.Source(diagram)
            graph_path = f"graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.svg"
            graph.render(filename=graph_path, format='svg', cleanup=False)  # Set cleanup to False
            # Remove the Graphviz code block from the text
            text = re.sub(r'```dot.*?```', '', text, flags=re.DOTALL).strip()
            return text, f"{graph_path}.svg"  # Ensure the correct file path is returned
        return text, ""

    def save_state(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sdlc_state_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(self.persistent_storage, f)
        return filename

    def load_state(self, file):
        try:
            with open(file.name, 'r') as f:
                self.persistent_storage = json.load(f)
            return (
                self.persistent_storage["requirements"],
                self.persistent_storage["hld"],
                self.persistent_storage["technical_design"]
            )
        except Exception as e:
            return "Error loading state", "", ""

    def save_requirements(self, project_name, requirements):
        self.persistent_storage["project_name"] = project_name
        self.persistent_storage["requirements"] = requirements
        hld = self.ai_helper.generate_hld(requirements)
        self.persistent_storage["hld"] = hld
        rendered_hld, diagram_path = self.extract_and_render_graphviz(hld)
        return gr.update(selected=1), rendered_hld, diagram_path

    def save_hld(self, hld):
        self.persistent_storage["hld"] = hld
        technical_design = self.ai_helper.generate_technical_design(hld)
        self.persistent_storage["technical_design"] = technical_design
        rendered_technical, diagram_path = self.extract_and_render_graphviz(technical_design)
        return gr.update(selected=2), rendered_technical, diagram_path

    def save_technical_design(self, technical_design):
        self.persistent_storage["technical_design"] = technical_design
        return gr.update(selected=3)

    def generate_code(self):
        code_structure = self.ai_helper.generate_code_structure(self.persistent_storage["technical_design"])
        
        # Create a directory for the generated code
        project_dir = f"generated_code_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(project_dir, exist_ok=True)

        # Create basic project structure
        self.current_structure = {
            "README.md": f"# {self.persistent_storage['project_name']}\n\n{self.persistent_storage['requirements']}",
            "requirements.txt": "# Generated requirements\n",
            "src/main.py": code_structure,
            "tests/test_main.py": "# Generated tests\n",
            "docs/technical_design.md": self.persistent_storage["technical_design"]
        }

        # Create files and directories
        for filepath, content in self.current_structure.items():
            full_path = os.path.join(project_dir, filepath)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)

        # Create zip file
        zip_filename = f"{project_dir}.zip"
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for root, _, files in os.walk(project_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, project_dir))

        shutil.rmtree(project_dir)
        return zip_filename, gr.Dropdown.update(choices=list(self.current_structure.keys())), ""

    def update_preview(self, selected_file):
        if selected_file in self.current_structure:
            return self.current_structure[selected_file]
        return ""

    def create_interface(self):
        with gr.Blocks() as self.demo:
            gr.Markdown("# Software Development Life Cycle Assistant")
            
            with gr.Tabs() as tabs:
                with gr.TabItem("Requirements Input"):
                    project_name = gr.Textbox(label="Project Name")
                    requirements_input = gr.Textbox(label="Enter Requirements", lines=10)
                    next_button_1 = gr.Button("Generate HLD")
                    save_state_button = gr.Button("Save Current State")
                    load_state_button = gr.File(label="Load Previous State")
                    state_output = gr.File(label="Saved State")

                with gr.TabItem("High-Level Design (HLD)"):
                    hld_input = gr.Textbox(label="High-Level Design", lines=10)
                    hld_diagram = gr.Image(label="HLD Diagram")
                    next_button_2 = gr.Button("Generate Technical Design")

                with gr.TabItem("Technical Design"):
                    technical_design_input = gr.Textbox(label="Technical Design", lines=10)
                    technical_design_diagram = gr.Image(label="Technical Design Diagram")
                    next_button_3 = gr.Button("Next")

                with gr.TabItem("Code Generation"):
                    generate_button = gr.Button("Generate Code")
                    with gr.Row():
                        with gr.Column():
                            download_link = gr.File(label="Download Code")
                            file_dropdown = gr.Dropdown(
                                label="Select File to Preview",
                                choices=[],
                                interactive=True
                            )
                        with gr.Column():
                            code_preview = gr.TextArea(
                                label="File Preview",
                                lines=20,
                                interactive=False
                            )

            # Event handlers
            next_button_1.click(
                self.save_requirements,
                inputs=[project_name, requirements_input],
                outputs=[tabs, hld_input, hld_diagram]
            )
            next_button_2.click(
                self.save_hld,
                inputs=[hld_input],
                outputs=[tabs, technical_design_input, technical_design_diagram]
            )
            next_button_3.click(
                self.save_technical_design,
                inputs=[technical_design_input],
                outputs=tabs
            )
            generate_button.click(
                self.generate_code,
                outputs=[download_link, file_dropdown, code_preview]
            )
            file_dropdown.change(
                self.update_preview,
                inputs=[file_dropdown],
                outputs=[code_preview]
            )
            save_state_button.click(
                self.save_state,
                outputs=state_output
            )
            load_state_button.change(
                self.load_state,
                inputs=[load_state_button],
                outputs=[requirements_input, hld_input, technical_design_input]
            )

    def launch(self):
        self.demo.launch()

if __name__ == "__main__":
    app = SDLCApp()
    app.launch()
