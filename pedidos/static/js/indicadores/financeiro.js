/* =========================================================
   DASHBOARD FINANCEIRO - VIESANO
========================================================= */

let financeiroGraficos = {};


/* =========================================================
   INICIALIZAÇÃO
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        carregarDadosFinanceiro();

    }
);


/* =========================================================
   CARREGAR DADOS
========================================================= */

async function carregarDadosFinanceiro() {

    try {

        const parametros = new URLSearchParams();

        const dataVencimentoInicio =
            document.getElementById(
                "financeiroDataVencimentoInicio"
            )?.value;

        const dataVencimentoFim =
            document.getElementById(
                "financeiroDataVencimentoFim"
            )?.value;

        const dataPagamentoInicio =
            document.getElementById(
                "financeiroDataPagamentoInicio"
            )?.value;

        const dataPagamentoFim =
            document.getElementById(
                "financeiroDataPagamentoFim"
            )?.value;

        const status =
            document.getElementById(
                "financeiroStatus"
            )?.value;

        const sla =
            document.getElementById(
                "financeiroSla"
            )?.value;


        if (dataVencimentoInicio) {
            parametros.append(
                "data_vencimento_inicio",
                dataVencimentoInicio
            );
        }


        if (dataVencimentoFim) {
            parametros.append(
                "data_vencimento_fim",
                dataVencimentoFim
            );
        }


        if (dataPagamentoInicio) {
            parametros.append(
                "data_pagamento_inicio",
                dataPagamentoInicio
            );
        }


        if (dataPagamentoFim) {
            parametros.append(
                "data_pagamento_fim",
                dataPagamentoFim
            );
        }


        if (status) {
            parametros.append(
                "status",
                status
            );
        }


        if (sla) {
            parametros.append(
                "sla",
                sla
            );
        }


        let url =
            "/indicadores/financeiro/";

        const queryString =
            parametros.toString();

        if (queryString) {

            url += "?" + queryString;

        }


        const response =
            await fetch(url);


        if (!response.ok) {

            throw new Error(
                `Erro HTTP ${response.status}`
            );

        }


        const html =
            await response.text();


        const parser =
            new DOMParser();

        const documento =
            parser.parseFromString(
                html,
                "text/html"
            );


        const dados =
            extrairDadosFinanceiro(
                documento
            );


        atualizarDashboardFinanceiro(
            dados
        );


    } catch (erro) {

        console.error(
            "Erro ao carregar dashboard financeiro:",
            erro
        );

    }

}


/* =========================================================
   EXTRAIR DADOS DA VIEW
========================================================= */

function extrairDadosFinanceiro(documento) {

    return {

        total_despesas:
            obterTexto(
                documento,
                "financeiroKpiTotalDespesas"
            ),

        total_pago:
            obterTexto(
                documento,
                "financeiroKpiTotalPago"
            ),

        total_a_vencer:
            obterTexto(
                documento,
                "financeiroKpiAVencer"
            ),

        total_dentro_prazo:
            obterTexto(
                documento,
                "financeiroKpiDentroPrazo"
            ),

        total_fora_prazo:
            obterTexto(
                documento,
                "financeiroKpiForaPrazo"
            ),

        pagamentos_realizados:
            obterTexto(
                documento,
                "financeiroKpiPagamentosRealizados"
            ),

        percentual_pontualidade:
            obterTexto(
                documento,
                "financeiroKpiPontualidade"
            ),

        prazo_medio:
            obterTexto(
                documento,
                "financeiroKpiPrazoMedio"
            )

    };

}


/* =========================================================
   ATUALIZAR DASHBOARD
========================================================= */

function atualizarDashboardFinanceiro(
    dados
) {

    definirTexto(
        "financeiroKpiTotalDespesas",
        dados.total_despesas
    );


    definirTexto(
        "financeiroKpiTotalPago",
        dados.total_pago
    );


    definirTexto(
        "financeiroKpiAVencer",
        dados.total_a_vencer
    );


    definirTexto(
        "financeiroKpiDentroPrazo",
        dados.total_dentro_prazo
    );


    definirTexto(
        "financeiroKpiForaPrazo",
        dados.total_fora_prazo
    );


    definirTexto(
        "financeiroKpiPagamentosRealizados",
        dados.pagamentos_realizados
    );


    definirTexto(
        "financeiroKpiPontualidade",
        dados.percentual_pontualidade
    );


    definirTexto(
        "financeiroKpiPrazoMedio",
        dados.prazo_medio
    );


    const atualizado =
        document.getElementById(
            "financeiroAtualizado"
        );


    if (atualizado) {

        atualizado.textContent =
            new Date().toLocaleString(
                "pt-BR"
            );

    }

}


/* =========================================================
   UTILITÁRIOS
========================================================= */

function obterTexto(
    documento,
    id
) {

    const elemento =
        documento.getElementById(id);


    if (!elemento) {

        return "--";

    }


    return elemento.textContent.trim();

}


function definirTexto(
    id,
    valor
) {

    const elemento =
        document.getElementById(id);


    if (elemento) {

        elemento.textContent =
            valor;

    }

}


/* =========================================================
   FILTROS
========================================================= */

document.addEventListener(
    "click",
    function (evento) {

        if (
            evento.target &&
            evento.target.id ===
                "financeiroAplicarFiltros"
        ) {

            carregarDadosFinanceiro();

        }

    }
);