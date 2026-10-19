
def interpretar_status(etapa_venda, status_producao, cenario_fiscal):

    print(
        f"Venda='{etapa_venda}' | Produção='{status_producao}' | "
        f"Cenário='{cenario_fiscal}'"
    )

    # Proteção contra valores None
    etapa_venda = (etapa_venda or "").strip().lower()
    status_producao = (status_producao or "").strip().lower()
    cenario_fiscal = (cenario_fiscal or "").strip().lower()

    if (
        etapa_venda == "separar estoque"
        and status_producao == "programado"
    ):
        return {
            "titulo": "Preparando produção",
            "descricao": (
                "Recebemos seu pedido e já validamos que todos "
                "os materiais necessários estão disponíveis. "
                "Em breve iniciaremos a fabricação."
            ),
            "cor": "warning"
        }

    if (
        etapa_venda == "separar estoque"
        and status_producao == "produzindo"
    ):
        return {
            "titulo": "Seu pedido está em produção",
            "descricao": (
                "Nossa equipe está produzindo o seu pedido com todo "
                "o cuidado e atenção à qualidade. "
                "Assim que essa etapa for concluída, ele seguirá "
                "para faturamento e ficará disponível para retirada."
            ),
            "cor": "primary"
        }

    if (
        etapa_venda == "separar estoque"
        and status_producao == "requisição de compra"
        and cenario_fiscal == "industrialização para terceiros"
    ):
        return {
            "titulo": "Aguardando materiais",
            "descricao": (
                "Estamos aguardando a chegada dos materiais necessários "
                "para iniciar a produção."
            ),
            "cor": "danger"
        }

    if (
        etapa_venda == "separar estoque"
        and status_producao == "requisição de compra"
    ):
        return {
            "titulo": "Aguardando materiais",
            "descricao": (
                "Estamos adquirindo alguns materiais necessários "
                "para iniciar a produção."
            ),
            "cor": "danger"
        }

    if (
        etapa_venda == "separar estoque"
        and status_producao == "concluído"
    ):
        return {
            "titulo": "Produção concluída",
            "descricao": (
                "Uma das etapas de produção do seu pedido foi concluída "
                "com sucesso. Ainda existem outras ordens de produção "
                "em andamento e, assim que todas forem finalizadas, "
                "seu pedido seguirá para faturamento."
            ),
            "cor": "primary"
        }

    if (
        etapa_venda == "faturar"
        and status_producao == "concluído"
    ):
        return {
            "titulo": "Seu pedido está quase pronto!",
            "descricao": (
                "A produção foi concluída com sucesso. "
                "Agora seu pedido seguirá para faturamento e, em seguida, "
                "será preparado para envio."
            ),
            "cor": "secondary"
        }

    # NOVA CONDIÇÃO: FATURAR + ARMAZENAR/EXPEDIR
    if (
        etapa_venda == "faturar"
        and status_producao == "armazenar/expedir"
    ):
        return {
            "titulo": "Seu pedido está pronto!",
            "descricao": (
                "Seu pedido está pronto e disponível para retirada. "
                "Nossa equipe está à disposição para atendê-lo. "
                "Em caso de dúvidas sobre horário ou local de retirada, "
                "entre em contato conosco."
            ),
            "cor": "success"
        }

    if (
        etapa_venda == "faturado"
        and status_producao == "concluído"
    ):
        return {
            "titulo": "Seu pedido está pronto.",
            "descricao": (
                "Seu pedido foi faturado e já está disponível para retirada. "
                "Nossa equipe está à disposição para atendê-lo. "
                "Em caso de dúvidas sobre horário ou local de retirada, "
                "entre em contato conosco."
            ),
            "cor": "success"
        }

    if (
        etapa_venda == "faturado"
        and status_producao == "armazenar/expedir"
    ):
        return {
            "titulo": "Seu pedido está pronto!",
            "descricao": (
                "Seu pedido está pronto e disponível para retirada. "
                "Nossa equipe está à disposição para atendê-lo. "
                "Em caso de dúvidas sobre horário ou local de retirada, "
                "entre em contato conosco."
            ),
            "cor": "success"
        }

    # SEGURANÇA: registra combinações ainda não mapeadas
    print(
        f"[STATUS NÃO MAPEADO] "
        f"Venda='{etapa_venda}' | "
        f"Produção='{status_producao}' | "
        f"Cenário fiscal='{cenario_fiscal}'"
    )

    # Retorno padrão para evitar falhas na exibição do status
    return {
        "titulo": "Pedido em andamento",
        "descricao": (
            "Seu pedido continua em acompanhamento pela nossa equipe. "
            "Em caso de dúvidas, entre em contato conosco."
        ),
        "cor": "secondary"
    }
