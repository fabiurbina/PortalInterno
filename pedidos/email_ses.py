import os
import boto3
from django.conf import settings

ses = boto3.client(
    "ses",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def enviar_email(assunto, destinatario, html,
                 texto="Seu e-mail não suporta HTML."):

    resposta = ses.send_email(
        Source=settings.DEFAULT_FROM_EMAIL,
        Destination={
            "ToAddresses": [destinatario]
        },
        Message={
            "Subject": {
                "Data": assunto,
                "Charset": "UTF-8"
            },
            "Body": {
                "Html": {
                    "Data": html,
                    "Charset": "UTF-8"
                },
                "Text": {
                    "Data": texto,
                    "Charset": "UTF-8"
                }
            }
        }
    )

    return resposta