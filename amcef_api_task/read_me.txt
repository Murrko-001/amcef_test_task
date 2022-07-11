AMCEF test task
microservice for managing posts

Python 3.9.5 on win32

How to run the service:
1. open terminal in the directory of the file ("...\amcef_api_task")

2. create virtual environment:  "py -3 -m venv venv"
                                "venv\Scripts\activate"

3. install all dependencies:    "pip install -r requirements.txt"

5. change directory to "...\amcef_api_task\src"
4. run python from the terminal
5. set up and run flask app:    "set FLASK_APP=app.py"
                                "set FLASK_ENV=development"
                                "flask run"

(in case it doesn't work, try upgrading your pip, and reinstalling requirements.txt)
