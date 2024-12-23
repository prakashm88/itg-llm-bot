# app/Dockerfile

FROM python:3.13-slim as simpleapp-builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip3 install --no-cache-dir  -r requirements.txt

FROM python:3.13-slim

WORKDIR /app

#RUN apt-get update && apt-get install -y curl

COPY --from=simpleapp-builder /app /app
COPY --from=simpleapp-builder /usr/local/ /usr/local/

RUN mkdir -p /app/data

COPY app.py .
COPY models.json ./data

RUN useradd -m -s /bin/bash svc-appuser
RUN chown -R svc-appuser:svc-appuser /app

USER svc-appuser

ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

EXPOSE 8501

#HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]