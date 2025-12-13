#Stage 1: Builder
FROM python:3.12-alpine AS staging
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

#Stage 2: Runtime
FROM python:3.12-alpine
WORKDIR /app
COPY --from=staging /install /usr/local
COPY app.py .
CMD ["sh", "-c", "echo 'Crashing!' && exit 1"]

