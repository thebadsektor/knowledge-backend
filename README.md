#TODO: test.db is at root and inside app/app/, fix this

```bash
.
└── backend/
    ├── .venv
    ├── src/
    │   └── app/
    │       ├── api/
    │       │   ├── v1/
    │       │   │   ├── general_tasks.py
    │       │   │   └── summaries.py
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
    │       │   ├── v1/
    │       │   │   └── summary_services.py
    │       │   └── v2/
    │       │       └── summary_services.py
    │       ├── tests/
    │       │   ├── conftest.py
    │       │   └── test_tasks.py
    │       ├── utils/
    │       │   └── openai.py
    │       ├── Dockerfile
    │       ├── main.py
    │       ├── requirements.txt
    │       ├── test.db
    │       └── worker.py
    ├── .env
    ├── .gitignore
    ├── docker-compose.yml
    └── READEME.md
```