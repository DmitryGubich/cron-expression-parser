VIRTUAL_ENV = .venv
PYTHON=${VIRTUAL_ENV}/bin/python3

$(VIRTUAL_ENV):
	@echo "$(ccso)--> Install and setup virtualenv $(ccend)"
	python3 -m pip install --upgrade pip
	python3 -m pip install virtualenv
	virtualenv $(VIRTUAL_ENV)

# create venv
venv: $(VIRTUAL_ENV)

# create venv and install deps
install: venv requirements.txt
	@echo "$(ccso)--> Updating packages $(ccend)"
	$(PYTHON) -m pip install -r requirements.txt

# run the command
run:
	@echo "$(ccso)--> Run tests $(ccend)"
	$(PYTHON) src/parser.py "${command}"

# run tests
test:
	@echo "$(ccso)--> Run tests $(ccend)"
	$(PYTHON) -m pytest