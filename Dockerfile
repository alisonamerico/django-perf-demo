FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc gettext && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
RUN uv venv /opt/venv && \
    uv pip install --python /opt/venv/bin/python \
        "Django>=5.1,<6.0" \
        "psycopg2-binary>=2.9.9" \
        "django-debug-toolbar>=4.4.6" \
        "django-silk>=5.3.2" \
        "dj-database-url>=2.2.0" \
        "python-decouple>=3.8" \
        "factory-boy>=3.3.1" \
        "Faker>=26.0.0" \
        "pytest>=8.3.3" \
        "pytest-django>=4.9.0"

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings

COPY . .
