from anime_blog.celery import app

from account.utils import send_activation_code, send_beat_mail


@app.task
def send_activation_code_task(activation_code, email):
    send_activation_code(activation_code, email)


@app.task
def send_beat_mail_task(email):
    send_beat_mail(email)
