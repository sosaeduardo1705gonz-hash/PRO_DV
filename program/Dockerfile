# Imagen base ligera de Python
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivos al contenedor
COPY app.py   .
COPY datos.txt .

# Variable de entorno para versión (se puede sobreescribir en runtime)
ENV VERSION=v1.0

# Ejecutar el programa al iniciar el contenedor
CMD ["python", "app.py"]
