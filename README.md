# fyp-fastapi-celery

Final Year Project's backend using Python FastAPI framework and Celery to serve Tensorflow Model

### Built With

-   [FastAPI](https://fastapi.tiangolo.com/)
-   [Celery](https://docs.celeryproject.org/en/stable/)
-   [Redis](https://redis.io/topics/quickstart)

### Prerequisites

-   Python 3.7.11, install specific Python version using [pyenv](https://github.com/pyenv/pyenv)
    ```sh
    pyenv install -v 3.7.11
    pyenv global 3.7.11
    ```
-   Redis installed on your machine

### Installation

1. Clone the repo
    ```sh
    git clone https://github.com/weiran0630/fyp-fastapi-celery.git
    ```
2. Create and startup Python virtual environment
    ```sh
    pip3 install virtualenv
    virtualenv .venv
    source .venv/bin/activate
    ```
3. Install Python packages
    ```sh
    pip install -r requirement.txt
    ```

### Run apps locally using [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

1. Set up local environment variables
    ```sh
    touch .env
    open .env
    ```
    Here’s an example .env file:
    ```
    REDIS_TLS_URL=rediss://
    REDIS_URL=redis://
    ```
2. Start up Redis server

    ```sh
    redis-server
    ```

3. Locally start all of the process types that are defined in Procfile
    ```sh
    heroku local
    ```

### Test and document your API using OpenAPI Swagger

-   Open your browser and navigate: http://localhost:5000/docs
