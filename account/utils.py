from django.core.mail import send_mail


def send_activation_code(email, activation_code):
    message = f"You registered! Activate your account and send us this code {activation_code}"
    send_mail(
        'Account activation',
        message,
        'test@gmail.com',
        [email]
    )


def send_beat_mail(email):
    send_mail(
        'Mailing subscribe',
        'You will get message every 10 minutes',
        'test@gmail.com',
        [email]
    )
