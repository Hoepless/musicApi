from musicApi._celery import app
from account.utils import send_activation_code, send_beat_mail


@app.task
def send_activation_code_task(email, activation_code):
    send_activation_code(email, activation_code)


@app.task
def send_beat_mail_task(email):
    send_beat_mail(email)
