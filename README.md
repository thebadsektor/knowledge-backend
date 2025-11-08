# Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Set up the environment:**
   - Create a `.env` file by copying the sample file:
     ```bash
     cp sample.env .env
     ```
   - Open the `.env` file and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```

3. **Build and run with Docker Compose:**
   ```bash
   docker-compose up -d --build
   ```

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