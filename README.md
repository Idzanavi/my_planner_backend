# My planner application backend

## Setup

Install: python

Clone the repository:

```sh
$ git clone https://github.com/Idzanavi/my_planner_backend.git
$ cd my_planner_backend
```

Create a virtual environment:

For Windows:
```sh
$ python -m pip install --user virtualenv
$ python -m venv env
``` 

For Unix/MacOS:
```sh
$ python3 -m pip install --user virtualenv
$ python3 -m venv env
``` 


Activate a virtual environment:


For Windows:
```sh
$ .\env\Scripts\activate
```

For Unix/MacOS:
```sh
$ source env/bin/activate
```

Install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv`.

After `pip` has finished downloading the dependencies.
Run server:
```sh
(env)$ python manage.py runserver
```

The backend was started.