from django.conf import settings
from django.core.mail import EmailMessage

def send_email_now(subject, message, to_email, file_path):
    from_email = settings.FROM_EMAIL
    bcc_email = settings.BCC_EMAIL
    reply_to_email = settings.REPLY_TO_EMAIL

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=[to_email],
        bcc=[bcc_email],
        reply_to=[reply_to_email]
    )
    email.content_subtype = "html"
    if file_path:
        email.attach_file(file_path)
    s = email.send()
    return email, s
