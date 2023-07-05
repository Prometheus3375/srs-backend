# srs-backend

## 0. Requirements

1. Install [Python 3.8.2](https://www.python.org/downloads/release/python-382/).
2. Change current working directory to the root of this repository.
3. (Optional) Initialize virtual environment and activate it according to the
 [tutorial](https://docs.python.org/3/library/venv.html).
4. [Update pip](https://pip.pypa.io/en/stable/installing/#upgrading-pip).
5. Run `pip install --upgrade setuptools`. This will update setuptools package.
6. Run `pip install -r requirements.txt`. This will install all necessary packages for the project.

## 1. Starting the server
1. Activate your virtual environment, if any.
2. If you are starting server the first time then run `python manage.py migrate`.
3. Run `python manage.py runserver 0:8000` to start the server.
