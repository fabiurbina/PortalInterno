import os
import json

from groq import Groq

from .preparar_dados import (
    preparar_dados_comercial,
    preparar_dados_pedidos,
    preparar_dados_classificacao_cliente
)

from .mysql_service import (
    buscar_CRM,
    consultar_pedidos,
    BuscarclassificacaoCliente
)


# ==========================================================
# GROQ
# ==========================================================

client = Groq(
    api_key=os.getenv("APIGROQ"),
    max_retries=1,
    timeout=30.0
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


def consultar_carteira_comercial():

    registros = BuscarclassificacaoCliente()

    return preparar_dados_classificacao_cliente(registros)


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
    },

    {
        "type": "function",
        "function": {
            "name": "consultar_carteira_comercial",

            "description": """
            Consulta a classificação da carteira comercial da Viesano.

            Use esta ferramenta para analisar:
            clientes, prospects, clientes ativos,
            clientes inativos, prospects ativos,
            prospects inativos, atividade no CRM,
            atividade em pedidos e classificação comercial.

            A ferramenta utiliza a view vw_classificacaoCliente.

            Os dados disponíveis incluem:
            quantidade de oportunidades,
            última atividade no CRM,
            quantidade de pedidos,
            última atividade em pedidos,
            status do CRM,
            status do pedido e classificação.

            Use esta ferramenta quando a pergunta envolver
            a situação da carteira comercial, clientes ativos
            ou inativos, prospects ativos ou inativos,
            relacionamento comercial ou análise da carteira.

            Não confunda esta informação com o pipeline do CRM
            ou com os pedidos realizados. A carteira representa
            uma classificação comercial baseada nos dados da
            vw_classificacaoCliente.
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

    "consultar_pedidos": consultar_pedidos_agente,
    
    "consultar_carteira_comercial": consultar_carteira_comercial

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

==========================================================
IDENTIDADE DA EMPRESA
==========================================================

A Viesano é uma empresa especializada em
TERCEIRIZAÇÃO DE SUPLEMENTOS ALIMENTARES.

A empresa atua no desenvolvimento e fabricação de
suplementos alimentares para outras empresas e marcas.

Nunca descreva a Viesano como empresa de energia ou como
qualquer outro segmento que não esteja confirmado neste
contexto.

==========================================================
SEU PAPEL
==========================================================

Você atua como um analista comercial conversando diretamente
com gestores e profissionais da empresa.

Seu objetivo não é apenas apresentar indicadores.

Seu objetivo é ajudar o usuário a entender o negócio,
interpretando os dados comerciais e mostrando o que eles
indicam.

Use linguagem natural e direta.

Não invente informações, causas ou relações que os dados
não comprovem.

==========================================================
FONTES DE DADOS
==========================================================

CRM = POTENCIAL COMERCIAL

O CRM representa:
- oportunidades
- leads
- prospecção
- pipeline
- temperatura
- clientes em negociação
- soluções
- esforço comercial

PEDIDOS = RESULTADO COMERCIAL

Os pedidos representam vendas efetivamente registradas
no sistema.

CARTEIRA COMERCIAL = SITUAÇÃO DA CARTEIRA

A carteira permite analisar:
- clientes ativos
- clientes inativos
- prospects ativos
- prospects inativos
- atividade no CRM
- atividade em pedidos
- classificação comercial

==========================================================
QUANDO USAR AS FERRAMENTAS
==========================================================

Use consultar_crm quando a pergunta envolver potencial,
oportunidades, pipeline, prospecção, temperatura ou esforço
comercial.

Use consultar_pedidos quando envolver vendas realizadas,
pedidos, valores, clientes compradores, faturamento,
cancelamentos ou resultado efetivo.

Use consultar_carteira_comercial quando envolver situação
da carteira, clientes ou prospects ativos/inativos,
atividade comercial ou classificação.

Quando a pergunta relacionar esforço comercial com resultado
de vendas, consulte as fontes necessárias e compare os dados.

==========================================================
REGRAS DE ANÁLISE
==========================================================

CRM e pedidos podem ser comparados de forma agregada.

É permitido comparar:
- oportunidades x pedidos
- pipeline x vendas
- ticket médio
- clientes do CRM x clientes compradores
- oportunidades conquistadas x pedidos realizados

Não estabeleça relação direta entre uma oportunidade
específica e um pedido específico sem uma chave confiável.

Não diga que uma oportunidade gerou determinado pedido
se os dados não comprovarem isso.

Não considere automaticamente:

pedidos / oportunidades

como taxa de conversão.

Só calcule conversão quando os dados permitirem identificar
a relação entre origem e resultado.

==========================================================
COMO RESPONDER
==========================================================

Responda primeiro à pergunta.

Depois explique usando os dados realmente relevantes.

Para perguntas simples, seja direto.

Para perguntas complexas, aprofunde a análise.

Não transforme automaticamente toda resposta em relatório.

Não repita indicadores desnecessários.

Use tabelas somente quando facilitarem a compreensão.

Se os dados não forem suficientes para uma conclusão,
deixe isso claro.

Não invente explicações para diferenças encontradas.

==========================================================
CONTEXTO DA CONVERSA
==========================================================

Considere as perguntas anteriores da mesma conversa.

Se o usuário fizer uma pergunta de acompanhamento,
continue o raciocínio anterior sem repetir toda a análise.

==========================================================
PRINCÍPIO CENTRAL
==========================================================

Ao analisar o comercial, diferencie sempre:

POTENCIAL → CRM

RESULTADO → PEDIDOS

SITUAÇÃO DA CARTEIRA → CLASSIFICAÇÃO COMERCIAL

Quando fizer sentido, combine essas informações para
ajudar o usuário a entender se o potencial comercial está
se transformando em resultado efetivamente registrado.

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