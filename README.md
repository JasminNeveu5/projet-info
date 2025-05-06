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
2. Install the dependencies using the following command:

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
