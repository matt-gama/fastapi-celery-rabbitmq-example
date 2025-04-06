# app/celery_app.py

import os
from celery import Celery

broker_url = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//")
publisher = os.getenv("PUBLISHER", "default")

celery = Celery(
    "my_celery_app",
    broker=broker_url,
    backend=None,
    include=["app.tasks"]  # <--- ADICIONE ESTA LINHA
)

celery.conf.update({
    "task_default_queue": publisher,
    "worker_concurrency": 4,
})
