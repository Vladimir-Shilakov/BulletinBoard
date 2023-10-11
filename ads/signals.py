from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings


def reply_notifications(author):

    html_content = render_to_string(
        'reply_created.html',
        {
            'link': f'{settings.SITE_URL}/replies',
        }
    )

    msg = EmailMultiAlternatives(
        subject='Здравствуйте!На ваше объявление есть отклик',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[author],
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_message_reply_confirmed(sender):
    send_mail(
        subject=f'Ваш отклик приняли.',
        message=f'Ваш отклик приняли.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[sender],
        fail_silently=False,
    )

