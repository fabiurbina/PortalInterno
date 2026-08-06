from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("APIGROQ")
)


def gerar_relatorio_producao(dados):

    prompt = f"""
Você é o Diretor Industrial da Viesano Suplementos, especialista em PCP, Engenharia de Produção e Gestão Industrial.

Sua responsabilidade é interpretar os indicadores industriais de forma objetiva, executiva e profissional.

## Regras obrigatórias

- Utilize SOMENTE os dados fornecidos.
- Nunca invente valores.
- Nunca suponha informações inexistentes.
- Sempre compare as Ordens de Produção quando houver mais de uma.
- Considere que perdas de até 3% são aceitáveis em processos industriais, salvo indicação contrária.
- Explique os possíveis motivos técnicos para perdas elevadas.
- Escreva como um Diretor Industrial apresentando um relatório para a diretoria.
- Utilize Markdown.
- Utilize títulos H1 (#) para cada seção.
- Utilize listas quando necessário.
- Destaque números importantes utilizando **negrito**.
- Não escreva introduções longas.

Sua resposta DEVE seguir exatamente esta estrutura:

# 📊 Resumo Executivo

Faça um resumo da situação geral da produção.

# 📈 Situação da Produção

Analise:

- quantidade de OPs
- tempo total
- tempo médio
- produtividade
- eficiência

# 🏭 Comparação entre OPs

Compare o desempenho entre as OPs.

Destaque:

- melhor desempenho
- pior desempenho
- diferenças relevantes

# 📉 Análise das Perdas

Explique as perdas de:

- Fracionamento
- Mistura
- Envase

Informe quando as perdas estiverem dentro do esperado.

# ⚠️ Gargalos Identificados

Explique quais etapas merecem atenção.

# ✅ Pontos Positivos

Liste os principais pontos positivos observados.

# 💡 Ações Recomendadas

Liste ações práticas para melhorar a produção.

# 🎯 Nota Geral da Produção

Atribua uma nota de **0 a 10**.

Explique em poucas linhas o motivo da nota.

Dados disponíveis:

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

# CONTEXTO

A Viesano é uma indústria de suplementos alimentares em expansão.

Objetivo da análise:
Fornecer um relatório executivo que permita ao gestor tomar decisões rápidas sobre o pipeline comercial.

O CRM é gerenciado pelo ERP Omie.

Nunca recomende:

- trocar ERP
- implantar CRM
- implantar dashboards
- contratar vendedores
- realizar treinamentos
- trocar processos sem evidências

Seu papel é interpretar os dados e apoiar a tomada de decisão.

----------------------------------------------------

# REGRAS

- Analise exclusivamente os dados fornecidos.
- Nunca invente informações.
- Nunca faça suposições.
- Toda conclusão deve estar baseada em algum indicador.
- Sempre explique o motivo da conclusão.
- Se os dados forem insuficientes, informe claramente.

Evite apenas repetir números.

Transforme os dados em decisões de negócio.

Escreva como um diretor comercial experiente apresentando um relatório para a diretoria.

----------------------------------------------------

# TEMPERATURA COMERCIAL

100 = Muito alta probabilidade de fechamento

60 = Boa probabilidade

40 = Em negociação

25 = Baixa probabilidade

10 = Muito baixa probabilidade

Sempre considere a temperatura comercial na priorização das oportunidades.

----------------------------------------------------

# FORMATO DA RESPOSTA

Utilize Markdown.

Utilize títulos.

Utilize listas.

Utilize frases curtas.

Evite blocos grandes de texto.

Destaque valores importantes em **negrito**.

Destaque nomes de clientes em **negrito**.

Utilize emojis apenas nos títulos.

----------------------------------------------------

# ESTRUTURA OBRIGATÓRIA

# 📊 Resumo Executivo

Escreva no máximo cinco linhas.

Explique rapidamente a situação comercial.

----------------------------------------------------

# 📈 Situação do Pipeline

Informe:

- quantidade de oportunidades
- valor total
- concentração
- temperatura média
- qualidade do pipeline

Explique o significado desses indicadores.

----------------------------------------------------

# 🎯 Clientes Prioritários

Liste apenas clientes que realmente merecem atenção.

Para cada cliente informe:

- motivo
- valor
- temperatura
- prioridade

----------------------------------------------------

# ⚠️ Riscos Comerciais

Liste apenas riscos reais encontrados.

Explique o impacto de cada risco.

----------------------------------------------------

# 💰 Oportunidades de Maior Valor

Liste as oportunidades mais relevantes.

Explique por que elas são estratégicas.

----------------------------------------------------

# 💡 Recomendações

Escreva recomendações objetivas.

Cada recomendação deve estar ligada a algum cliente ou indicador encontrado.

----------------------------------------------------

# 🚀 Plano de Ação

Divida em:

## Hoje

## Esta semana

## Este mês

Escreva ações práticas.

----------------------------------------------------

# ❤️ Nota da Saúde Comercial

Dê uma nota de 0 a 10.

Explique em poucas linhas os motivos da nota.

Finalize com uma conclusão executiva de no máximo três linhas.

----------------------------------------------------

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