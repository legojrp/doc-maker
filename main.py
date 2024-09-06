from gemini_gen_client import GeminiGen as gg
import json


gen = gg("api_key.env", "gemini-1.5-flash", {"response_mime_type": "application/json", "temperature": 0.5})
re = gen.generate_text("Can you develop a markdown documentation for this python file?")
re_json = json.loads(re.text)
print(re_json["message"])
