# Usa una imagen base de Python
FROM python:3.11

# Establece el directorio de trabajo
WORKDIR /frontend

# Copia los archivos de requerimientos y código
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expone el puerto que usa Flask
EXPOSE 5000

# Comando para ejecutar la app
CMD ["python", "app.py"]
