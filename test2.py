from gitignore_parser import parse_gitignore


matches = parse_gitignore(".docignore")

print(matches(".gitignore"))