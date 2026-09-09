/* =========================================================
   DASHBOARD FINANCEIRO - VIESANO
========================================================= */

let financeiroGraficos = {};


/* =========================================================
   INICIALIZAÇÃO
========================================================= */

function inicializarDashboardFinanceiro() {

    if (!document.getElementById("financeiroDre")) {
        return;
    }

    carregarDadosFinanceiro();
}


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
            "/indicadores/financeiro/dados/";

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


        const dados =
            await response.json();


        atualizarDashboardFinanceiro(dados);


    } catch (erro) {

        console.error(
            "Erro ao carregar dashboard financeiro:",
            erro
        );

    }

}


/* =========================================================
   ATUALIZAR DASHBOARD
========================================================= */

function atualizarDashboardFinanceiro(dados) {


    /* =====================================================
       KPIs
    ===================================================== */

    definirTexto(
        "financeiroKpiTotalDespesas",
        formatarMoeda(dados.total_despesas)
    );

    definirTexto(
        "financeiroKpiTotalPago",
        formatarMoeda(dados.total_pago)
    );

    definirTexto(
        "financeiroKpiAVencer",
        formatarMoeda(dados.total_a_vencer)
    );

    definirTexto(
        "financeiroKpiDentroPrazo",
        formatarMoeda(dados.total_dentro_prazo)
    );

    definirTexto(
        "financeiroKpiForaPrazo",
        formatarMoeda(dados.total_fora_prazo)
    );

    definirTexto(
        "financeiroKpiPagamentosRealizados",
        formatarNumero(dados.pagamentos_realizados)
    );

    definirTexto(
        "financeiroKpiPontualidade",
        formatarPercentual(dados.percentual_pontualidade)
    );

    definirTexto(
        "financeiroKpiPrazoMedio",
        "—"
    );


    /* =====================================================
       DATA DE ATUALIZAÇÃO
    ===================================================== */

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


    /* =====================================================
       GRÁFICOS
    ===================================================== */

    criarGraficoDre(dados);

    criarGraficoCategoria(dados);

    criarGraficoStatus(dados);

    criarGraficoSla(dados);

    criarGraficoEvolucao(dados);

}


/* =========================================================
   GRÁFICO - DRE
========================================================= */

