import os
import json
import re
import shutil
import sys

if len(sys.argv) != 3:
    print("Uso: python rename_workflows.py <diretório_origem> <diretório_destino>")
    sys.exit(1)

src = os.path.abspath(sys.argv[1])
dest = os.path.abspath(sys.argv[2])
os.makedirs(dest, exist_ok=True)

INVALID_CHARS = r'[\\/:*?"<>|]'

for file in os.listdir(src):
    if not file.endswith(".json"):
        continue

    src_path = os.path.join(src, file)
    name = file[:-5]

    try:
        with open(src_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        name = data.get("name", name)
    except (json.JSONDecodeError, OSError) as e:
        print(f"{file} -> [ERRO ao ler] {e}")
        continue

    safe_name = re.sub(INVALID_CHARS, "_", name)
    dest_path = os.path.join(dest, f"{safe_name}.json")

    print(f"{file} -> {safe_name}.json", end="")
    try:
        shutil.copy(src_path, dest_path)
        print(" [OK]")
    except OSError as e:
        print(f" [ERRO] {e}")
