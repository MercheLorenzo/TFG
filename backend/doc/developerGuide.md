# 📖 Developer Guide

## 📌 Index:

- [🏗️ Project Structure and Adding New Models](#-project-structure-and-adding-new-models)
- [📦 Running the Application with PyInstaller](#-running-the-application-with-pyinstaller)

---

## 🏗️ Project Structure and Adding New Models

If you wish to add a new model (e.g., companies, workers, clients...), you can copy the users or the workers files, and modify/add things on them. To add a new model, follow these steps:

1. **📦 Model:** Create a Pydantic model in the `Models` directory.
2. **🧠 Logic Class:** Implement the business logic in a separate class.
3. **🗂️ Controller:** Create a controller to handle CRUD operations and any specific logic.
4. **🌐 Routes:** Define routes that expose the model's operations using APIRouter.
5. **✅ Final Step - Routes Registration:** Register the routes in `app.py` (the main application file).

Use the USERS or WORKERS model as a template for any new model you want to add. This ensures that your project maintains a consistent and organized structure.

### **Example of Creating a New Model**

1. 📦 Model → `src/Model/workerModel.py`:

Define the data schema using Pydantic for `Worker` similar to `User`.

2. 🧠 Logic Class → `src/Lib/WorkerClass/workerClass.py`:

Implement functions to create, read, update, and delete (CRUD) or the functions of your choice for `Worker` following the structure of `userClass.py`.

3. 🗂️ Controller → `src/Controllers/workerController.py`:

Add logic for operations specific to the `Workers` model.

4. 🌐 Routes → `src/Routes/workerRoutes.py`:

Define routes to create, retrieve, update, and delete clients in the project, similar to `userRoutes.py`, or the ones of your choice.

5. ✅ Final Step - Routes Registration in `app.py`.
 
## 📦 Running the Application with PyInstaller

You can create an executable from a Python app using `PyInstaller`. 

1. Build the Executable:

Run the following PyInstaller command to package the app into a single file:

```sh
pyinstaller --onefile \
  --add-data "src:src" \
  --hidden-import=pydantic_settings \
  --hidden-import=pytz \
  --hidden-import=jwt \
  --hidden-import=beanie \
  src/app.py
```

This will generate an executable that is packaged with all the configuration, and it also includes extra dependencies like `pydantic_settings`, `pytz`, `jwt`, and `beanie`.

2. Use the `.spec` file:

Once you've generated the executable with PyInstaller, it will create an `app.spec` file. For future runs, you can simply use this `.spec` file, which automatically bundles everything. You can just execute:

```sh
pyinstaller app.spec
```

This will run your application more efficiently without having to write out the `--add-data` or `--hidden-import` flags again.