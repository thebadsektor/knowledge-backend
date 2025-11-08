# Knowledge Research Inc. API

This project is a containerized application that provides a RESTful API for summarizing text documents using OpenAI's language models. The application is built with FastAPI and uses Celery for asynchronous task processing, with Redis as the message broker and result backend. The project is fully containerized using Docker Compose, which simplifies the setup and deployment process.

## Architecture

The application is composed of the following services:

- **`web`**: A FastAPI application that serves the RESTful API.
- **`worker`**: A Celery worker that processes summarization tasks asynchronously.
- **`redis`**: A Redis instance that serves as the message broker for Celery.
- **`dashboard`**: A Flower dashboard for monitoring the Celery worker.

## Getting Started

### Prerequisites

- Docker and Docker Compose must be installed on your local machine.
- You must have an active OpenAI API key.

### Installation

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

### Usage

- **API**: The FastAPI application will be available at `http://localhost:8000`. You can access the API documentation at `http://localhost:8000/docs`.
- **Flower Dashboard**: The Flower dashboard will be available at `http://localhost:5556`.

### Project Structure

```
.
├── src/
│   └── app/
│       ├── api/
│       │   ├── v1/
│       │   │   ├── general_tasks.py
│       │   │   └── summaries.py
│       │   └── v2/
│       │       └── summaries.py
│       ├── database/
│       │   └── database.py
│       ├── models/
│       │   └── models.py
│       ├── schemas/
│       │   └── schemas.py
│       ├── services/
│       │   ├── v1/
│       │   │   └── summary_services.py
│       │   └── v2/
│       │       └── summary_services.py
│       ├── Dockerfile
│       ├── main.py
│       └── worker.py
├── .env
├── .gitignore
├── docker-compose.yml
└── README.md
```
