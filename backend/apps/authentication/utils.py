# authentication/utils.py

from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token

def send_confirmation_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)

    activation_url = request.build_absolute_uri(
        reverse('confirm-email', kwargs={'uidb64': uid, 'token': token})
    )

    subject = 'Confirma tu cuenta'
    message = f'''
    Hola {user.first_name},

    Gracias por registrarte. Para activar tu cuenta, haz clic en el siguiente enlace:

    {activation_url}

    Si no hiciste este registro, puedes ignorar este mensaje.
    '''
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        print("ERROR AL ENVIAR EMAIL:", e)