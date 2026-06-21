# integracoes/omie.py

import requests
from django.conf import settings


class OmieClient:

    def __init__(self):
        self.app_key = settings.OMIE_APP_KEY
        self.app_secret = settings.OMIE_APP_SECRET

    def consultar_ops(self, pagina=1):

        payload = {
            "call": "ListarOrdemProducao",
            "app_key": self.app_key,
            "app_secret": self.app_secret,
            "param": [
                {
                    "pagina": pagina,
                    "registros_por_pagina": 50
                }
            ]
        }

        response = requests.post(
            "https://app.omie.com.br/api/v1/producao/op/",
            json=payload,
            timeout=30
        )

        return response.json()