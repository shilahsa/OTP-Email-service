import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.config_from_object('django.conf:settings', namespace='CELERY')

# https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html#beat-entries
app.conf.beat_schedule = {
    'test_beat_5M': {
        'task': 'core.tasks.test_beat',
        'schedule': crontab(minute='*/1'),
    }
}

app.autodiscover_tasks()
