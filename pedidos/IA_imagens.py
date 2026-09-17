import os
import requests

from dotenv import load_dotenv
from pathlib import Path
from gradio_client import Client

load_dotenv()


def generate_image_gradio():

    prompt = (
        "Professional premium advertising photography for Viesano "
        "Suplementos, a Brazilian dietary supplements company. "
        "Modern supplement manufacturing facility, premium capsules, "
        "supplement powders and elegant supplement containers. "
        "Clean pharmaceutical and industrial environment, quality "
        "control, technology and innovation. Sophisticated corporate "
        "visual identity using subtle blue and turquoise tones. "
        "Realistic high-end commercial photography, cinematic soft "
        "lighting, premium composition, wide horizontal banner, "
        "no people, no text, no logos."
    )

    print("Gerando nova imagem da semana...")

    client = Client(
        "black-forest-labs/FLUX.1-schnell"
    )

    resultado = client.predict(
        prompt=prompt,
        seed=0,
        randomize_seed=True,
        width=1536,
        height=1024,
        num_inference_steps=4,
        api_name="/infer"
    )

    imagem_origem = resultado[0]

    # Pasta static/img do Django
    pasta_imagem = (
        Path(__file__).resolve().parent
        / "pedidos"
        / "static"
        / "img"
    )

    pasta_imagem.mkdir(
        parents=True,
        exist_ok=True
    )

    caminho_imagem = (
        pasta_imagem / "login_destaque.png"
    )

    # Substitui a imagem anterior
    with open(imagem_origem, "rb") as origem:

        with open(caminho_imagem, "wb") as destino:

            destino.write(origem.read())

    print("Imagem gerada com sucesso.")
    print(f"Imagem atual: {caminho_imagem}")

