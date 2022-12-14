# Генератор имен выгруженных файлов
from datetime import datetime
from os.path import splitext

# Цифровая подпись
from django.template.loader import render_to_string
from django.core.signing import Signer
from bboard.settings import ALLOWED_HOSTS

signer = Signer()

def send_activation_notification(user):
    # Поиск адреса страницы активации
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'

    # Добавление id пользователя с цифровой подписью
    context = {'user':user, 'host':host, 'sign':signer.sign(user.username)}
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string('email/activation_letter_body.txt', context)
    user.email_user(subject, body_text)

# Создает имя выгруженного файла используя текущие временнЫе отметки
def get_timestamp_path (instance, filename):
    # return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])
    return f"{datetime.now().timestamp()} {splitext(filename)[1]}"
