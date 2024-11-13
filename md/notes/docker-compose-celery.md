## Docker Compose and Celery Setup for Corpora Project

### Project Structure and Overview

In this setup:
- The `corpora` app is designed to be independent, providing core functionality.
- The `corpora_proj` project acts as a container that integrates `corpora` with additional services (e.g., Redis for task queuing with Celery).

The overall architecture allows `corpora` to remain agnostic while `corpora_proj` manages the additional dependencies.

### Docker Compose Configuration

Docker Compose is configured with four primary services:
1. **app**: Runs Django and the main API.
2. **db**: PostgreSQL with pgvector enabled, providing persistent data storage.
3. **redis**: Acts as a broker and backend for Celery tasks.
4. **celery**: The worker service that runs tasks asynchronously.

Below is the `docker-compose.yaml` configuration, followed by explanations of each component.

```yaml
services:
  app:
    build:
      context: .
      dockerfile: .devcontainer/Dockerfile
    volumes:
      - .:/workspace
    environment:
      PYTHONPATH: "/workspace/py/packages"
      REDIS_URL: "redis://redis:6379/0"
    depends_on:
      - db
      - redis
      - celery
    ports:
      - "8000:8000"

  db:
    build:
      context: .
      dockerfile: docker/Dockerfile.pgvector
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data

  redis:
    image: redis:latest
    ports:
      - "6379:6379"
    healthcheck:
      test: [ "CMD", "redis-cli", "ping" ]
      interval: 5s
      timeout: 5s
      retries: 5

  celery:
    build:
      context: .
      dockerfile: .devcontainer/Dockerfile
    command: celery -A corpora_proj.celery_app.app worker --loglevel=info
    volumes:
      - .:/workspace
    environment:
      PYTHONPATH: "/workspace/py/packages"
      REDIS_URL: "redis://redis:6379/0"
    depends_on:
      redis:
        condition: service_healthy

volumes:
  postgres-data:
```

### Service Descriptions and Configuration Details

1. **app (Django Application Service)**
   The `app` service builds the Django application defined in `corpora_proj`. It has dependencies on `db`, `redis`, and `celery`, ensuring that all supporting services are available before startup.
   - **Environment**: Sets the `PYTHONPATH` to recognize packages and defines `REDIS_URL` to connect with Redis.
   - **Ports**: Exposes port `8000` for accessing the Django app locally.

2. **db (PostgreSQL with pgvector)**
   The database service uses a Dockerfile specifically set up for pgvector (`docker/Dockerfile.pgvector`). PostgreSQL settings are defined to create a persistent `postgres-data` volume.
   - **Ports**: Exposes port `5432` for database connections.

3. **redis (Message Broker and Result Backend)**
   Redis is used by Celery for queuing and backend storage of task results. A health check ensures Redis is ready before dependent services start, with the `ping` command to verify connectivity.
   - **Ports**: Exposes port `6379`.

4. **celery (Celery Worker)**
   The Celery worker runs with the `command` field, initializing `celery_app.app` as the worker app. It depends on Redis to ensure the broker is active before starting task consumption.
   - **Environment**: Sets `REDIS_URL` to the Redis broker and includes the correct `PYTHONPATH` for package imports.

### Celery Task Management

For Celery to automatically detect tasks, ensure that:
1. In `corpora_proj/celery_app.py`, use `autodiscover_tasks()` to register tasks within the `corpora` app:

   ```python
   # corpora_proj/celery_app.py
   from celery import Celery
   import os

   os.environ.setdefault("DJANGO_SETTINGS_MODULE", "corpora_proj.settings")

   app = Celery("corpora_proj")
   app.config_from_object("django.conf:settings", namespace="CELERY")
   app.autodiscover_tasks(['corpora'])
   ```

2. In `corpora_proj/__init__.py`, add the following to initialize Celery with Django on startup:

   ```python
   from .celery_app import app as celery_app
   ```

3. **Creating Tasks in `corpora`**: Use `@shared_task` for tasks within `corpora`, so they work in any Celery app environment:

   ```python
   # corpora/tasks.py
   from celery import shared_task

   @shared_task
   def example_task(data):
       print(f"Processing data: {data}")
       return "Task completed"
   ```

### Running and Managing Containers

1. **Build and Start Services**:
   ```bash
   docker-compose up --build
   ```
   - This command builds the images and starts all services, ensuring each is up-to-date with recent changes.

2. **Stopping and Restarting Containers**:
   - Use `docker-compose stop` to halt services without removing them.
   - Use `docker-compose up` to restart them or `docker-compose up -d` to start them in detached mode.

3. **Logging and Debugging**:
   - Access logs for each service using `docker-compose logs -f <service-name>`. For example, to check Celery logs:
     ```bash
     docker-compose logs -f celery
     ```
   - For error tracking, ensure that each container is running and connected as expected by inspecting the logs, especially for connectivity between `app`, `redis`, and `celery`.

4. **Running Django Shell and Tests**:
   - To access a shell inside the `app` container for testing Django settings and task execution, use:
     ```bash
     docker-compose exec app ./manage.py shell
     ```
   - To test tasks directly from the Django shell:
     ```python
     from corpora.tasks import example_task
     example_task.delay("Sample data")
     ```

### Tips and Best Practices

- **Use Health Checks**: Adding health checks to services like Redis ensures dependent services only start once the service is ready.
- **Clear Docker Volumes**: For clean testing, you may need to clear out Docker volumes:
  ```bash
  docker-compose down -v
  ```
- **Environment Variable Management**: Centralize environment variables in a `.env` file to avoid hardcoding sensitive data in `docker-compose.yaml`.
- **Task Testing and Debugging**: Test each Celery task in isolation with `delay()` and monitor logs to verify task status and result.

### Summary

This setup creates a scalable environment where `corpora` remains a standalone Django app, with Celery tasks managed by Redis and executed by a dedicated worker. Using Docker Compose simplifies the process of orchestrating these services, allowing for isolated testing and deployment.
