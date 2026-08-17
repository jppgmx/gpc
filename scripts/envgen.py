"""
    Gerador de arquivo .env para o n8n.
"""

import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(ROOT_DIR, ".env")
TEMPLATE_FILE = os.path.join(ROOT_DIR, ".env.template")

generated_env_content = {}
print("Lendo template...")
with open(TEMPLATE_FILE, "r", encoding="utf-8") as template_file:
    for line in template_file:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, defvalue = line.split("=", 1)

        defstr = f" (padrão: {defvalue})" if defvalue else ""
        value = input(f"Digite o valor para {key}{defstr}: ") or defvalue
        generated_env_content[key] = value

print("Escrevendo arquivo .env... ", end="")

try:
    with open(ENV_FILE, "w", encoding="utf-8") as env_file:
        for key, value in generated_env_content.items():
            env_file.write(f"{key}={value}\n")
    print("OK")
except Exception as e:
    print(f"Erro ao escrever arquivo .env: {e}")
