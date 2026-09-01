def preparar_dados_producao(registros):

    dados = []

    for r in registros:

        dados.append({

            "pedido": r["numero_pedido"],
            "op": r["codigo_op"],

            "tempo": {
                "total_min": int(r["tempo_total_min"]),
                "medio_etapa_min": float(r["tempo_medio_etapa_min"]),
                "fracionamento_min": int(r["tempo_fracionamento_min"]),
                "mistura_min": int(r["tempo_mistura_min"]),
                "qualidade_min": int(r["tempo_qualidade_min"]),
                "envase_min": int(r["tempo_envase_min"])
            },

            "mistura": {
                "previsto": float(r["mistura_prevista"]),
                "real": float(r["mistura_real"]),
                "perda": float(r["perda_mistura"]),
                "perda_pct": float(r["perda_mistura_pct"]),
                "eficiencia_pct": float(r["eficiencia_mistura_pct"])
            },

            "fracionamento": {
                "previsto": float(r["fracionamento_previsto"]),
                "real": float(r["fracionamento_real"]),
                "perda": float(r["perda_fracionamento"]),
                "perda_pct": float(r["perda_fracionamento_pct"]),
                "eficiencia_pct": float(r["eficiencia_fracionamento_pct"])
            },

            "envase": {
                "previsto": float(r["envase_previsto"]),
                "real": float(r["envase_real"]),
                "perda": float(r["perda_envase"]),
                "perda_pct": float(r["perda_envase_pct"]),
                "eficiencia_pct": float(r["eficiencia_envase_pct"])
            },

            "perdas_apontadas": float(r["perdas_apontadas"]),

            "responsavel": r["responsavel"]

        })

    return dados


from decimal import Decimal

def preparar_dados_comercial(registros):

    if not registros:
        return {
            "resumo": {},
            "oportunidades_relevantes": [],
            "clientes_relevantes": []
        }

    # Indicadores gerais já utilizados na dashboard
    primeiro = registros[0]

    resumo = {
        "total_oportunidades": primeiro.get("total_oportunidades", 0),
        "valor_pipeline": primeiro.get("valor_pipeline", 0),
        "ticket_medio": primeiro.get("ticket_medio", 0),
        "maior_oportunidade": primeiro.get("maior_oportunidade", 0),
        "menor_oportunidade": primeiro.get("menor_oportunidade", 0),

        "total_ativos": primeiro.get("total_ativos", 0),
        "total_conquistados": primeiro.get("total_conquistados", 0),
        "total_suspensos": primeiro.get("total_suspensos", 0),
        "total_cancelados": primeiro.get("total_cancelados", 0),

        "valor_conquistado": primeiro.get("valor_conquistado", 0),

        "temperatura": {
            "100": primeiro.get("temp_100", 0),
            "60": primeiro.get("temp_60", 0),
            "40": primeiro.get("temp_40", 0),
            "25": primeiro.get("temp_25", 0),
            "10": primeiro.get("temp_10", 0),
        },

        "solucoes": {
            "Full-Service": primeiro.get("total_full_service", 0),
            "Parcial-Service": primeiro.get("total_parcial_service", 0),
            "Mão de Obra": primeiro.get("total_mao_obra", 0),
            "A Definir": primeiro.get("total_a_definir", 0),
        }
    }

    # ---------------------------------------------------------
    # OPORTUNIDADES
    # Mantemos apenas informações úteis para interpretação
    # ---------------------------------------------------------

    oportunidades = []

    for r in registros:

        oportunidades.append({
            "codigo": r.get("codigo_oportunidade"),
            "cliente": r.get("cliente"),
            "origem": r.get("origem"),
            "status": r.get("status"),
            "valor": r.get("valor"),
            "temperatura": r.get("temperatura"),
            "data_inclusao": str(r.get("DataInclusao")) if r.get("DataInclusao") else None,
            "data_conclusao": r.get("DataConclusao"),
            "dias_pipeline": r.get("DiasNoPipeline"),
            "solucao": r.get("solucao"),
            "motivo": r.get("motivo"),
            "qtd_pedidos": r.get("qtd_pedidos"),
            "valor_conquistado": r.get("valor_conquistado")
        })

    # ---------------------------------------------------------
    # TOP OPORTUNIDADES
    # ---------------------------------------------------------

    oportunidades_relevantes = sorted(
        oportunidades,
        key=lambda x: (
            x["valor"] or 0,
            x["temperatura"] or 0
        ),
        reverse=True
    )[:10]

    # ---------------------------------------------------------
    # CLIENTES
    # ---------------------------------------------------------

    clientes = {}

    for r in registros:

        cliente = r.get("cliente")

        if not cliente:
            continue

        if cliente not in clientes:
            clientes[cliente] = {
                "cliente": cliente,
                "oportunidades": 0,
                "valor_total": 0,
                "maior_temperatura": 0
            }

        clientes[cliente]["oportunidades"] += 1
        clientes[cliente]["valor_total"] += r.get("valor") or 0

        temperatura = r.get("temperatura") or 0

        if temperatura > clientes[cliente]["maior_temperatura"]:
            clientes[cliente]["maior_temperatura"] = temperatura

    clientes_relevantes = sorted(
        clientes.values(),
        key=lambda x: x["valor_total"],
        reverse=True
    )[:10]

    return {
        "resumo": resumo,
        "oportunidades_relevantes": oportunidades_relevantes,
        "clientes_relevantes": clientes_relevantes
    }