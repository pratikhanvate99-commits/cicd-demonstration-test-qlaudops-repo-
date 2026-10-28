FROM node:22-alpine AS frontend-build
WORKDIR /workspace/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8000
WORKDIR /app
RUN addgroup --system --gid 10001 qlaudops && adduser --system --uid 10001 --ingroup qlaudops --no-create-home qlaudops
COPY backend/requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir --upgrade setuptools wheel \
    && python -m pip install --no-cache-dir -r requirements.txt
COPY backend/app ./app
COPY --from=frontend-build /workspace/frontend/dist ./static
USER 10001:10001
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/ready', timeout=2)" || exit 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
