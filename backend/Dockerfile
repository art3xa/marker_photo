FROM python:3.10-alpine
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache \
	pip install -r requirements.txt

COPY . .
ENV PRODUCTION=1

RUN chmod +x ./init.sh
ENV GUNICORN_CMD_ARGS "--bind=0.0.0.0:5000"
CMD ./init.sh
EXPOSE 5000
