from gemini_gen_client import GeminiGen as gg
import json
from pathlib import Path
import os
from gitignore_parser import parse_gitignore
import sys
import mimetypes

def return_true(var1):
    return True

class DocMaker:

    def __init__(self, key_file_name = "api_key.env", project_file = "./", make_full_docs = False, gitignore = False):
        self.gen_flash = gg(key_file_name, "gemini-1.5-flash", {"response_mime_type": "text/plain", "temperature": 0.5})
        self.gen_pro = gg(key_file_name, "gemini-pro", {"response_mime_type": "text/plain", "temperature": 0.5})
        self.project_file = project_file
        self.gitignore = gitignore
        self.make_full_docs = make_full_docs
        
        self.full_prompt = "I am giving code that is part of a full codebase, which I need to document all things you think a programmer in this codebase would need to know. I have given every file, as shown below, seperated with ------. I need you to generate a reader-friendly docs and explanation. Only respond with the md file. Nothing else. Make sure that it is in md format. There is a current issue on previous attempts it would have ``` at the start, which you should NOT do. Make sure that you DO NOT OUTPUT just the code from the original file"
        self.doc_prompt = "I am giving you a file to document. This is part of a larger codebase, and is shown below. Please respond only in md, in a reader-friendly way with all files needed. Do not give anything but documentation"
    def generate_documentation(self):
        if self.gitignore:      
            self.matches = parse_gitignore(self.gitignore)
        
        else:
            self.matches = return_true
        
        print(self.gitignore)

        self.create_project_doc_folder()
        
        for root, dirs, files in os.walk(self.project_file):
            for file in files:
                file_path = os.path.join(root, file)
                if not self.matches(file_path) and self.is_text_file(file_path):
                    file_path = file_path.replace("\\", "/")
                    print(file_path)
                    with open(file_path, 'r') as f:
                        content = f.read()
                        print(os.path.relpath(file_path, self.project_file).replace("\\", "/"))
                        
                        self.document(os.path.relpath(file_path, self.project_file).replace("\\", "/"), content)
        

    def create_project_doc_folder(self):
        Path(self.project_file + "docs").mkdir(parents=True, exist_ok=True)
        
    def add_to_docs(self, path, content):
        full_path = os.path.join(self.project_file + "docs/", path + ".md")
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    def add_to_full_docs(self, path, content):
        with open(self.project_file + "docs/full_docs_helper.txt", "a") as f:
            f.write("--------\n")
            f.write(path + "\n")
            f.write("--------\n")
            f.write(content)
            f.write("\n")
    
    
    def document(self, path, content):
        re = self.gen_flash.generate_text(self.doc_prompt + content)
        try: 
            re = re.text
        except:
            
            
            re = "Error"
            

        self.add_to_docs(path, re)
        if self.make_full_docs:
            self.add_to_full_docs(path, re)
        
    def generate_full_documentation(self):
        with open(self.project_file + "docs/full_docs_helper.txt", "w") as f:
            content = f.read()
            re = self.gen_pro.generate_text(self.full_prompt + content)
            try: 
                re = json.loads(re.text)["message"]
            except:
                re = "Error"
            
            with open(self.project_file + "docs/full_docs.md", "w") as f:
                f.write(re)
            
            
            os.remove(self.project_file + "docs/full_docs_helper.txt")
    
        
        
    def is_text_file(self, file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type:
            # Allow text/* and specific application/* types
            return (mime_type.startswith('text') or 
                    mime_type in ['application/javascript', 'application/json', 'application/xml'])
        return False