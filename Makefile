.PHONY: all help test validate gallery fix build-missing install clean

PYTHON ?= python3

all: validate

help:
	@echo "🎨 Marhy's Picons Developer & Contributor Commands"
	@echo "================================================="
	@echo "  make install        Nainstalovat potřebné Python závislosti"
	@echo "  make test           Spustit automatizovanou kontrolu kvality (CI audit)"
	@echo "  make gallery        Spustit validaci a přegenerovat HTML galerii a kontaktní list"
	@echo "  make fix            Automaticky opravit paritu rozlišení (640 vs 1024)"
	@echo "  make build-missing  Přeexportovat všechny DVB-T2 stanice ze source/raw/"
	@echo "  make clean          Vyčistit dočasné soubory z buildu"
	@echo ""
	@echo "Přidání nové stanice:"
	@echo "  python3 tools/add_picon.py --name 'Nova Sport 5' --id 'novasport5' --raw 'source/raw/novasport5.svg' --bg '#003366'"

install:
	$(PYTHON) -m pip install -r requirements.txt

test: validate

validate:
	$(PYTHON) tools/validate_picons.py

gallery:
	$(PYTHON) tools/validate_picons.py --gallery

fix:
	$(PYTHON) tools/validate_picons.py --fix

build-missing:
	$(PYTHON) generate_missing_picons.py

clean:
	rm -rf build/
	rm -f /tmp/picon_sources/temp_*.html
