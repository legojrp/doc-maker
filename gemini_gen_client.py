import google.generativeai as genai


import os

# Suppress logging warnings
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"


class GeminiGen:
    def __init__(self, key_file_name, model_name, config) -> None:
        with open(key_file_name, 'r') as f:
            api_key = f.read()
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name=model_name, generation_config=config)

    def generate_text(self, prompt):
        return self.model.generate_content(prompt)

    

    
    