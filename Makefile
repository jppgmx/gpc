# Detecta SO para escolher os caminhos/comandos certos
ifeq ($(OS),Windows_NT)
	PYTHON := python
else
	PYTHON := python3
endif

RM := rm -rf
VENV_DIR := backend/.venv

# Auto-detecta o caminho do executável do Python e do pip dentro do virtualenv
VENV_BIN     = $(firstword $(wildcard $(VENV_DIR)/Scripts $(VENV_DIR)/bin))
PYTHON_VENV  = $(firstword $(wildcard $(VENV_BIN)/python.exe $(VENV_BIN)/python))
PIP_VENV     = $(firstword $(wildcard $(VENV_BIN)/pip.exe $(VENV_BIN)/pip))

.PHONY: setup start stop clean

setup: $(VENV_DIR)
	$(PIP_VENV) install --upgrade pip
	$(PIP_VENV) install -r backend/requirements.txt

start:
	docker compose up -d --build

stop:
	docker compose down

clean:
	rm -rf $(VENV_DIR)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	docker compose down -v --remove-orphans
	docker system prune -f

$VENV_DIR:
	$(PYTHON) -m venv $(VENV_DIR)