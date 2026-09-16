import os
import requests
from dotenv import load_dotenv
import os
from pathlib import Path
from huggingface_hub import InferenceClient

load_dotenv()

api_key = os.getenv("APIPOLLINATIONS")
api_keyh = os.getenv("APIHuggingFace")


def generate_image():
    prompt = (
        "Professional and modern supplement manufacturing facility, "
        "clean industrial environment, quality control, technology, "
        "blue and turquoise visual identity, cinematic lighting, "
        "wide horizontal banner, no text"
    )

    url = "https://gen.pollinations.ai/image/" + requests.utils.quote(prompt)

    response = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {api_key}"
        },
        params={
            "model": "flux"
        },
        timeout=120
    )

    if response.ok:

        caminho = r"C:\Users\fabio\OneDrive - Viesano Suplementos\Dados - TI\Site\PortalInterno\pedidos\imagem_dia.png"

        with open(caminho, "wb") as arquivo:
            arquivo.write(response.content)

        print(f"✅ Imagem salva em: {caminho}")

    else:
        print("❌ Erro:", response.text)
        
        
        
def generate_image_huggingface():
    
    if not api_keyh:
        raise ValueError("APIHuggingFace não encontrada no .env")

    # Cria o cliente
    client = InferenceClient(
        provider="fal-ai",
        api_key=api_keyh
    )

    # Gera a imagem
    image = client.text_to_image(
        prompt="A realistic golden retriever sitting in a beautiful garden",
        model="black-forest-labs/FLUX.1-schnell"
    )

    # Pasta onde este código está sendo executado
    pasta_projeto = Path(__file__).resolve().parent

    # Caminho da imagem
    caminho_imagem = pasta_projeto / "teste_huggingface.png"

    # Salva
    image.save(caminho_imagem)

    print(f"Imagem gerada com sucesso!")
    print(f"Salva em: {caminho_imagem}")



        
if __name__ == "__main__":
    
    generate_image_huggingface()