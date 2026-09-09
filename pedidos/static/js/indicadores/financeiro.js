/* =========================================================
   DASHBOARD FINANCEIRO - VIESANO
========================================================= */

let financeiroGraficos = {};


/* =========================================================
   INICIALIZAÇÃO
========================================================= */

function inicializarDashboardFinanceiro() {

    if (!document.getElementById("financeiroPareto")) {
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

        const vencimentoInicio =
            document.getElementById(
                "financeiroDataVencimentoInicio"
            )?.value;

        const vencimentoFim =
            document.getElementById(
                "financeiroDataVencimentoFim"
            )?.value;

        const pagamentoInicio =
            document.getElementById(
                "financeiroDataPagamentoInicio"
            )?.value;

        const pagamentoFim =
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


        if (vencimentoInicio) {
            parametros.append(
                "data_vencimento_inicio",
                vencimentoInicio
            );
        }

        if (vencimentoFim) {
            parametros.append(
                "data_vencimento_fim",
                vencimentoFim
            );
        }

        if (pagamentoInicio) {
            parametros.append(
                "data_pagamento_inicio",
                pagamentoInicio
            );
        }

        if (pagamentoFim) {
            parametros.append(
                "data_pagamento_fim",
                pagamentoFim
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
   ATUALIZAR DASHBOARD
========================================================= */

function atualizarDashboardFinanceiro(
    dados
) {

    /* =====================================================
       KPIs
    ===================================================== */

    definirTextoFinanceiro(
        "financeiroKpiTotalDespesas",
        formatarMoedaFinanceiro(
            dados.total_despesas
        )
    );

    definirTextoFinanceiro(
        "financeiroKpiTotalPago",
        formatarMoedaFinanceiro(
            dados.total_pago
        )
    );

    definirTextoFinanceiro(
        "financeiroKpiAVencer",
        formatarMoedaFinanceiro(
            dados.total_a_vencer
        )
    );

    definirTextoFinanceiro(
        "financeiroKpiDentroPrazo",
        formatarMoedaFinanceiro(
            dados.total_dentro_prazo
        )
    );

    definirTextoFinanceiro(
        "financeiroKpiForaPrazo",
        formatarMoedaFinanceiro(
            dados.total_fora_prazo
        )
    );

    definirTextoFinanceiro(
        "financeiroKpiPagamentosRealizados",
        formatarNumeroFinanceiro(
            dados.pagamentos_realizados
        )
    );

    definirTextoFinanceiro(
        "financeiroKpiPontualidade",
        formatarPercentualFinanceiro(
            dados.percentual_pontualidade
        )
    );


    /* =====================================================
       DATA ATUALIZAÇÃO
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

    criarGraficoParetoFinanceiro(
        dados.pareto || []
    );

    criarGraficoTop5Financeiro(
        dados.top5_fornecedores || {}
    );

    criarGraficoStatusFinanceiro(
        dados.status || {}
    );

    criarGraficoSlaFinanceiro(
        dados.sla || {}
    );

    criarGraficoEvolucaoFinanceiro(
        dados.evolucao || {},
        dados.projecao || {}
    );

}


/* =========================================================
   CURVA 80/20
========================================================= */

function criarGraficoParetoFinanceiro(dados) {

    const canvas = document.getElementById(
        "financeiroPareto"
    );

    if (!canvas) {
        return;
    }

    destruirGraficoFinanceiro("pareto");


    // =====================================================
    // ORDENA DO MAIOR PARA O MENOR
    // =====================================================

    const dadosOrdenados = [...dados]
        .sort(
            (a, b) =>
                Number(b.valor || 0) -
                Number(a.valor || 0)
        );


    // =====================================================
    // MOSTRA SOMENTE AS 8 PRINCIPAIS CATEGORIAS
    // =====================================================

    const principais = dadosOrdenados.slice(0, 8);


    const labels = principais.map(
        item => item.categoria || "Sem Categoria"
    );


    const valores = principais.map(
        item => Number(item.valor || 0)
    );


    const acumulado = principais.map(
        item => Number(item.acumulado || 0)
    );


    financeiroGraficos.pareto = new Chart(canvas, {

        type: "bar",

        data: {

            labels: labels,

            datasets: [

                {

                    label: "Despesas",

                    data: valores,

                    borderWidth: 0,

                    borderRadius: 5,

                    barPercentage: 0.65,

                    categoryPercentage: 0.75,

                    yAxisID: "y"

                },

                {

                    type: "line",

                    label: "% Acumulado",

                    data: acumulado,

                    borderWidth: 2,

                    tension: 0.25,

                    pointRadius: 3,

                    pointHoverRadius: 5,

                    yAxisID: "yPercent"

                }

            ]

        },


        options: {

            responsive: true,

            maintainAspectRatio: false,


            interaction: {

                mode: "index",

                intersect: false

            },


            plugins: {

                legend: {

                    display: true,

                    position: "bottom",

                    labels: {

                        usePointStyle: true,

                        padding: 12

                    }

                },


                // NÃO MOSTRA NÚMEROS SOBRE AS BARRAS

                datalabels: {

                    display: false

                },


                tooltip: {

                    callbacks: {

                        label: function(contexto) {

                            if (
                                contexto.dataset
                                    .yAxisID === "yPercent"
                            ) {

                                return (
                                    "% Acumulado: " +
                                    Number(
                                        contexto.raw || 0
                                    ).toLocaleString(
                                        "pt-BR",
                                        {
                                            minimumFractionDigits: 1,
                                            maximumFractionDigits: 1
                                        }
                                    ) +
                                    "%"
                                );

                            }


                            return (
                                "Despesa: " +
                                formatarMoedaFinanceiro(
                                    contexto.raw
                                )
                            );

                        }

                    }

                }

            },


            scales: {

                x: {

                    ticks: {

                        autoSkip: false,

                        maxRotation: 35,

                        minRotation: 35,

                        font: {

                            size: 9

                        }

                    }

                },


                y: {

                    beginAtZero: true,

                    ticks: {

                        callback: function(valor) {

                            return formatarMoedaGerencialFinanceiro(
                                valor
                            );

                        }

                    }

                },


                yPercent: {

                    beginAtZero: true,

                    max: 100,

                    position: "right",

                    grid: {

                        drawOnChartArea: false

                    },

                    ticks: {

                        callback: function(valor) {

                            return valor + "%";

                        }

                    }

                }

            }

        }

    });

}


/* =========================================================
   TOP 5 FORNECEDORES
========================================================= */

function criarGraficoTop5Financeiro(
    dados
) {

    const canvas =
        document.getElementById(
            "financeiroTop5Fornecedores"
        );

    if (!canvas) {
        return;
    }

    destruirGraficoFinanceiro(
        "top5"
    );


    financeiroGraficos.top5 =
        new Chart(
            canvas,
            {

                type: "bar",

                data: {

                    labels:
                        dados.labels || [],

                    datasets: [

                        {

                            label:
                                "Valor",

                            data:
                                dados.values || [],

                            borderWidth: 0,

                            borderRadius: 4

                        }

                    ]

                },


                options: {

                    indexAxis: "y",

                    responsive: true,

                    maintainAspectRatio: false,


                    plugins: {

                        legend: {

                            display: false

                        },


                        tooltip: {

                            callbacks: {

                                label:
                                    function (
                                        contexto
                                    ) {

                                        return formatarMoedaFinanceiro(
                                            contexto.raw
                                        );

                                    }

                            }

                        }

                    },


                    scales: {

                        x: {

                            beginAtZero: true,

                            ticks: {

                                callback:
                                    function (
                                        valor
                                    ) {

                                        return formatarMoedaCompactaFinanceiro(
                                            valor
                                        );

                                    }

                            }

                        }

                    }

                }

            }
        );

}


/* =========================================================
   SITUAÇÃO FINANCEIRA
========================================================= */

function criarGraficoStatusFinanceiro(
    dados
) {

    const canvas =
        document.getElementById(
            "financeiroGraficoStatus"
        );

    if (!canvas) {
        return;
    }

    destruirGraficoFinanceiro(
        "status"
    );


    financeiroGraficos.status =
        new Chart(
            canvas,
            {

                type: "doughnut",

                data: {

                    labels:
                        Object.keys(
                            dados
                        ),

                    datasets: [

                        {

                            data:
                                Object.values(
                                    dados
                                ),

                            borderWidth: 1

                        }

                    ]

                },


                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    cutout: "60%",


                    plugins: {

                        legend: {

                            display: true,

                            position: "bottom"

                        },


                        tooltip: {

                            callbacks: {

                                label:
                                    function (
                                        contexto
                                    ) {

                                        return (
                                            contexto.label
                                            +
                                            ": "
                                            +
                                            formatarMoedaFinanceiro(
                                                contexto.raw
                                            )
                                        );

                                    }

                            }

                        }

                    }

                }

            }
        );

}


/* =========================================================
   SLA
========================================================= */

function criarGraficoSlaFinanceiro(
    dados
) {

    const canvas =
        document.getElementById(
            "financeiroSla"
        );

    if (!canvas) {
        return;
    }

    destruirGraficoFinanceiro(
        "sla"
    );


    financeiroGraficos.sla =
        new Chart(
            canvas,
            {

                type: "doughnut",

                data: {

                    labels:
                        Object.keys(
                            dados
                        ),

                    datasets: [

                        {

                            data:
                                Object.values(
                                    dados
                                ),

                            borderWidth: 1

                        }

                    ]

                },


                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    cutout: "60%",


                    plugins: {

                        legend: {

                            display: true,

                            position: "bottom"

                        },


                        tooltip: {

                            callbacks: {

                                label:
                                    function (
                                        contexto
                                    ) {

                                        return (
                                            contexto.label
                                            +
                                            ": "
                                            +
                                            formatarMoedaFinanceiro(
                                                contexto.raw
                                            )
                                        );

                                    }

                            }

                        }

                    }

                }

            }
        );

}


/* =========================================================
   EVOLUÇÃO + PROJEÇÃO
========================================================= */

function criarGraficoEvolucaoFinanceiro(evolucao, projecao) {

    const canvas = document.getElementById(
        "financeiroEvolucao"
    );

    if (!canvas) {
        return;
    }

    destruirGraficoFinanceiro("evolucao");


    const labels = evolucao.labels || [];

    const pago = (evolucao.pago || []).map(
        valor => Number(valor || 0)
    );

    const previsao = (
        evolucao.previsao ||
        evolucao.a_vencer ||
        []
    ).map(
        valor => Number(valor || 0)
    );


    /*
    =========================================================
    AJUSTA TAMANHO DAS SÉRIES
    =========================================================
    */

    const tamanho = labels.length;

    const dadosPago = [
        ...pago,
        ...new Array(
            Math.max(tamanho - pago.length, 0)
        ).fill(null)
    ].slice(0, tamanho);


    const dadosPrevisao = [
        ...previsao,
        ...new Array(
            Math.max(tamanho - previsao.length, 0)
        ).fill(null)
    ].slice(0, tamanho);


    /*
    =========================================================
    GRÁFICO
    =========================================================
    */

    financeiroGraficos.evolucao = new Chart(canvas, {

        type: "bar",

        data: {

            labels: labels,

            datasets: [

                {
                    label: "Pagamentos Realizados",

                    data: dadosPago,

                    borderWidth: 0,

                    borderRadius: 5,

                    barPercentage: 0.72,

                    categoryPercentage: 0.72,

                    backgroundColor: "#1687e8"
                },

                {
                    label: "Previsão de Pagamentos",

                    data: dadosPrevisao,

                    borderWidth: 0,

                    borderRadius: 5,

                    barPercentage: 0.72,

                    categoryPercentage: 0.72,

                    backgroundColor: "#ff7a1a"
                }

            ]

        },


        options: {

            responsive: true,

            maintainAspectRatio: false,


            interaction: {

                mode: "index",

                intersect: false

            },


            plugins: {

                legend: {

                    display: true,

                    position: "bottom",

                    labels: {

                        usePointStyle: true,

                        padding: 15

                    }

                },


                /*
                =================================================
                VALORES ARREDONDADOS NAS COLUNAS
                =================================================
                */

                datalabels: {

                    display: function(context) {

                        return Number(
                            context.dataset.data[
                                context.dataIndex
                            ] || 0
                        ) > 0;

                    },

                    anchor: "end",

                    align: "top",

                    offset: 3,

                    clamp: true,

                    font: {

                        size: 10,

                        weight: "600"

                    },

                    formatter: function(valor) {

                        return formatarMoedaGerencialFinanceiro(
                            valor
                        );

                    }

                },


                tooltip: {

                    callbacks: {

                        label: function(contexto) {

                            return (
                                contexto.dataset.label +
                                ": " +
                                formatarMoedaFinanceiro(
                                    contexto.raw
                                )
                            );

                        }

                    }

                }

            },


            scales: {

                x: {

                    stacked: false,

                    ticks: {

                        autoSkip: true,

                        maxTicksLimit: 12,

                        maxRotation: 35,

                        minRotation: 0

                    }

                },


                y: {

                    beginAtZero: true,

                    ticks: {

                        callback: function(valor) {

                            return formatarMoedaGerencialFinanceiro(
                                valor
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

function destruirGraficoFinanceiro(
    nome
) {

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

function formatarMoedaGerencialFinanceiro(valor) {

    const numero = Number(valor || 0);

    const absoluto = Math.abs(numero);


    if (absoluto >= 1000000) {

        return (
            "R$ " +
            (numero / 1000000).toLocaleString(
                "pt-BR",
                {
                    minimumFractionDigits: 1,
                    maximumFractionDigits: 1
                }
            ) +
            " mi"
        );

    }


    if (absoluto >= 1000) {

        return (
            "R$ " +
            (numero / 1000).toLocaleString(
                "pt-BR",
                {
                    minimumFractionDigits: 0,
                    maximumFractionDigits: 0
                }
            ) +
            " mil"
        );

    }


    return (
        "R$ " +
        numero.toLocaleString(
            "pt-BR",
            {
                maximumFractionDigits: 0
            }
        )
    );

}

function formatarMoedaFinanceiro(
    valor
) {

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


function formatarMoedaCompactaFinanceiro(
    valor
) {

    const numero =
        Number(
            valor || 0
        );

    if (
        Math.abs(numero) >= 1000000
    ) {

        return (
            "R$ "
            +
            (numero / 1000000)
                .toLocaleString(
                    "pt-BR",
                    {
                        maximumFractionDigits: 1
                    }
                )
            +
            " mi"
        );

    }

    if (
        Math.abs(numero) >= 1000
    ) {

        return (
            "R$ "
            +
            (numero / 1000)
                .toLocaleString(
                    "pt-BR",
                    {
                        maximumFractionDigits: 1
                    }
                )
            +
            " mil"
        );

    }

    return formatarMoedaFinanceiro(
        numero
    );

}


function formatarNumeroFinanceiro(
    valor
) {

    return Number(
        valor || 0
    ).toLocaleString(
        "pt-BR"
    );

}


function formatarPercentualFinanceiro(
    valor
) {

    return (
        Number(
            valor || 0
        ).toLocaleString(
            "pt-BR",
            {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }
        )
        +
        "%"
    );

}


/* =========================================================
   TEXTO
========================================================= */

function definirTextoFinanceiro(
    id,
    valor
) {

    const elemento =
        document.getElementById(
            id
        );

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