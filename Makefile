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
	$(PYTHON) -m venv $(PYTHON_VENV)
	@echo "Venv created"

install_dependencies:
	@echo "Installing python dependencies..."
	$(PYTHON_VENV)/bin/pip install -r $(REQUIREMTNS_FILE)
	@echo "Python dependencies installed."

	@echo "Checking clipboard requirements..."
	@if [ "$$(echo $$XDG_SESSION_TYPE)" = "x11" ]; then \
		echo "Detected X11 - Installing xclip..."; \
		if command -v apt > /dev/null 2>&1; then sudo apt install -y xclip; fi; \
		if command -v dnf > /dev/null 2>&1; then sudo dnf install -y xclip; fi; \
		if command -v pacman > /dev/null 2>&1; then sudo pacman -S --noconfirm xclip; fi; \
	elif [ "$$(echo $$XDG_SESSION_TYPE)" = "wayland" ]; then \
		echo "Detected Wayland - Installing wl-clipboard..."; \
		if command -v apt > /dev/null 2>&1; then sudo apt install -y wl-clipboard; fi; \
		if command -v dnf > /dev/null 2>&1; then sudo dnf install -y wl-clipboard; fi; \
		if command -v pacman > /dev/null 2>&1; then sudo pacman -S --noconfirm wl-clipboard; fi; \
	else \
		echo "Could not detect X11 or Wayland - Skipping clipboard tool installation."; \
	fi

	@echo "Checking for gobject-introspection..."
	@if ! command -v g-ir-scanner > /dev/null 2>&1; then \
		echo "Installing gobject-introspection..."; \
		if command -v apt > /dev/null 2>&1; then sudo apt install -y gobject-introspection; fi; \
		if command -v dnf > /dev/null 2>&1; then sudo dnf install -y gobject-introspection; fi; \
		if command -v pacman > /dev/null 2>&1; then sudo pacman -S --noconfirm gobject-introspection; fi; \
	else \
		echo "gobject-introspection is already installed."; \
	fi

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