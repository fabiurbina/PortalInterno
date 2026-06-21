import requests
from django.conf import settings
from django.core.cache import cache

def listar_ops():

    ops = cache.get('lista_ops')

    if ops:

        print('🟢 CACHE OPS')

        return ops

    try:

        print('🔴 OMIE OPS')

        payload = {
            "call": "ListarOrdemProducao",
            "app_key": settings.OMIE_APP_KEY,
            "app_secret": settings.OMIE_APP_SECRET,
            "param": [
                {
                    "pagina": 1,
                    "registros_por_pagina": 50
                }
            ]
        }

        response = requests.post(
            "https://app.omie.com.br/api/v1/produtos/op/",
            json=payload,
            timeout=30
        )

        retorno = response.json()

        cache.set(
            'lista_ops',
            retorno,
            timeout=1800
        )

        return retorno

    except Exception as e:

        return {
            "erro": str(e)
        }
        
def consultar_produto(codigo_produto):

    cache_key = f'produto_{codigo_produto}'

    produto = cache.get(cache_key)

    if produto:

        print(f'CACHE PRODUTO {codigo_produto}')

        return produto

    payload = {
        "call": "ConsultarProduto",
        "app_key": settings.OMIE_APP_KEY,
        "app_secret": settings.OMIE_APP_SECRET,
        "param": [
            {
                "codigo_produto": codigo_produto,
                "codigo_produto_integracao": "",
                "codigo": ""
            }
        ]
    }

    print(f'OMIE PRODUTO {codigo_produto}')

    response = requests.post(
        "https://app.omie.com.br/api/v1/geral/produtos/",
        json=payload,
        timeout=30
    )

    produto = response.json()

    cache.set(
        cache_key,
        produto,
        timeout=86400
    )

    return produto



def consultar_op(codigo_op):

    cache_key = f'op_{codigo_op}'

    op = cache.get(cache_key)

    if op:

        print(f'🟢 CACHE OP {codigo_op}')

        return op

    print(f'🔴 OMIE OP {codigo_op}')

    payload = {
        "call": "ConsultarOrdemProducao",
        "app_key": settings.OMIE_APP_KEY,
        "app_secret": settings.OMIE_APP_SECRET,
        "param": [
            {
                "cCodIntOP": "",
                "nCodOP": codigo_op
            }
        ]
    }

    response = requests.post(
        "https://app.omie.com.br/api/v1/produtos/op/",
        json=payload,
        timeout=30
    )

    op = response.json()

    cache.set(
        cache_key,
        op,
        timeout=1800
    )

    return op


def listar_locais_estoque():

    payload = {
        "call": "ListarLocaisEstoque",
        "app_key": settings.OMIE_APP_KEY,
        "app_secret": settings.OMIE_APP_SECRET,
        "param": [
            {
                "nPagina": 1,
                "nRegPorPagina": 50
            }
        ]
    }

    response = requests.post(
        "https://app.omie.com.br/api/v1/estoque/local/",
        json=payload,
        timeout=30
    )

    return response.json()


def consultar_pedido(numero_pedido):

    payload = {
        "call": "ConsultarPedido",
        "app_key": settings.OMIE_APP_KEY,
        "app_secret": settings.OMIE_APP_SECRET,
        "param": [
            {
                "numero_pedido": numero_pedido
            }
        ]
    }

    response = requests.post(
        "https://app.omie.com.br/api/v1/produtos/pedido/",
        json=payload
    )

    return response.json()


import re

def extrair_numero_pedido(texto):

    match = re.search(
        r'pedido de venda nº (\d+)',
        texto
    )

    if match:
        return int(match.group(1))

    return None


def listar_lotes():

    url = "https://app.omie.com.br/api/v1/produtos/produtoslote/"

    payload = {
        "call": "ListarLotes",
        "app_key": settings.OMIE_APP_KEY,
        "app_secret": settings.OMIE_APP_SECRET,
        "param": [
            {
                "nPagina": 1,
                "nRegPorPagina": 500
            }
        ]
    }

    response = requests.post(
        url,
        json=payload
    )

    return response.json()

    
    
def consultar_estoque_local(cod_local):

    pagina = 1

    resultados = []

    while True:

        payload = {

            "call": "ListarPosEstoque",

            "app_key": settings.OMIE_APP_KEY,

            "app_secret": settings.OMIE_APP_SECRET,

            "param": [
                {
                    "nPagina": pagina,
                    "nRegPorPagina": 50,
                    "cExibeTodos": "S",
                    "codigo_local_estoque": cod_local
                }
            ]
        }

        response = requests.post(
            settings.OMIE_API_URL_ESTOQUE,
            json=payload,
            timeout=30
        )

        data = response.json()

        produtos = data.get(
            'produtos',
            []
        )

        if not produtos:
            break

        resultados.extend(produtos)

        total_paginas = data.get(
            'nTotPaginas',
            1
        )

        if pagina >= total_paginas:
            break

        pagina += 1

    return resultados


def listar_quarentena():

    produtos = cache.get(
        'estoque_quarentena'
    )

    if produtos:

        print('🟢 CACHE QUARENTENA')

        return produtos

    print('🔴 OMIE QUARENTENA')

    produtos = consultar_estoque_local(
        1770134348
    )

    cache.set(
        'estoque_quarentena',
        produtos,
        300
    )

    return produtos


def listar_movimentos_entrada():
    
    payload = {
    "call": "ListarMovimentos",
    "app_key": settings.OMIE_APP_KEY,
    "app_secret": settings.OMIE_APP_SECRET,
    "param": [
        {
            "pagina": 1,
            "registros_por_pagina": 500,
            "codigo_local_estoque": 1770134348
        }
    ]
}
    
    
def listar_movimentos_entrada(data_inicial, data_final):

    payload = {
        "call": "ListarMovimentos",
        "app_key": settings.OMIE_APP_KEY,
        "app_secret": settings.OMIE_APP_SECRET,
        "param": [
            {
                "pagina": 1,
                "registros_por_pagina": 500,
                "data_inicial": data_inicial,
                "data_final": data_final,
                "hora_inicial": "00:00:00",
                "hora_final": "23:59:59",
                "codigo_local_estoque": 1770134348
            }
        ]
    }

    response = requests.post(
        "https://app.omie.com.br/api/v1/estoque/movestoque/",
        json=payload
    )

    data = response.json()

    entradas = []

    for produto in data.get("cadastros", []):

        for movimento in produto.get("movimentos", []):

            if movimento.get("nQtdeEntradas", 0) > 0:

                entradas.append({

                    "codigo": produto["cCodigo"],

                    "descricao": produto["cDescricao"],

                    "data": movimento["dDataMovimento"],

                    "quantidade": movimento["nQtdeEntradas"],

                    "cod_prod": produto["nCodProd"]

                })

    return entradas