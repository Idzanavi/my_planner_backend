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

In `settings.py` modify line: `CELERY_BROKER_URL='redis://127.0.0.1:6379'`, where 127.0.0.1 is the address of redis server

Redis and Celery should be started on Linux or WSL

Install Redis
```sh
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

sudo apt-get update
sudo apt-get install redis

```

Start Redis:
```sh
sudo service redis-server start
```

Connect to Redis (and test connection):
```sh
redis-cli 
127.0.0.1:6379> ping
PONG
```

Activate virtual environment (or use activated if have it avtivated):
```sh
$ source env/bin/activate
```

In two separate windows with activated virtual environments start:

1.Celery worker
```sh
(env)$ celery -A planner  worker --loglevel=INFO
```

2. Django-based application:
```sh
(env)$ python manage.py runserver
```

The backend was started.
You can test it with Postman (or any other tool) or connect with frontend.

The address will be: `127.0.0.1:8000`
