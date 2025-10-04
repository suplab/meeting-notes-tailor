.PHONY: run build
run:
	uvicorn app.api.main:app --reload
build:
	docker build -t meeting-notes-tailor:local .
