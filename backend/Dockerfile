FROM python:3.11-slim-bullseye

WORKDIR /app

ENV POETRY_HOME="/opt/poetry" \
    VENV="/app/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV/bin:$PATH"

RUN apt update && apt install -y \
    build-essential \
    gcc \
    git \
    libpq-dev \
    make \
    netcat \
    pkg-config \
    python3-dev \
    python3-opencv \
    wget \
    && apt clean && rm -rf /var/lib/apt/lists/*


ENV POETRY_VERSION=1.3.2
ENV PYTHONUNBUFFERED=1

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . /code
WORKDIR /code/src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
