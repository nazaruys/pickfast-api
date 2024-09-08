import requests, os
from django.conf import settings

def send_email(subject, message, to_email, from_name_email = 'PickFast <noreply@pick-fast.com>'):
    print("Sending to ", to_email)
    domain = settings.MAILGUN_DOMAIN
    response = requests.post(
        f"https://api.eu.mailgun.net/v3/{domain}/messages",
        auth=("api", os.getenv('MAILGUN_API_KEY')),
        data={"from": from_name_email,
              "to": [to_email],
              "subject": subject,
              "text": message})
    print(response.status_code)
