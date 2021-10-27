import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicApi.settings')
app = Celery('musicApi')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    'send-spam-every-5-minute': {
        'task': 'account.tasks.send_beat_mail_task',
        'schedule': crontab(minute='*/5'),
        'args': ({
            'email'
        },)
    },
}
