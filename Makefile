SRC = src
VENV ?= venv

$(VENV): requirements.txt nltk.txt
	@python -m venv $@
	@source $@/bin/activate && pip install -r $<
	@mkdir $@/nltk_data/
	@source $@/bin/activate && python -m nltk.downloader $(file < nltk.txt) -d $@/nltk_data/
	@echo "Enter virtual environment: source $@/bin/activate"

tags: $(SRC)
	@ctags --languages=python --python-kinds=-i -R $(SRC)

.PHONY: outdated
outdated:
	@source $(VENV)/bin/activate && pip list --outdated

.PHONY: lint
lint:
	@pylint -f colorized $(SRC)

.PHONY: typecheck
typecheck:
	@mypy $(SRC)
