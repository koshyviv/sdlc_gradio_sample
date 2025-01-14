import openai
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
        return self.generate_response(prompt, SYSTEM_MESSAGES["code"])
