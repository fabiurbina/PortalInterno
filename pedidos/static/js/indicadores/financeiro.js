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

function atualizarDashboardFinanceiro(dados) {


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
   CONCENTRAÇÃO DAS DESPESAS
   TOP 5 + OUTRAS DESPESAS
========================================================= */

function criarGraficoParetoFinanceiro(dados) {

    const canvas =
        document.getElementById(
            "financeiroPareto"
        );


    if (!canvas) {
        return;
    }


    destruirGraficoFinanceiro(
        "pareto"
    );


    /* =====================================================
       ORDENA MAIOR → MENOR
    ===================================================== */

    const dadosOrdenados =
        [...dados].sort(
            (a, b) =>
                Number(b.valor || 0) -
                Number(a.valor || 0)
        );


    /* =====================================================
       TOP 5
    ===================================================== */

    const top5 =
        dadosOrdenados.slice(
            0,
            5
        );


    const restantes =
        dadosOrdenados.slice(
            5
        );


    /* =====================================================
       OUTRAS DESPESAS
    ===================================================== */

    const valorOutras =
        restantes.reduce(
            (total, item) =>
                total +
                Number(
                    item.valor || 0
                ),
            0
        );


    const categorias =
        top5.map(
            item =>
                item.categoria ||
                "Sem Categoria"
        );


    const valores =
        top5.map(
            item =>
                Number(
                    item.valor || 0
                )
        );


    if (valorOutras > 0) {

        categorias.push(
            "Outras Despesas"
        );


        valores.push(
            valorOutras
        );

    }


    /* =====================================================
       PERCENTUAL INDIVIDUAL
    ===================================================== */

    const total =
        valores.reduce(
            (soma, valor) =>
                soma + valor,
            0
        );


    const percentuais =
        valores.map(
            valor =>
                total > 0
                    ? (
                        valor /
                        total
                    ) * 100
                    : 0
        );


    /* =====================================================
       GRÁFICO HORIZONTAL
    ===================================================== */

    financeiroGraficos.pareto =
        new Chart(
            canvas,
            {

                type: "bar",

                data: {

                    labels: categorias,

                    datasets: [

                        {

                            label:
                                "Participação nas Despesas",

                            data:
                                percentuais,

                            backgroundColor:
                                "#82bde4",

                            borderWidth: 0,

                            borderRadius: 5,

                            barPercentage: 0.65,

                            categoryPercentage: 0.72

                        }

                    ]

                },


                options: {

                    indexAxis: "y",

                    responsive: true,

                    maintainAspectRatio: false,


                    layout: {

                        padding: {

                            left: 4,

                            right: 25,

                            top: 8,

                            bottom: 2

                        }

                    },


                    plugins: {

                        legend: {

                            display: false

                        },


                        datalabels: {

                            display: true,

                            anchor: "end",

                            align: "right",

                            offset: 4,

                            clamp: true,

                            color: "#18202a",

                            font: {

                                size: 10,

                                weight: "600"

                            },

                            formatter:
                                function(valor) {

                                    return (
                                        Number(valor)
                                            .toLocaleString(
                                                "pt-BR",
                                                {
                                                    minimumFractionDigits: 1,
                                                    maximumFractionDigits: 1
                                                }
                                            )
                                        +
                                        "%"
                                    );

                                }

                        },


                        tooltip: {

                            callbacks: {

                                label:
                                    function(contexto) {

                                        const indice =
                                            contexto.dataIndex;


                                        return (
                                            percentuais[
                                                indice
                                            ].toLocaleString(
                                                "pt-BR",
                                                {
                                                    minimumFractionDigits: 1,
                                                    maximumFractionDigits: 1
                                                }
                                            )
                                            +
                                            "%  |  "
                                            +
                                            formatarMoedaGerencialFinanceiro(
                                                valores[
                                                    indice
                                                ]
                                            )
                                        );

                                    }

                            }

                        }

                    },


                    scales: {

                        y: {

                            grid: {

                                display: false

                            },


                            ticks: {

                                autoSkip: false,

                                padding: 7,

                                font: {

                                    size: 10

                                }

                            }

                        },


                        x: {

                            beginAtZero: true,

                            max: 100,

                            border: {

                                display: false

                            },


                            grid: {

                                color:
                                    "rgba(100,110,120,.12)"

                            },


                            ticks: {

                                stepSize: 20,

                                font: {

                                    size: 9

                                },


                                callback:
                                    function(valor) {

                                        return (
                                            valor +
                                            "%"
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
   TOP 5 FORNECEDORES
========================================================= */

function criarGraficoTop5Financeiro(dados) {

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


    const fornecedores =
        (dados.labels || [])
            .map(
                (nome, index) => ({

                    nome: nome,

                    valor:
                        Number(
                            dados.values?.[index] ||
                            0
                        )

                })
            )
            .filter(
                item => {

                    const nome =
                        item.nome
                            .toLowerCase()
                            .trim();


                    return !nome.includes(
                        "andre machado"
                    );

                }
            )
            .sort(
                (a, b) =>
                    b.valor -
                    a.valor
            )
            .slice(
                0,
                5
            );


    financeiroGraficos.top5 =
        new Chart(
            canvas,
            {

                type: "bar",

                data: {

                    labels:
                        fornecedores.map(
                            item =>
                                item.nome
                        ),

                    datasets: [

                        {

                            label:
                                "Valor",

                            data:
                                fornecedores.map(
                                    item =>
                                        item.valor
                                ),

                            backgroundColor:
                                "#82bde4",

                            borderWidth: 0,

                            borderRadius: 4,

                            barPercentage: 0.65,

                            categoryPercentage: 0.75

                        }

                    ]

                },


                options: {

                    indexAxis: "y",

                    responsive: true,

                    maintainAspectRatio: false,


                    layout: {

                        padding: {

                            left: 0,

                            right: 20,

                            top: 5,

                            bottom: 2

                        }

                    },


                    plugins: {

                        legend: {

                            display: false

                        },


                        datalabels: {

                            display: false

                        },


                        tooltip: {

                            callbacks: {

                                label:
                                    function(contexto) {

                                        return formatarMoedaGerencialFinanceiro(
                                            contexto.raw
                                        );

                                    }

                            }

                        }

                    },


                    scales: {

                        y: {

                            grid: {

                                display: false

                            },


                            ticks: {

                                autoSkip: false,

                                padding: 6,

                                font: {

                                    size: 9

                                }

                            }

                        },


                        x: {

                            beginAtZero: true,

                            border: {

                                display: false

                            },


                            ticks: {

                                font: {

                                    size: 9

                                },


                                callback:
                                    function(valor) {

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
   SOMENTE PAGO + A VENCER
========================================================= */

function criarGraficoStatusFinanceiro(dados) {

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


    const ordemStatus = [
        "PAGO",
        "A VENCER"
    ];


    const labels = [];

    const valores = [];


    ordemStatus.forEach(
        status => {

            if (
                dados[status] !== undefined
            ) {

                labels.push(
                    status
                );


                valores.push(
                    Number(
                        dados[status] || 0
                    )
                );

            }

        }
    );


    financeiroGraficos.status =
        new Chart(
            canvas,
            {

                type: "doughnut",

                data: {

                    labels: labels,

                    datasets: [

                        {

                            data: valores,

                            borderWidth: 1

                        }

                    ]

                },


                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    cutout: "60%",


                    layout: {

                        padding: 4

                    },


                    plugins: {

                        legend: {

                            display: true,

                            position: "bottom",

                            labels: {

                                padding: 10,

                                boxWidth: 28,

                                font: {

                                    size: 9

                                }

                            }

                        },


                        datalabels: {

                            display: true,

                            color: "#18202a",

                            font: {

                                size: 10,

                                weight: "600"

                            },


                            formatter:
                                function(valor) {

                                    return formatarMoedaGerencialFinanceiro(
                                        valor
                                    );

                                }

                        },


                        tooltip: {

                            enabled: false

                        }

                    }

                }

            }
        );

}


/* =========================================================
   SLA
========================================================= */

function criarGraficoSlaFinanceiro(dados) {

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


    const labels = [
        "Dentro do Prazo",
        "Fora do Prazo"
    ];


    const valores = [

        Number(
            dados["Dentro do Prazo"] ||
            0
        ),

        Number(
            dados["Fora do Prazo"] ||
            0
        )

    ];


    financeiroGraficos.sla =
        new Chart(
            canvas,
            {

                type: "doughnut",

                data: {

                    labels: labels,

                    datasets: [

                        {

                            data: valores,

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

                            position: "bottom",

                            labels: {

                                padding: 10,

                                boxWidth: 28,

                                font: {

                                    size: 9

                                }

                            }

                        },


                        datalabels: {

                            display: true,

                            color: "#18202a",

                            font: {

                                size: 10,

                                weight: "600"

                            },


                            formatter:
                                function(valor) {

                                    return formatarMoedaGerencialFinanceiro(
                                        valor
                                    );

                                }

                        },


                        tooltip: {

                            enabled: false

                        }

                    }

                }

            }
        );

}


/* =========================================================
   EVOLUÇÃO E PROJEÇÃO
   COLUNAS
========================================================= */

function criarGraficoEvolucaoFinanceiro(
    evolucao,
    projecao
) {

    const canvas =
        document.getElementById(
            "financeiroEvolucao"
        );


    if (!canvas) {
        return;
    }


    destruirGraficoFinanceiro(
        "evolucao"
    );


    const labelsHistorico =
        evolucao.labels || [];


    const despesas =
        (evolucao.despesas || [])
            .map(
                valor =>
                    Number(valor || 0)
            );


    const pago =
        (evolucao.pago || [])
            .map(
                valor =>
                    Number(valor || 0)
            );


    const aVencer =
        (evolucao.a_vencer || [])
            .map(
                valor =>
                    Number(valor || 0)
            );


    const labelsProjecao =
        projecao.labels || [];


    const valoresProjecao =
        (projecao.valores || [])
            .map(
                valor =>
                    Number(valor || 0)
            );


    /* =====================================================
       TODOS OS MESES
    ===================================================== */

    const labels = [

        ...labelsHistorico,

        ...labelsProjecao

    ];


    /* =====================================================
       PAGAMENTOS REALIZADOS
    ===================================================== */

    const dadosPago = [

        ...pago,

        ...new Array(
            labelsProjecao.length
        ).fill(null)

    ];


    /* =====================================================
       PREVISÃO
    ===================================================== */

    const dadosPrevisao = [

        ...new Array(
            Math.max(
                labelsHistorico.length,
                0
            )
        ).fill(null),

        ...valoresProjecao

    ];


    /* =====================================================
       FORMATAÇÃO DOS MESES
    ===================================================== */

    const labelsFormatados =
        labels.map(
            label => {

                if (
                    typeof label !== "string"
                ) {

                    return label;

                }


                const partes =
                    label.split("-");


                if (
                    partes.length === 2
                ) {

                    return (
                        partes[1] +
                        "/" +
                        partes[0].slice(2)
                    );

                }


                return label;

            }
        );


    financeiroGraficos.evolucao =
        new Chart(
            canvas,
            {

                type: "bar",

                data: {

                    labels: labelsFormatados,

                    datasets: [

                        {

                            label:
                                "Pagamentos Realizados",

                            data:
                                dadosPago,

                            backgroundColor:
                                "#2196e0",

                            borderWidth: 0,

                            borderRadius: 4,

                            barPercentage: 0.55,

                            categoryPercentage: 0.75

                        },


                        {

                            label:
                                "Previsão de Pagamentos",

                            data:
                                dadosPrevisao,

                            backgroundColor:
                                "#ff7b19",

                            borderWidth: 0,

                            borderRadius: 4,

                            barPercentage: 0.55,

                            categoryPercentage: 0.75

                        }

                    ]

                },


                options: {

                    responsive: true,

                    maintainAspectRatio: false,


                    layout: {

                        padding: {

                            top: 8,

                            right: 8,

                            left: 8,

                            bottom: 2

                        }

                    },


                    interaction: {

                        mode: "index",

                        intersect: false

                    },


                    plugins: {

                        legend: {

                            display: true,

                            position: "bottom",

                            labels: {

                                padding: 12,

                                boxWidth: 14,

                                font: {

                                    size: 10

                                }

                            }

                        },


                        datalabels: {

                            display:
                                function(contexto) {

                                    return (
                                        contexto.raw !== null &&
                                        Number(
                                            contexto.raw || 0
                                        ) > 0
                                    );

                                },


                            anchor: "end",

                            align: "top",

                            offset: 2,

                            clamp: true,

                            color: "#18202a",

                            font: {

                                size: 8,

                                weight: "600"

                            },


                            formatter:
                                function(valor) {

                                    return formatarMoedaGerencialFinanceiro(
                                        valor
                                    );

                                }

                        },


                        tooltip: {

                            callbacks: {

                                label:
                                    function(contexto) {

                                        return (
                                            contexto.dataset.label
                                            +
                                            ": "
                                            +
                                            formatarMoedaGerencialFinanceiro(
                                                contexto.raw
                                            )
                                        );

                                    }

                            }

                        }

                    },


                    scales: {

                        x: {

                            grid: {

                                display: false

                            },


                            ticks: {

                                autoSkip: true,

                                maxTicksLimit: 9,

                                font: {

                                    size: 9

                                }

                            }

                        },


                        y: {

                            beginAtZero: true,

                            border: {

                                display: false

                            },


                            grid: {

                                color:
                                    "rgba(100,110,120,.12)"

                            },


                            ticks: {

                                font: {

                                    size: 9

                                },


                                callback:
                                    function(valor) {

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
   DESTRUIR GRÁFICO
========================================================= */

function destruirGraficoFinanceiro(nome) {

    if (
        financeiroGraficos[nome]
    ) {

        financeiroGraficos[nome].destroy();

        delete financeiroGraficos[nome];

    }

}


/* =========================================================
   FORMATAÇÃO — MOEDA COMPLETA
========================================================= */

function formatarMoedaFinanceiro(valor) {

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


/* =========================================================
   FORMATAÇÃO — MOEDA GERENCIAL
========================================================= */

function formatarMoedaGerencialFinanceiro(valor) {

    const numero =
        Number(
            valor || 0
        );


    const absoluto =
        Math.abs(numero);


    if (
        absoluto >= 1000000
    ) {

        return (
            "R$ " +
            (
                numero / 1000000
            ).toLocaleString(
                "pt-BR",
                {

                    maximumFractionDigits: 1

                }
            ) +
            " mi"
        );

    }


    if (
        absoluto >= 1000
    ) {

        return (
            "R$ " +
            (
                numero / 1000
            ).toLocaleString(
                "pt-BR",
                {

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


/* =========================================================
   FORMATAÇÃO — EIXO MONETÁRIO
========================================================= */

function formatarMoedaCompactaFinanceiro(valor) {

    const numero =
        Number(
            valor || 0
        );


    const absoluto =
        Math.abs(numero);


    if (
        absoluto >= 1000000
    ) {

        return (
            "R$ " +
            (
                numero / 1000000
            ).toLocaleString(
                "pt-BR",
                {

                    maximumFractionDigits: 1

                }
            ) +
            " mi"
        );

    }


    if (
        absoluto >= 1000
    ) {

        return (
            "R$ " +
            (
                numero / 1000
            ).toLocaleString(
                "pt-BR",
                {

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


/* =========================================================
   NÚMERO
========================================================= */

function formatarNumeroFinanceiro(valor) {

    return Number(
        valor || 0
    ).toLocaleString(
        "pt-BR"
    );

}


/* =========================================================
   PERCENTUAL
========================================================= */

function formatarPercentualFinanceiro(valor) {

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
    function(evento) {

        if (
            evento.target &&
            evento.target.id ===
                "financeiroAplicarFiltros"
        ) {

            carregarDadosFinanceiro();

        }

    }
);