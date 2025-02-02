PYTHON = python3
PYTHON_VENV = venv
PYINSTALLER = $(PYTHON_VENV)/bin/pyinstaller
SRC_DIR = .
DIST_DIR = dist
CONFIG_DIR = $${HOME}/.config/pinboard
REQUIREMTNS_FILE = requirements.txt

EXECUTABLE_NAME = pinboard

all: create_venv install_dependencies create_config_dir build_executable

create_venv:
	@echo "Installing dependencies..."
	$(PYTHON_VENV)/bin/pip install -r $(REQUIREMTNS_FILE)
	@echo "Dependencies installed."

create_config_dir:
	mkdir -p $(CONFIG_DIR)
	@echo "Config dir: $(CONFIG_DIR)"

build_executable:
	@echo "Starting build..."
	$(PYINSTALLER) --onefile --name pinboard main.py
	@echo "Building done."

clean:
	rm -rf $(DIST_DIR)
	rm -rf build
	rm -rf $(EXECUTABLE_NAME).spec
	rm -rf $(PYTHON_VENV)
	@echo "Cleaned up."

uninstall: clean
	rm -rf $(CONFIG_DIR)
	@echo "Uninstalled"

.PHONY: create_venv install_dependencies create_config_dir build_executable clean uninstall