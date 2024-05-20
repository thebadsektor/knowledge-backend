#TODO: test.db is at root and inside app/app/, fix this

```plaintext
.
└── backend/
    ├── .venv
    ├── src/
    │   └── app/
    │       ├── api/
    │       │   ├── v1/
    │       │   │   ├── summarize.py
    │       │   │   └── summary_tasks.py
    │       │   └── v2/
    │       │       └── summaries.py
    │       ├── databases/
    │       │   └── database.py
    │       ├── documents/ #For testing celery job queue/
    │       │   └── document-1-357-1697.txt
    │       ├── logs/
    │       │   ├── .gitkeep
    │       │   └── celery.log
    │       ├── models/
    │       │   └── models.py
    │       ├── schemas/
    │       │   └── schemas.py
    │       ├── services/
    │       │   └── summarize_service.py
    │       ├── tests/
    │       │   ├── conftest.py
    │       │   └── test_tasks.py
    │       ├── utils/
    │       │   └── openai.py
    │       ├── Dockerfile
    │       ├── main.py
    │       ├── requirements.txt
    │       └── worker.py
    ├── .env
    ├── .gitignore
    ├── docker-compose.yml
    └── READEME.md
```