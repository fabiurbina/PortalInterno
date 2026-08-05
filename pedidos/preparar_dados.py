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

    dados = []

    for r in registros:

        dados.append({

            "cliente": r["cliente"],

            "oportunidades": int(r["oportunidades_cliente"]),

            "pipeline": float(r["valor"]),

            "status": r["status"],

            "origem": r["origem"],

            "solucao": r["solucao"],

            "motivo": r["motivo"],

            "temperatura": int(r["temperatura"]),

            "ano_previsto": int(r["ano_previsto"]),

            "mes_previsto": int(r["mes_previsto"]),

            "ranking": int(r["ranking_valor"]),

            "percentual_pipeline": float(r["percentual_pipeline"])

        })

    return dados