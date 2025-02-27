# Usamos una imagen base de Python 3.12 slim para mantener el tamaño reducido
FROM python:3.12-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo requirements.txt y lo instalamos primero (para aprovechar el cache de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el proyecto (código y datos) en el contenedor
COPY . .

# Definimos el comando por defecto para ejecutar main.py
CMD ["python", "main.py"]