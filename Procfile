web: gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.main:app
worker: celery --app app.celery_queue.worker worker -l info -c 2