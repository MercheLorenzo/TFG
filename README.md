# 🧑‍💻 TFG - Desarrollo de Microservicios con Azure AI en Python

Bienvenido/a al repositorio del TFG de Mercedes Lorenzo Aragón. Aquí tienes instrucciones para ejecutar el **backend** y el **frontend**.

---

## 🚀 Cómo ejecutar el backend

1. Entra en la carpeta del backend:

   ```bash
   cd backend
   ```

2. Activa el entorno virtual:

   ```bash
    source venv/bin/activate
   ```
   
3. Instala las dependencias:

   ```bash
    pip install -r requirements.txt
   ```

4. Construye la imagen Docker:

   ```bash
    docker build -t backend .
   ```
   
5. Ejecuta el contenedor Docker:

   ```bash
    docker run -p 8000:8000 --env-file /home/mercedes/config/.env.development -v /home/mercedes/config:/microservice/config -it backend
   ```

---

## 🌐 Cómo ejecutar el frontend

1. Entra en la carpeta del frontend:

   ```bash
   cd frontend
   ```

2. Activa el entorno virtual:
   
   ```bash
    source venv2/bin/activate
   ```
   
3. Instala las dependencias:

   ```bash
    pip install -r requirements.txt
   ```

4. Construye la imagen Docker:

   ```bash
    docker build -t flask-frontend .
   ```

6. Ejecuta el contenedor Docker:

   ```bash
    docker run -p 5000:5000 --env-file /home/mercedes/frontConfig/.env -v /home/mercedes/frontConfig:/frontend/config -it flask-frontend
   ```

---

## 📄 Notas

- Asegúrate de tener Docker instalado y funcionando.
- Las rutas de los archivos `.env` y las carpetas montadas (`-v`) deben existir y contener la configuración necesaria.
- Para salir de los contenedores usa `Ctrl + C`.
- Debes tener el contenedor de **MongoDB Community Server** en tu Docker y abierto para que se conecten a la base de datos.  
  Puedes encontrarlo aquí: [MongoDB Community Server en Docker Hub](https://hub.docker.com/r/mongodb/mongodb-community-server)

