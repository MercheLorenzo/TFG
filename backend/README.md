# Santra Python Microservice Template - FastAPI
Backend Python FastAPI production ready template for **Santra™** micro services. ([https://www.santrame.com](https://www.santrame.com))

---

## 📋 Requirements

- `Python 3.8` or higher
- [Uvicorn](https://www.uvicorn.org/) as the ASGI server
- `pip` for managing dependencies

---

## 🚀 Development Enviroment Setup

1. First, clone the project and navigate to the directory:

   ```sh
    git clone https://github.com/NomiaEnergy/santra-python-microservice-template.git
    cd santra-python-microservice-template
    ```

2. Next, create a virtual environment using the `venv` module and activate it:

    ```sh
    python3 -m venv venv
    source venv/bin/activate # In Linux/Mac
    env\Scripts\activate  # In Windows
    ```

Make sure to do everything related to the project **inside the virtual environment** (such as installing dependencies and running the project).

3. To install dependencies:

    ```sh
    pip install -r requirements.txt
    ```

---

## 🧪 Running in Development Mode

Run the service with:

```sh
python src/app.py # This will load the default environment configuration

# If you want to load the .env.development file, use:
ENV_FILE=.env.development python src/app.py
# If you want to load the .env.production file, use:
ENV_FILE=.env.production python src/app.py
# This way you can load any environment file
```

- The server will be available in [http://localhost:8000](http://localhost:8000).
- Reload option will reload automatically the server when there are changes in the code.

If you encounter this error while doing `python src/app.py`:

```sh
ModuleNotFoundError: No module named 'src'
```

Run:

```sh
export PYTHONPATH=$PWD
python src/app.py
```

---

## 📦 Running in Production Mode (Binary Build)

```sh
./app                               # Default environment

ENV_FILE=.env.development ./app     # Development
ENV_FILE=.env.production ./app      # Production
```

---

## 🐳 Running with Docker

Ensure Docker is installed on your system.

1. Clone the repository and navigate to the project folder (if you still don't have it)

```sh
git clone https://github.com/NomiaEnergy/santra-python-microservice-template.git
cd santra-python-microservice-template
```

2. Build and start the Docker containers

Run the following command to build the Docker images and start the containers defined in the `docker-compose.yaml` file:

```sh
docker-compose up --build
```

This will:

- Build the images defined in your Dockerfile.
- Start the services defined in your `docker-compose.yaml` file (FastAPI and MongoDB).

Note: To stop the containers, use: `docker-compose down`

---

## 📄 API Documentation

You can access the interactive API documentation at:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### 📚 Further Information

- [📑 Optional Settings](./doc/optionalSettings.md) – Environment settings and test execution
- [🛠️ Developer Guide](./doc/developerGuide.md) – How to extend the project and add new models
