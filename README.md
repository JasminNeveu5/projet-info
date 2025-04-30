# 🏁 Projet de traitement de données - Formule 1


This is a project for the course "Traitement de données" at the ENSAI, where we analyze data from the Formula 1 World Championship. The project is divided into two parts: a data analysis part and a machine learning part.

## 📦 Installing Dependencies

The required dependencies for the project are listed in the `requirements.txt` file. To install them, follow these steps:

1. Make sure you have Python 3.8 or later installed on your machine.
2. Install the dependencies using the following command:

   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Running the CLI Application

To run the CLI application, use the ```python main.py``` file as the entry point. Here's how to laucn it

1. Ensure you are in the root directory of the project.
2. Run the following command:

```bash
python -m project-info
```

## 🔗 Running the API


To run the API, use the `src/api/main.py` file as the entry point. Here's how to launch it:

1. Ensure you have `fastapi` installed (it is included in `requirements.txt`).
2. Run the following command:
```bash
fastapi dev src/api/main.py
```


## 🧪 Running Tests

The project includes test files to verify the functionality of its features. To run the tests:

1. Ensure you have ```pytest``` installed (it is included in `requirements.txt`).
2. Run the test using the following command:

```bash
pytest -v
```
