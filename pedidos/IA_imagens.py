from pathlib import Path

from gradio_client import Client
from dotenv import load_dotenv
from PIL import Image
import os
import requests

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

    # Converte a imagem gerada para PNG
    imagem = Image.open(imagem_origem)
    imagem.save(
        caminho_imagem,
        "PNG"
    )
    
    url_portal = "https://interno.viesano.com.br/receber-login-destaque/"

    token = os.getenv("LOGIN_DESTAQUE_TOKEN")

    with open(caminho_imagem, "rb") as arquivo:
        resposta = requests.post(
            url_portal,
            files={
                "imagem": (
                    "login_destaque.png",
                    arquivo,
                    "image/png"
                )
            },
            headers={
                "Authorization": f"Bearer {token}"
            },
            timeout=120
        )

    if resposta.status_code == 200:
        print("Imagem enviada para o PortalInterno com sucesso.")
    else:
        print(
            f"Erro ao enviar imagem: "
            f"{resposta.status_code} - {resposta.text}"
        )

    print("Imagem gerada com sucesso.")
    print(f"Imagem atual: {caminho_imagem}")


if __name__ == "__main__":
    generate_image_gradio()