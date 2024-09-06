from docmaker import DocMaker


dm = DocMaker(key_file_name = "api_key.env", project_file = "../club-client/", make_full_docs = False, gitignore = "../club-client/.docignore")
dm.generate_documentation()