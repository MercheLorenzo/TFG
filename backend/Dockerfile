# Dockerfile para construir la imagen del microservicio FastAPI.

# Este archivo define cómo se configura y construye la imagen Docker para la aplicación FastAPI. 

# Para construir la imagen, utiliza el siguiente comando en el directorio donde se encuentra este Dockerfile:
# docker build -t nombre_imagen .
# Para ejecutar el contenedor:
# docker run nombre_imagen
# docker run -p 8000:8000 nombre_imagen

# docker build -t nombre_imagen .
# PARA EJECUTAR EL SERVICIO (le pasas el puerto, el env file y la ruta de tu pc:la ruta del proyecto)
# docker run -p 8000:8000   --env-file .env.production   -v /home/mercedesnomia/flask_app_v1:/microservice   nombre_imagen

# ESTA PARTE es para hacer el docker a partir del ejecutable, por lo que no tendremos que instalar las dependencias, así pues será más rápido

FROM python:3.11

# Establece el directorio de trabajo
WORKDIR /microservice

# Copiar los archivos necesarios
COPY app app
#COPY config /microservice/config

# Crear la carpeta config
RUN mkdir -p /microservice/config 
# La opción -p asegura que no falle si ya existe la carpeta

# Asegúrate de que los archivos sean ejecutables
RUN chmod +x app

# Configura el comando por defecto, si es necesario
CMD ["./app"]


#-------------------
# # Definir el directorio de trabajo dentro del contenedor
# WORKDIR /microservice

# # Copiar el binario a la imagen
# COPY app /microservice/app

# # Dar permisos de ejecución al binario
# RUN chmod +x /microservice/app

# # Especificar el comando que ejecutará el contenedor
# CMD ["/microservice/app"]
#-------------------




# ESTA PARTE es para hacer el docker a partir del codigo, instalando dependencias y copiando todo

# FROM python:3.11

# WORKDIR /microservice

# COPY requirements.txt requirements.txt
# COPY .env.development .env.development
# RUN pip install -r requirements.txt
# COPY . .

# ENV PORT=8000
# EXPOSE 8000

# ENV NODE_ENV=development
# ENV PYTHONPATH=/microservice
# ENV ENV_FILE=.env.development

# CMD ["python", "src/app.py"]