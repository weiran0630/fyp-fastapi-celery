web: gunicorn -w 3 -k uvicorn.workers.UvicornWorker app.main:app
worker: celery --app app.celery_queue.worker worker -l info -c 3