from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_template_email(to_email, subject, template_name, context):
    html_message = render_to_string(template_name, context)
    send_mail(
        subject=subject,
        message='',
        from_email='no-reply@hapipay.com',  # Adjust if needed
        recipient_list=[to_email],
        html_message=html_message,
        fail_silently=True,  # Fail safe
    )

def strip_tags(html):
    """Very basic HTML tag stripper for plain text fallback."""
    import re
    return re.sub('<[^<]+?>', '', html)
