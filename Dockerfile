# Dockerfile del proyecto django-proyecto.
# Server de desarrollo (runserver) sobre la imagen oficial de Python 3.14.
# psycopg[binary] y Pillow traen wheels de Linux: no hace falta compilar nada.
FROM python:3.14-slim

# No escribe archivos .pyc y muestra los logs sin buffer (docker logs -f).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# tzdata para que el contenedor reconozca America/Lima (settings.py).
RUN apt-get update \
    && apt-get install -y --no-install-recommends tzdata \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Primero las dependencias: su capa queda en cache mientras el código cambie.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Después el código (la carpeta assets/ ya no existe: el media vive,
# exclusivamente, en el bucket AWS S3).
COPY . .

EXPOSE 8000

# Health contra la ruta raíz de la app (health/views.py: GET / → health-check).
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request, sys; urllib.request.urlopen('http://127.0.0.1:8000/') or sys.exit(1)" || exit 1

# Migraciones automáticas al arrancar y server escuchando en 0.0.0.0.
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
