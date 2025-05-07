# Formule 1 : pourquoi la saison de 2025 prend-elle un virage inattendu ?
```
 ____                            __
/\  _`\               __        /\ \__
\ \ \L\ \_ __   ___  /\_\     __\ \ ,_\
 \ \ ,__/\`'__\/ __`\\/\ \  /'__`\ \ \/
  \ \ \/\ \ \//\ \L\ \\ \ \/\  __/\ \ \_
   \ \_\ \ \_\\ \____/_\ \ \ \____\\ \__\
    \/_/  \/_/ \/___//\ \_\ \/____/ \/__/
                     \ \____/
                      \/___/
 __                       __                                     __
/\ \__                 __/\ \__                                 /\ \__
\ \ ,_\  _ __    __   /\_\ \ ,_\    __    ___ ___      __    ___\ \ ,_\
 \ \ \/ /\`'__\/'__`\ \/\ \ \ \/  /'__`\/' __` __`\  /'__`\/' _ `\ \ \/
  \ \ \_\ \ \//\ \L\.\_\ \ \ \ \_/\  __//\ \/\ \/\ \/\  __//\ \/\ \ \ \_
   \ \__\\ \_\\ \__/.\_\\ \_\ \__\ \____\ \_\ \_\ \_\ \____\ \_\ \_\ \__\
    \/__/ \/_/ \/__/\/_/ \/_/\/__/\/____/\/_/\/_/\/_/\/____/\/_/\/_/\/__/


  __                  __
 /\ \                /\ \
 \_\ \     __        \_\ \    ___     ___     ___      __     __    ____
 /'_` \  /'__`\      /'_` \  / __`\ /' _ `\ /' _ `\  /'__`\ /'__`\ /',__\
/\ \L\ \/\  __/     /\ \L\ \/\ \L\ \/\ \/\ \/\ \/\ \/\  __//\  __//\__, `\
\ \___,_\ \____\    \ \___,_\ \____/\ \_\ \_\ \_\ \_\ \____\ \____\/\____/
 \/__,_ /\/____/     \/__,_ /\/___/  \/_/\/_/\/_/\/_/\/____/\/____/\/___/

```



This is a project for the course "Traitement de données" at the ENSAI, where we analyze data from the Formula 1 World Championship. The project is divided into two parts: a data analysis part and a machine learning part.

## Installing Dependencies

The required dependencies for the project are listed in the `requirements.txt` file. To install them, follow these steps:

1. Make sure you have Python 3.8 or later installed on your machine.
2. Go to the root directory of the project, then setup your virtual environment:
   ```bash
   python -m venv env
   ```
3. Install the dependencies using the following command:
   ```bash
   pip install -r requirements.txt
   ```

## Running the CLI Application

To run the CLI application, use the ```python main.py``` file as the entry point. Here's how to laucn it

1. Ensure you are just up the root directory of the project. (example: go in the project then `cd ..`)
2. Run the following command:

```bash
python -m projet-info
```

## Running the API


To run the API, use the `src/api/main.py` file as the entry point. Here's how to launch it:

1. Ensure you have `fastapi` installed (it is included in `requirements.txt`).
2. Run the following command:
```bash
fastapi dev src/api/main.py
```
3. You can access the API documentation after running the server by navigating to `http://localhost:8000/docs` in your web browser. This will provide you with an interactive interface to test the API endpoints.


## Running Tests


The project includes test files to verify the functionality of its features. To run the tests:

1. Ensure you have ```pytest``` installed (it is included in `requirements.txt`).
2. Run the test using the following command:

```bash
pytest -v
```


## Playground

Grab your hats, beach toys and sunscreen, and have some fun on the playground playing with the functions !
## Pylint bonus test

1. Ensure you have pylint install and that you are in the root directory
2. run the following command to chack how good or bad the code is:
```bash
pylint . --disable=C0114,C0115,R0903,C0301,C0116,C0103,W0612,E0401
```

The disabled codes are import errors and name file errors that have too big of an impact on the score despite the first one depending on your PYTHONPATH and the other one is pure convention.
