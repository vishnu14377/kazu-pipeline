import os

ONT_DIR = os.path.join(os.path.dirname(__file__), '..', 'ontologies')

for root, dirs, files in os.walk(ONT_DIR):
    for file in files:
        if file.endswith('.ttl'):
            path = os.path.join(root, file)
            with open(path, encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f, 1):
                    if 'disease' in line.lower():
                        print(f"{path}:{i}: {line.strip()}")