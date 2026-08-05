from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("APIGROQ")
)


def gerar_relatorio(dados):

    prompt = f"""
Você é o Diretor Industrial da Viesano Suplementos.

Conhece processos de:

- Fracionamento
- Mistura
- Envase

Sua função é interpretar indicadores industriais.

Regras:

- Nunca invente números.

- Nunca critique uma perda sem dizer se ela é aceitável.

- Sempre considere que perdas de até 3% são normais em processos industriais.

- Compare uma OP com outra.

- Identifique tendências.

- Explique os motivos prováveis.

- Fale como um gerente industrial.

No final gere:

Resumo Executivo

Pontos Positivos

Pontos de Atenção

Gargalos

Ações Recomendadas

Nota da Produção (0 a 10)

{json.dumps(dados, indent=4, ensure_ascii=False)}
"""

    resposta = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        temperature=0.3,

        messages=[
            {
                "role": "system",
                "content": "Você é um especialista em gestão industrial."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

    )

    return resposta.choices[0].message.content



def gerar_relatorio_comercial(dados):

    prompt = f"""
Você é o Diretor Comercial da Viesano Suplementos.

Contexto da empresa:

- Indústria nova de suplementos alimentares.
- Foco em expansão comercial e conquista de novos clientes.
- Equipe comercial composta por apenas um vendedor.
- O CRM é gerenciado pelo ERP Omie.
- Não recomende implantação de sistemas, ERP, CRM, dashboards, treinamentos ou contratação de pessoas.

Regras:

- Analise apenas os dados recebidos.
- Nunca invente informações.
- Sempre justifique suas conclusões.
- Quando os dados forem insuficientes, informe isso.
- Transforme números em decisões de negócio.
- Evite apenas repetir os dados.

Temperatura comercial:

100 = Muito alta probabilidade de fechamento
60 = Boa probabilidade
40 = Em negociação
25 = Baixa probabilidade
10 = Muito baixa probabilidade

Sua análise deve identificar:

- Clientes prioritários
- Concentração do pipeline
- Riscos comerciais
- Motivos de perda
- Oportunidades de maior valor
- Clientes estratégicos
- Tendências observadas
- Ações práticas para a equipe comercial

Toda recomendação deve estar baseada em um cliente ou indicador presente nos dados.

Estruture a resposta em:

1. Resumo Executivo
2. Situação do Pipeline
3. Clientes Prioritários
4. Riscos Comerciais
5. Oportunidades
6. Recomendações
7. Plano de Ação
8. Nota da Saúde Comercial

Dados:

{json.dumps(dados, indent=4, ensure_ascii=False)}

"""

    resposta = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        temperature=0.3,

        messages=[

            {
                "role": "system",
                "content": "Você é um Diretor Comercial especialista em CRM, gestão de pipeline, vendas B2B e análise de indicadores comerciais."
            },

            {
                "role": "user",
                "content": prompt
            }

        ]

    )

    return resposta.choices[0].message.content