function criarGraficoDre(dados) {

    const canvas =
        document.getElementById(
            "financeiroDre"
        );

    if (!canvas) {
        return;
    }

    destruirGrafico("dre");


    financeiroGraficos.dre =
        new Chart(canvas, {

            type: "bar",

            data: {

                labels:
                    Object.keys(
                        dados.despesas_dre || {}
                    ),

                datasets: [

                    {

                        label: "Despesas",

                        data:
                            Object.values(
                                dados.despesas_dre || {}
                            ),

                        borderWidth: 1

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {
                        display: false
                    },

                    tooltip: {

                        callbacks: {

                            label: function (context) {

                                return formatarMoeda(
                                    context.raw
                                );

                            }

                        }

                    }

                },

                scales: {

                    y: {

                        beginAtZero: true,

                        ticks: {

                            callback: function (value) {

                                return formatarMoeda(
                                    value
                                );

                            }

                        }

                    }

                }

            }

        });

}


/* =========================================================
   GRÁFICO - CATEGORIA
========================================================= */

function criarGraficoCategoria(dados) {

    const canvas =
        document.getElementById(
            "financeiroCategoria"
        );

    if (!canvas) {
        return;
    }

    destruirGrafico("categoria");


    financeiroGraficos.categoria =
        new Chart(canvas, {

            type: "bar",

            data: {

                labels:
                    Object.keys(
                        dados.despesas_categoria || {}
                    ),

                datasets: [

                    {

                        label: "Despesas",

                        data:
                            Object.values(
                                dados.despesas_categoria || {}
                            ),

                        borderWidth: 1

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                indexAxis: "y",

                plugins: {

                    legend: {
                        display: false
                    },

                    tooltip: {

                        callbacks: {

                            label: function (context) {

                                return formatarMoeda(
                                    context.raw
                                );

                            }

                        }

                    }

                },

                scales: {

                    x: {

                        beginAtZero: true,

                        ticks: {

                            callback: function (value) {

                                return formatarMoeda(
                                    value
                                );

                            }

                        }

                    }

                }

            }

        });

}


/* =========================================================
   GRÁFICO - STATUS
========================================================= */

function criarGraficoStatus(dados) {

    const canvas =
        document.getElementById(
            "financeiroGraficoStatus"
        );

    if (!canvas) {
        return;
    }

    destruirGrafico("status");


    financeiroGraficos.status =
        new Chart(canvas, {

            type: "doughnut",

            data: {

                labels:
                    Object.keys(
                        dados.status || {}
                    ),

                datasets: [

                    {

                        data:
                            Object.values(
                                dados.status || {}
                            ),

                        borderWidth: 1

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {
                        position: "bottom"
                    },

                    tooltip: {

                        callbacks: {

                            label: function (context) {

                                return (
                                    context.label +
                                    ": " +
                                    formatarMoeda(
                                        context.raw
                                    )
                                );

                            }

                        }

                    }

                }

            }

        });

}


/* =========================================================
   GRÁFICO - SLA
========================================================= */

function criarGraficoSla(dados) {

    const canvas =
        document.getElementById(
            "financeiroSla"
        );

    if (!canvas) {
        return;
    }

    destruirGrafico("sla");


    financeiroGraficos.sla =
        new Chart(canvas, {

            type: "doughnut",

            data: {

                labels:
                    Object.keys(
                        dados.sla || {}
                    ),

                datasets: [

                    {

                        data:
                            Object.values(
                                dados.sla || {}
                            ),

                        borderWidth: 1

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {
                        position: "bottom"
                    },

                    tooltip: {

                        callbacks: {

                            label: function (context) {

                                return (
                                    context.label +
                                    ": " +
                                    formatarMoeda(
                                        context.raw
                                    )
                                );

                            }

                        }

                    }

                }

            }

        });

}


/* =========================================================
   GRÁFICO - EVOLUÇÃO
========================================================= */

function criarGraficoEvolucao(dados) {

    const canvas =
        document.getElementById(
            "financeiroEvolucao"
        );

    if (!canvas) {
        return;
    }

    destruirGrafico("evolucao");


    financeiroGraficos.evolucao =
        new Chart(canvas, {

            type: "line",

            data: {

                labels:
                    dados.evolucao?.labels || [],

                datasets: [

                    {

                        label: "Despesas",

                        data:
                            dados.evolucao?.despesas || [],

                        borderWidth: 2,

                        tension: 0.3

                    },

                    {

                        label: "Pago",

                        data:
                            dados.evolucao?.pago || [],

                        borderWidth: 2,

                        tension: 0.3

                    }

                ]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    tooltip: {

                        callbacks: {

                            label: function (context) {

                                return (
                                    context.dataset.label +
                                    ": " +
                                    formatarMoeda(
                                        context.raw
                                    )
                                );

                            }

                        }

                    }

                },

                scales: {

                    y: {

                        beginAtZero: true,

                        ticks: {

                            callback: function (value) {

                                return formatarMoeda(
                                    value
                                );

                            }

                        }

                    }

                }

            }

        });

}


/* =========================================================
   DESTRUIR GRÁFICO
========================================================= */

function destruirGrafico(nome) {

    if (
        financeiroGraficos[nome]
    ) {

        financeiroGraficos[nome].destroy();

        delete financeiroGraficos[nome];

    }

}


/* =========================================================
   FORMATAÇÃO
========================================================= */

function formatarMoeda(valor) {

    return Number(
        valor || 0
    ).toLocaleString(
        "pt-BR",
        {
            style: "currency",
            currency: "BRL"
        }
    );

}


function formatarNumero(valor) {

    return Number(
        valor || 0
    ).toLocaleString(
        "pt-BR"
    );

}


function formatarPercentual(valor) {

    return Number(
        valor || 0
    ).toLocaleString(
        "pt-BR",
        {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }
    ) + "%";

}


/* =========================================================
   TEXTO
========================================================= */

function definirTexto(id, valor) {

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