FROM python:3.9

ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.5.1 

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# RUN poetry export --dev -f requirements.txt | pip install -r /dev/stdin
RUN poetry export --dev --without-hashes -f requirements.txt | pip install -r /dev/stdin

RUN apt-get update

# Copy code
COPY . /code
RUN poetry build && pip install dist/*.whl

EXPOSE 7000