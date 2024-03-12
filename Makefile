.PHONY: init-db

init-db:
	@echo "Creating and initializing the database with dummy records..."
	@uvicorn app.app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
	@curl -X POST "http://localhost:8000/create_database"
	@echo "Database initialized successfully."
