import os
import json
import shutil
import sys

if len(sys.argv) != 3:
    print("Uso: python rename_workflows.py <diretório_origem> <diretório_destino>")
    sys.exit(1)

src = os.path.abspath(sys.argv[1])
dest = os.path.abspath(sys.argv[2])

files = os.listdir(src)
for file in files:
    if file.endswith(".json"):
        name = file[:-5]  # Remove a extensão .json
    with open(os.path.join(src, file), 'r', encoding='utf-8') as f:
        data = json.load(f)
        name = data.get('name', name)  # Use o nome do workflow se disponível
    new_file_name = f"{name}.json"
    src_path = os.path.join(src, file)
    dest_path = os.path.join(dest, new_file_name)

    print(f"{file} -> {new_file_name}", end="")
    try:
        shutil.copy(src_path, dest_path)
        print(" [OK]")
    except Exception as e:
        print(f" [ERRO] {e}")
