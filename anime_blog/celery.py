import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anime_blog.settings')
app = Celery('anime_blog')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    'send-spam-every-5-minute': {
        'task': 'account.tasks.send_beat_email_task',
        'schedule': crontab(minute='*/5'),
    },
}
