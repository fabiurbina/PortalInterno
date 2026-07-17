def interpretar_status(etapa_venda, status_producao):

    print(
    f"Venda='{etapa_venda}' | Produção='{status_producao}'"
)
    # Evita erro caso venha None
    etapa_venda = (etapa_venda or "").strip().lower()
    status_producao = (status_producao or "").strip().lower()

    if (
        etapa_venda == "separar estoque"
        and status_producao == "programado"
    ):

        return {
            "titulo": "Programar",
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
            "titulo": "Produzindo",
            "descricao": (
                "Nossa equipe está produzindo o seu pedido com todo o cuidado e atenção à qualidade. "
                "Assim que essa etapa for concluída, ele seguirá para faturamento e ficará disponível para retirada."
            ),
            "cor": "primary"
}

    if (
        etapa_venda == "separar estoque"
        and status_producao == "requisição de compra"
    ):

        return {
            "titulo": "Requisições de Compra",
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
            "titulo": "Produção em andamento",
            "descricao": (
                "Uma das etapas de produção do seu pedido foi concluída com sucesso. "
                "Ainda existem outras ordens de produção em andamento e, assim que todas "
                "forem finalizadas, seu pedido seguirá para faturamento."
            ),
            "cor": "warning"
        }
        
        

        
    if (
        etapa_venda == "faturar"
        and status_producao == "concluído"
    ):

        return {
        "titulo": "Produção Concluída.",
        "descricao": (
            "A produção foi concluída com sucesso. "
            "Agora seu pedido seguirá para faturamento e, em seguida, será preparado para envio."
        ),
        
        "cor": "secondary"
    }
        
        
        
    if (
    etapa_venda == "faturado"
    and status_producao == "concluído"
    ):

        return {
            "titulo": "Pedido Faturado!",
            "descricao": (
                "Seu pedido foi faturado e já está disponível para retirada. "
                "Nossa equipe está à disposição para atendê-lo. "
                "Em caso de dúvidas sobre horário ou local de retirada, entre em contato conosco."
            ),
            
            "cor": "success"
        }
        
        
    if (
    etapa_venda == "faturado"
    and status_producao == "armazenar/expedir"
    ):

        return {
            "titulo": "Pedido Enviado!",
            "descricao": (
                "Seu pedido está pronto e disponível para retirada. "
                "Nossa equipe está à disposição para atendê-lo. "
                "Em caso de dúvidas sobre horário ou local de retirada, entre em contato conosco."
            ),
            
            "cor": "success"
        }

    return {
        "titulo": "Em andamento",
        "descricao": (
            f"Status não mapeado: "
            f"Venda='{etapa_venda}' | "
            f"Produção='{status_producao}'"
        ),
        
        "cor": "success"
    }
    
    