# Detecta SO para escolher os caminhos/comandos certos
ifeq ($(OS),Windows_NT)
	PYTHON := python
else
	PYTHON := python3
endif

RM := rm -rf
BACKEND_DIR := backend
VENV_DIR := $(BACKEND_DIR)/.venv
WORKFLOWS_DIR := workflows
N8N_DIR := .n8n_data
SCRIPTS_DIR := scripts

# Auto-detecta o caminho do executável do Python e do pip dentro do virtualenv
VENV_BIN     = $(firstword $(wildcard $(VENV_DIR)/Scripts $(VENV_DIR)/bin))
PYTHON_VENV  = $(firstword $(wildcard $(VENV_BIN)/python.exe $(VENV_BIN)/python))
PIP_VENV     = $(firstword $(wildcard $(VENV_BIN)/pip.exe $(VENV_BIN)/pip))

DOCKER_N8N := docker compose exec n8n

.PHONY: setup start stop clean

setup: $(VENV_DIR)
	$(PYTHON_VENV) -m pip install --upgrade pip
	$(PIP_VENV) install -r backend/requirements.txt

start:
	docker compose up -d --build

start-n8n:
	docker compose up -d n8n

start-backend:
	docker compose up -d --build backend

stop:
	docker compose down

export-workflows: start-n8n
	mkdir -p $(WORKFLOWS_DIR)
	$(DOCKER_N8N) sh -lc 'rm -rf /home/node/.n8n/exports'
	$(DOCKER_N8N) sh -lc 'mkdir -p /home/node/.n8n/exports'
	$(DOCKER_N8N) sh -lc 'chown -R node:node /home/node/.n8n/exports'
	
	# Usuários do MSYS2 (assim como eu) que usa o make deles, podem ter problemas em relação
	# a conversão dos caminhos, o qual make interpreta /home/node/.n8n/exports como C:/msys64/home/node/.n8n/exports,
	# e isso quebra o comando do n8n. Para contornar isso, podemos usar a variável de ambiente MSYS2_ARG_CONV_EXCL
	# e excluir o argumento --output= da conversão de caminhos do MSYS2.
	MSYS2_ARG_CONV_EXCL='--output=' \
	$(DOCKER_N8N) n8n export:workflow \
		--all \
		--pretty \
		--separate \
		--output=/home/node/.n8n/exports
	
	$(PYTHON) $(SCRIPTS_DIR)/copy_workflows.py "$(N8N_DIR)/exports" "$(WORKFLOWS_DIR)"

clean:
	rm -rf $(VENV_DIR)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	docker compose down -v --remove-orphans
	docker system prune -f

$(VENV_DIR):
	$(PYTHON) -m venv $(VENV_DIR)
	