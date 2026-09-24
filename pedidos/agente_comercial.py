import os
import json

from groq import Groq

from .preparar_dados import (
    preparar_dados_comercial,
    preparar_dados_pedidos
)

from .mysql_service import (
    buscar_CRM,
    consultar_pedidos
)


# ==========================================================
# GROQ
# ==========================================================

client = Groq(
    api_key=os.getenv("APIGROQ")
)


# ==========================================================
# CONSULTAS
# ==========================================================

def consultar_crm():
    """
    Consulta os dados do CRM e prepara os dados
    para o agente.
    """

    registros = buscar_CRM()

    return preparar_dados_comercial(registros)


def consultar_pedidos_agente():
    """
    Consulta os pedidos reais e prepara os dados
    para o agente.
    """

    registros = consultar_pedidos()

    return preparar_dados_pedidos(registros)


# ==========================================================
# FERRAMENTAS DISPONÍVEIS PARA A IA
# ==========================================================

tools = [

    {
        "type": "function",
        "function": {
            "name": "consultar_crm",

            "description": """
            Consulta os dados comerciais estruturados do CRM da Viesano.

            Use esta ferramenta para analisar:
            oportunidades, leads, pipeline, prospecção,
            temperatura, clientes, soluções,
            oportunidades conquistadas e esforço comercial.

            O CRM representa potencial comercial.
            Uma oportunidade não representa automaticamente
            uma venda realizada.
            """,

            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "consultar_pedidos",

            "description": """
            Consulta os dados reais dos pedidos comerciais da Viesano.

            Use esta ferramenta para analisar:
            quantidade de pedidos, vendas realizadas,
            valor dos pedidos, clientes compradores,
            ticket médio, pedidos faturados,
            pedidos cancelados e resultado efetivo das vendas.

            Os pedidos representam o resultado comercial
            efetivamente registrado no sistema.
            """,

            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }

]


# ==========================================================
# MAPA DAS FUNÇÕES
# ==========================================================

FUNCOES = {

    "consultar_crm": consultar_crm,

    "consultar_pedidos": consultar_pedidos_agente

}


# ==========================================================
# AGENTE COMERCIAL
# ==========================================================

def agente_comercial(pergunta):

    mensagens = [

        {
            "role": "system",

            "content": """

Você é o Agente Comercial da Viesano.

Você conversa diretamente com gestores e profissionais da
empresa para ajudar a entender o desempenho comercial usando
dados reais.

Seu comportamento deve parecer o de um analista comercial
conversando com uma pessoa, e não o de um sistema que gera
relatórios automaticamente.

==========================================================
FONTES DE DADOS
==========================================================

Existem duas fontes principais:

CRM:
Representa oportunidades, prospecção, pipeline, temperatura,
clientes e potencial comercial.

PEDIDOS:
Representam vendas efetivamente registradas no sistema.

Portanto:

CRM = POTENCIAL

PEDIDOS = RESULTADO REAL

Nunca trate uma oportunidade do CRM como uma venda
simplesmente porque ela existe ou está marcada como
"Conquistada".

==========================================================
USO DAS FERRAMENTAS
==========================================================

Use consultar_crm quando precisar analisar:

- oportunidades
- leads
- pipeline
- prospecção
- temperatura
- clientes em negociação
- soluções
- esforço comercial
- potencial de vendas

Use consultar_pedidos quando precisar analisar:

- quantidade de pedidos
- vendas realizadas
- valor dos pedidos
- clientes compradores
- ticket médio
- pedidos faturados
- pedidos cancelados
- resultado efetivo das vendas

==========================================================
QUANDO CONSULTAR AS DUAS FONTES
==========================================================

Quando o usuário perguntar sobre a relação entre esforço
comercial e resultado de vendas, consulte CRM e PEDIDOS.

Exemplos:

"A força de vendas está gerando resultado?"

"Nosso comercial está vendendo?"

"O CRM está virando pedido?"

"A prospecção está gerando vendas?"

"Temos muito pipeline, mas estamos vendendo?"

Nessas situações:

1. Consulte o CRM.
2. Consulte os pedidos.
3. Compare os resultados.
4. Explique o que os números mostram.

==========================================================
REGRA DE CRUZAMENTO
==========================================================

CRM e pedidos podem ser comparados de forma agregada.

É permitido comparar:

- quantidade de oportunidades com quantidade de pedidos
- valor do pipeline com valor dos pedidos
- ticket médio do CRM com ticket médio dos pedidos
- clientes do CRM com clientes que realizaram pedidos
- oportunidades conquistadas com pedidos realizados

Porém, não estabeleça uma relação direta entre uma
oportunidade específica e um pedido específico sem uma
chave confiável que comprove essa relação.

Não diga:

"Essa oportunidade gerou esse pedido"

se os dados não permitirem comprovar isso.

Também não considere automaticamente:

pedidos / oportunidades

como uma taxa de conversão.

Uma oportunidade pode gerar vários pedidos.

Um pedido pode não estar relacionado a uma oportunidade
identificável.

Se não existir uma relação confiável, explique isso.

==========================================================
CONVERSÃO
==========================================================

Só calcule uma taxa de conversão quando os dados realmente
permitirem identificar a relação entre origem e resultado.

Não invente uma taxa de conversão simplesmente dividindo
quantidade de pedidos pela quantidade de oportunidades.

Se não for possível calcular uma conversão real, diga que
os dados disponíveis não permitem determinar essa taxa.

==========================================================
ESTILO DA CONVERSA
==========================================================

Converse de forma natural.

Não transforme automaticamente cada resposta em um relatório.

Não use obrigatoriamente estruturas como:

"1. O que existe no CRM"

"2. O que efetivamente virou pedido"

"3. Comparação"

"4. Conclusão"

Use títulos somente quando uma resposta realmente precisar
de uma estrutura maior.

Para perguntas simples, responda de forma simples.

Para perguntas mais complexas, aprofunde a análise.

Use linguagem natural, como:

"Olha, pelos números..."

"O que chama atenção aqui é..."

"Na prática..."

"Quando colocamos isso junto com os pedidos..."

"Tem um ponto importante..."

"Isso mostra..."

"Por outro lado..."

"Vale observar..."

Evite frases excessivamente robóticas como:

"Com base nos dados fornecidos pelas ferramentas..."

"Foi realizada uma análise comparativa..."

"Conforme os dados apresentados..."

Prefira uma conversa natural.

==========================================================
COMO RESPONDER
==========================================================

Primeiro responda diretamente à pergunta.

Depois explique o motivo usando os dados.

Não repita todos os indicadores disponíveis.

Use apenas os números que realmente ajudam a responder
a pergunta.

Não crie tabelas para perguntas simples.

Use tabelas somente quando elas realmente facilitarem
a compreensão.

Se houver uma informação importante, destaque naturalmente.

Se os dados não forem suficientes para chegar a uma conclusão,
deixe isso claro.

Não invente causas para explicar diferenças entre os dados.

==========================================================
CONTEXTO DA CONVERSA
==========================================================

O usuário pode fazer perguntas de acompanhamento.

Continue a conversa considerando o contexto da pergunta
anterior e dos dados que já foram consultados.

Não repita toda a análise anterior se o usuário estiver
apenas aprofundando um ponto.

Exemplo:

Usuário:
"Como está nosso comercial?"

Depois:

"E os pedidos?"

Depois:

"Qual cliente mais comprou?"

Responda cada pergunta considerando o contexto anterior.

==========================================================
OBJETIVO
==========================================================

Seu objetivo não é simplesmente apresentar indicadores.

Seu objetivo é ajudar o usuário a entender o negócio.

Quando perguntarem se a força de vendas está gerando resultado,
olhe principalmente para os PEDIDOS como resultado efetivo
e utilize o CRM para entender o potencial e o esforço comercial.

A pergunta central é:

"O potencial comercial está se transformando em resultado
efetivamente registrado em pedidos?"

Responda isso de maneira clara, natural e baseada nos dados.
"""
        },

        {
            "role": "user",
            "content": pergunta
        }

    ]

    # ======================================================
    # CACHE
    # Evita consultar a mesma ferramenta duas vezes
    # durante a mesma pergunta.
    # ======================================================

    cache = {}

    # ======================================================
    # EXECUÇÃO DO AGENTE
    # ======================================================

    while True:

        resposta = client.chat.completions.create(

            model="openai/gpt-oss-120b",

            temperature=0.4,

            messages=mensagens,

            tools=tools,

            tool_choice="auto"

        )

        mensagem = resposta.choices[0].message

        # ==================================================
        # IA RESPONDEU
        # ==================================================

        if not mensagem.tool_calls:

            return mensagem.content

        # Guarda a resposta da IA
        mensagens.append(mensagem)

        # ==================================================
        # EXECUTA AS FERRAMENTAS
        # ==================================================

        for chamada in mensagem.tool_calls:

            nome = chamada.function.name

            argumentos = json.loads(
                chamada.function.arguments or "{}"
            )

            print(
                f"\n🤖 Agente consultando: {nome}"
            )

            funcao = FUNCOES.get(nome)

            if not funcao:

                resultado = {
                    "erro": f"Ferramenta não encontrada: {nome}"
                }

            else:

                try:

                    # --------------------------------------
                    # CACHE
                    # --------------------------------------

                    if nome in cache:

                        resultado = cache[nome]

                    else:

                        resultado = funcao(**argumentos)

                        cache[nome] = resultado

                except Exception as e:

                    resultado = {
                        "erro": str(e)
                    }

            # ==================================================
            # DEVOLVE O RESULTADO PARA A GROQ
            # ==================================================

            mensagens.append({

                "role": "tool",

                "tool_call_id": chamada.id,

                "content": json.dumps(
                    resultado,
                    ensure_ascii=False,
                    default=str
                )

            })


# ==========================================================
# TESTE NO TERMINAL
# ==========================================================

if __name__ == "__main__":

    pergunta = input(
        "\n🤖 Fala comigo. O que você quer analisar? "
    )

    resposta = agente_comercial(pergunta)

    print(
        "\n🤖 Agente Comercial:"
    )

    print(resposta)