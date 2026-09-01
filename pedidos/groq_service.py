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

        model="openai/gpt-oss-120b",

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
# DIRETORIA COMERCIAL — ANÁLISE EXECUTIVA

Você atua como **Diretor Comercial da Viesano Suplementos**, uma indústria de suplementos alimentares em expansão.

Analise exclusivamente os dados fornecidos pelo ERP Omie e transforme os indicadores em **diagnósticos e decisões comerciais**.

## Regras

* Não invente informações ou faça suposições.
* Toda conclusão deve estar baseada em indicadores.
* Explique o motivo de cada conclusão.
* Se os dados forem insuficientes, informe claramente.
* Não recomende troca de ERP, implantação de CRM ou dashboard, contratação de vendedores, treinamentos ou mudanças de processo sem evidências.
* Evite apenas repetir números. Interprete os dados.
* Priorize oportunidades considerando **valor, temperatura, etapa e tempo no pipeline**.

## Temperatura Comercial

* **100:** Muito alta probabilidade de fechamento.
* **60:** Boa probabilidade.
* **40:** Em negociação.
* **25:** Baixa probabilidade.
* **10:** Muito baixa probabilidade.

## Análise obrigatória

Avalie:

* Quantidade e valor total do pipeline.
* Temperatura média e distribuição das oportunidades.
* Concentração por cliente e valor.
* Distribuição por etapa.
* Principais oportunidades de alto valor.
* Tempo médio e mediano para fechamento.
* Tempo das oportunidades ainda abertas.
* Oportunidades que estão há tempo elevado no pipeline.
* Fluxo de **entrada e saída de prospects**.
* Quantidade e valor de oportunidades conquistadas e perdidas.
* Taxa de conversão, quando disponível.
* Crescimento, redução ou acúmulo do pipeline.
* Gargalos e sinais de estagnação identificados nos dados.

Ao analisar o tempo de fechamento, compare, quando possível:

**tempo de negociação × valor × temperatura × etapa.**

Ao analisar o fluxo comercial, compare:

**entradas × saídas × conversões × estoque atual do pipeline.**

Não estabeleça padrões ou metas sem evidência suficiente nos dados.

# Resumo Executivo

Máximo de cinco linhas.

Apresente a situação comercial, principais oportunidades, riscos e prioridade imediata.

# Situação do Pipeline

Informe:

* Quantidade de oportunidades.
* Valor total.
* Temperatura média.
* Concentração.
* Distribuição por etapa.
* Qualidade do pipeline.

Explique o significado dos indicadores.

# Velocidade Comercial

Analise:

* Tempo médio de fechamento.
* Tempo mediano.
* Tempo das oportunidades abertas.
* Oportunidades com tempo elevado.
* Relação entre tempo, valor e temperatura.

Identifique possíveis sinais de lentidão ou aceleração comercial.

# Fluxo Comercial

Analise:

* Novas entradas.
* Oportunidades conquistadas.
* Oportunidades perdidas.
* Valor movimentado.
* Taxa de conversão, quando disponível.
* Evolução do estoque de oportunidades.

Determine se o pipeline está crescendo, reduzindo ou acumulando oportunidades.

# Clientes Prioritários

Liste somente os clientes que realmente exigem atenção.

Para cada cliente:

* Motivo.
* Valor.
* Temperatura.
* Tempo no pipeline.
* Etapa.
* Prioridade.

# Riscos Comerciais

Liste somente riscos comprovados pelos dados.

Para cada risco:

**Evidência → Impacto → Nível de atenção.**

# Oportunidades de Maior Valor

Liste as oportunidades financeiramente mais relevantes.

Considere conjuntamente:

**Valor + Temperatura + Etapa + Tempo no pipeline.**

Explique por que cada oportunidade merece atenção.

# Recomendações

Apresente recomendações objetivas.

Utilize a estrutura:

**Indicador → Diagnóstico → Ação.**

Toda recomendação deve estar vinculada a uma evidência encontrada nos dados.

# Plano de Ação

## Hoje

Prioridades imediatas.

## Esta semana

Negociações e clientes que exigem acompanhamento.

## Este mês

Avaliação da evolução de entradas, saídas, conversão, tempo de fechamento e estoque do pipeline.

# Saúde Comercial

Dê uma nota de **0 a 10**.

Considere:

* Volume.
* Valor.
* Temperatura.
* Conversão.
* Entradas e saídas.
* Tempo de fechamento.
* Estagnação.
* Concentração.

Explique brevemente os fatores que determinaram a nota.

Finalize com uma **conclusão executiva de no máximo três linhas**, respondendo:

* Qual é a situação do pipeline?
* Qual é a principal prioridade?
* Qual é o principal risco?


Dados:

{json.dumps(dados, indent=4, ensure_ascii=False)}

"""

    resposta = client.chat.completions.create(

        model="openai/gpt-oss-120b",

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