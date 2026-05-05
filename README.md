# Intern Coding Prompt: Flask to FastAPI Migration

## Overview

This repository contains a simple Flask application with CRUD (Create, Read, Update, Delete) operations for a task management API. Your task is to migrate this application from Flask to FastAPI, utilizing modern package management with `uv`, and ensure it is properly containerized with Docker.

## Current Application

The existing Flask application (`app.py`) provides a task management API with the following endpoints:

- **GET /tasks** - Retrieve all tasks
- **GET /tasks/<task_id>** - Retrieve a specific task by ID
- **POST /tasks** - Create a new task
- **PUT /tasks/<task_id>** - Update an existing task
- **DELETE /tasks/<task_id>** - Delete a task
- **GET /health** - Health check endpoint

The application uses in-memory storage (a Python dictionary) to store tasks. Each task has the following fields:
- `id` (UUID)
- `title` (string)
- `description` (string)
- `completed` (boolean)
- `created_at` (ISO timestamp)
- `updated_at` (ISO timestamp, only on updates)

## Your Task

You need to complete the following tasks:

### 1. Convert Flask to FastAPI

Migrate the Flask application to FastAPI while maintaining the same functionality and API contract. Consider the following:

- Use FastAPI's dependency injection system
- Implement proper request/response models using Pydantic
- Use FastAPI's automatic OpenAPI documentation
- Maintain the same endpoint paths and behavior
- Use async/await where appropriate
- Implement proper error handling with FastAPI's exception handlers

### 2. Modernize Package Management with `uv`

The project already uses `pyproject.toml` for package management. Continue using `uv` for package management:

- Install dependencies using `uv sync`
- Add new dependencies using `uv add <package>`
- Remove dependencies using `uv remove <package>`
- Run the application using `uv run python app.py`
- Document the setup process in the README

### 3. Containerize with Docker

Update the Dockerfile to work with the new FastAPI application:

- Use an appropriate Python base image (prefer slim variants)
- Install `uv` and use it for dependency management
- Copy the `pyproject.toml` and lock files
- Install dependencies using `uv sync`
- Expose the appropriate port (FastAPI defaults to 8000)
- Use a production-grade ASGI server like `uvicorn`
- Optimize the Docker image for size (multi-stage builds if needed)

### 4. Maintain CRUD Operations

Ensure all four CRUD operations are properly implemented in FastAPI:

- **Create**: POST /tasks
- **Read**: GET /tasks and GET /tasks/<task_id>
- **Update**: PUT /tasks/<task_id>
- **Delete**: DELETE /tasks/<task_id>

### 5. Setup GitHub Actions

Setup a GitHub Actions workflow to run unit tests with code coverage reporting on push and pull request.

## Requirements

- Python 3.11 or higher
- FastAPI
- uv for package management
- Docker for containerization
- Pydantic for data validation
- Uvicorn (or similar ASGI server)

## Deliverables

1. Updated `app.py` - FastAPI application
2. `pyproject.toml` - Project configuration and dependencies (already created)
3. Updated `Dockerfile` - Container configuration
4. Updated `README.md` - Clear instructions on how to run the application
5. `.github/workflows/test.yml` - GitHub Actions workflow to run unit tests with code coverage reporting on push and pull request

## Submission

See [`SUBMISSIONS.md`](./SUBMISSIONS.md) for instructions on how to fork the repository and submit your completed exercise.

## Testing Your Implementation

After completing the migration, verify your implementation by:

1. Starting the application locally using `uv run uvicorn app:app --reload`
2. Testing each endpoint using `curl` or a tool like Postman
3. Building and running the Docker container
4. Verifying the automatic OpenAPI documentation at `/docs` or `/openapi.json`

## Example API Usage

```bash
# Create a task
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Complete migration", "description": "Migrate Flask to FastAPI"}'

# Get all tasks
curl http://localhost:5000/tasks

# Get a specific task
curl http://localhost:5000/tasks/{task_id}

# Update a task
curl -X PUT http://localhost:5000/tasks/{task_id} \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Delete a task
curl -X DELETE http://localhost:5000/tasks/{task_id}

# Health check
curl http://localhost:5000/health
```

## Additional Considerations

- Think about data validation and error handling
- Consider adding input validation using Pydantic models
- Think about potential improvements (e.g., database integration, authentication)
- Document any assumptions or design decisions you make
- Ensure the Docker image is optimized for production use

## Getting Started

1. Clone this repository
2. Review the existing Flask application in `app.py`
3. Review the current `Dockerfile`
4. **Important: Do not edit the unit tests in the `tests/` directory** - these tests must continue to pass after your migration
5. Begin your migration to FastAPI
6. Run the unit tests to ensure your implementation is correct: `uv run pytest`
7. Test your implementation thoroughly
8. Update the README with any additional instructions

## Unit Tests

The repository includes a comprehensive suite of unit tests in the `tests/` directory. These tests verify the functionality of all CRUD operations and the health check endpoint.

**Important:** Do not modify the unit tests. Your FastAPI implementation must pass all existing tests to ensure API compatibility and functionality.

To run the tests:
```bash
uv sync --dev
uv run pytest
```
---

## Running the Application

Install dependencies:

```bash
uv sync --dev
```

Run locally:

```bash
uv run uvicorn app:app --reload
```

Open in browser:
http://localhost:8000/docs

## Running Tests
```bash
uv run pytest
```

## Docker

Build the image:

```bash
docker build -t credibly-fastapi .
```

Run the container:

```bash
docker run -p 8000:8000 credibly-fastapi
```

Then open:
http://localhost:8000/docs

## Notes

- Moved from Flask API to FastAPI
- Retained the functionality of the current API
- Confirmed that all the given tasks are working
- Introduced Docker container for the application