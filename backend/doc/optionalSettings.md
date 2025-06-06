# ⚙️ Optional Settings

## 📌 Index:

- [🌍 Languages](#-languages)
- [🧪 Tests](#-tests)
- [🛠️ Version and Build Configuration](#️-version-and-build-configuration)

---

## 🌍 Languages

In the main page, [http://localhost:8000/main](http://localhost:8000/main), you can change the language. By default, the main page is in Spanish (`es`), but if you add `?lang=` + `language`, you can change it to:

- `es`: Spanish - Español
- `eng`: English - English
- `fr`: French - Français
- `de`: German - Deutsch
- `it`: Italian - Italiano
- `ch`: Chinese - 中文

By default is Spanish, and if you enter another option that is not between these ones, it will return Spanish too.

---

## 🧪 Tests

To run all the tests, inside the project directory, run the command:

```sh
PYTHONPATH=$(pwd) pytest
```

If you only want to run a specific test file, you can do:

```sh
PYTHONPATH=$(pwd) pytest test/TEST_FILE
# For example:
PYTHONPATH=$(pwd) pytest test/test_db.py
```

---

## 🛠️ Version and Build Configuration

- **📦 VERSION:** is the git version (`git describe --tags`). To add a new version, in the terminal make `git tag v1.0.x` and `git push origin v1.0.x`, and this will be automatically the new `VERSION`.
- **📆 BUILD:** is automatically the date of when running the micro service. The date is with spanish format `('%d-%m-%Y')`, you can change to another modifying the `config.py`, for ex. `('%Y-%m-%d')`
