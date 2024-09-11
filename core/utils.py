import requests, os
from django.conf import settings

def send_email(subject, message, recipient_list, from_name_email = 'PickFast <noreply@pick-fast.com>'):
    domain = settings.MAILGUN_DOMAIN
    response = requests.post(
        f"https://api.eu.mailgun.net/v3/{domain}/messages",
        auth=("api", os.getenv('MAILGUN_API_KEY')),
        data={"from": from_name_email,
              "to": recipient_list,
              "subject": subject,
              "text": message})
    print("Email status: ", response.status_code)
