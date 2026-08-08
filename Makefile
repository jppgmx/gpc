# Detecta SO para escolher os caminhos/comandos certos
ifeq ($(OS),Windows_NT)
	PYTHON := python
else
	PYTHON := python3
endif

RM := rm -rf

# Pastas do projeto
SCRIPTS_DIR := scripts
WORKFLOWS_DIR := workflows
BACKEND_DIR := backend

# Pastas temporárias
VENV_DIR := $(BACKEND_DIR)/.venv
N8N_DIR := .n8n_data

# venv
# Auto-detecta o caminho do executável do Python e do pip dentro do virtualenv
VENV_BIN     = $(firstword $(wildcard $(VENV_DIR)/Scripts $(VENV_DIR)/bin))
ACTIVATE = . $(VENV_BIN)/activate
PIP = pip

DOCKER_N8N := docker compose exec n8n

.PHONY: setup start stop clean

# Configura ambiente de desenvolvimento
setup: $(VENV_DIR)
	$(ACTIVATE) && $(PYTHON) -m pip install --upgrade pip
	$(ACTIVATE) && $(PIP) install -r backend/requirements.txt
	$(ACTIVATE) && $(PIP) install -r backend/requirements-dev.txt
	$(ACTIVATE) && cd backend && $(PIP) install -e .

# Roda pylint
pylint:
	$(ACTIVATE) && pylint backend/app

# Inicia os containers do docker
start:
	docker compose up -d --build

# Inicia apenas o container do n8n
start-n8n:
	docker compose up -d n8n

# Inicia apenas o container do backend
start-backend:
	docker compose up -d --build backend

# Para parar os containers do docker
stop:
	docker compose down

# Para parar apenas o container do n8n
stop-n8n:
	docker compose down n8n

# Para parar apenas o container do backend
stop-backend:
	docker compose down backend

# Exporta todos os workflows do n8n para a pasta workflows
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

# Limpa arquivos temporários, venv e containers do docker
clean:
	rm -rf $(VENV_DIR)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	docker compose down -v --remove-orphans
	docker system prune -f

# Cria venv caso não exista
$(VENV_DIR):
	$(PYTHON) -m venv $(VENV_DIR)
	