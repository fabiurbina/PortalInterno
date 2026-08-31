/* =========================================================
   DASHBOARD COMERCIAL - VIESANO
========================================================= */

let comercialGraficos = {};


/* =========================================================
   INICIALIZAÇÃO
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        carregarDadosComercial();

    }
);


/* =========================================================
   CARREGAR DADOS
========================================================= */

async function carregarDadosComercial() {

    try {

        const response = await fetch(
            "/indicadores/comercial/dados/"
        );


        if (!response.ok) {

            throw new Error(
                `Erro HTTP ${response.status}`
            );

        }


        const dados =
            await response.json();


        atualizarDashboard(
            dados
        );


    } catch (erro) {

        console.error(
            "Erro ao carregar dashboard comercial:",
            erro
        );

    }

}


/* =========================================================
   ATUALIZAR DASHBOARD
========================================================= */

function atualizarDashboard(
    dados
) {

    atualizarKPIs(
        dados
    );


    criarGraficos(
        dados
    );


    document.getElementById(
        "comercialAtualizado"
    ).textContent =
        new Date().toLocaleString(
            "pt-BR"
        );

}


/* =========================================================
   KPIs
========================================================= */

function atualizarKPIs(
    dados
) {

    definirTexto(
        "comercialKpiTotal",
        dados.total_oportunidades || 0
    );


    definirTexto(
        "comercialKpiAtivos",
        dados.total_ativos || 0
    );


    definirTexto(
        "comercialKpiConquistadas",
        dados.total_conquistados || 0
    );


    definirTexto(
        "comercialKpiSuspensas",
        dados.total_suspensos || 0
    );


    definirTexto(
        "comercialKpiCanceladas",
        dados.total_cancelados || 0
    );


    definirTexto(
    "comercialKpiPipeline",
    formatarMoeda(
        dados.valor_pipeline || 0
    )
);

    console.log(
        "TAXA RECEBIDA:",
        dados.taxa_conversao
    );

    definirTexto(
        "comercialKpiTaxa",
        Number(
            dados.taxa_conversao || 0
        ).toLocaleString(
            "pt-BR",
            {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }
        ) + "%"
    );


/* =========================================================
   GRÁFICOS
========================================================= */

function criarGraficos(
    dados
) {

    destruirGraficos();


    criarGraficoStatus(
        dados.status || {}
    );


    criarGraficoSolucao(
        dados.solucao || {}
    );


    criarGraficoTemperatura(
        dados.temperatura || {}
    );


    criarGraficoEvolucao(
        dados.evolucao_mensal || []
    );

}


/* =========================================================
   STATUS
========================================================= */

function criarGraficoStatus(
    dados
) {

    const canvas =
        document.getElementById(
            "comercialStatus"
        );


    if (!canvas) {
        return;
    }


    comercialGraficos.status =
        new Chart(

            canvas,

            {

                type: "doughnut",

                data: {

                    labels:
                        Object.keys(dados),

                    datasets: [

                        {

                            data:
                                Object.values(dados),

                            borderWidth: 0

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

                        }

                    }

                }

            }

        );

}


/* =========================================================
   SOLUÇÃO
========================================================= */

function criarGraficoSolucao(
    dados
) {

    const canvas =
        document.getElementById(
            "comercialSolucao"
        );


    if (!canvas) {
        return;
    }


    comercialGraficos.solucao =
        new Chart(

            canvas,

            {

                type: "doughnut",

                data: {

                    labels:
                        Object.keys(dados),

                    datasets: [

                        {

                            data:
                                Object.values(dados),

                            borderWidth: 0

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

                            position: "right"

                        }

                    }

                }

            }

        );

}


/* =========================================================
   TEMPERATURA
========================================================= */

function criarGraficoTemperatura(
    dados
) {

    const canvas =
        document.getElementById(
            "comercialTemperatura"
        );


    if (!canvas) {
        return;
    }


    comercialGraficos.temperatura =
        new Chart(

            canvas,

            {

                type: "bar",

                data: {

                    labels:
                        Object.keys(dados),

                    datasets: [

                        {

                            label:
                                "Oportunidades",

                            data:
                                Object.values(dados),

                            borderWidth: 0,

                            borderRadius: 4

                        }

                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    scales: {

                        y: {

                            beginAtZero: true,

                            ticks: {

                                precision: 0

                            }

                        }

                    },

                    plugins: {

                        legend: {

                            display: false

                        }

                    }

                }

            }

        );

}


/* =========================================================
   EVOLUÇÃO DO PIPELINE
========================================================= */

function criarGraficoEvolucao(
    dados
) {

    const canvas =
        document.getElementById(
            "comercialEvolucao"
        );


    if (!canvas) {
        return;
    }


    const labels =
        dados.map(
            item => item.mes
        );


    const valores =
        dados.map(
            item =>
                Number(
                    item.pipeline || 0
                )
        );


    comercialGraficos.evolucao =
        new Chart(

            canvas,

            {

                type: "line",

                data: {

                    labels: labels,

                    datasets: [

                        {

                            label:
                                "Pipeline",

                            data:
                                valores,

                            tension: 0.35,

                            fill: false,

                            pointRadius: 4,

                            pointHoverRadius: 6,

                            borderWidth: 2

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

                            position: "bottom"

                        },

                        tooltip: {

                            callbacks: {

                                label:
                                    function (
                                        contexto
                                    ) {

                                        return (

                                            "Pipeline: " +

                                            formatarMoeda(
                                                contexto.raw
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

                                callback:
                                    function (
                                        valor
                                    ) {

                                        return formatarMoedaCompacta(
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
   DESTRUIR GRÁFICOS
========================================================= */

function destruirGraficos() {

    Object.values(
        comercialGraficos
    ).forEach(

        grafico => {

            if (grafico) {

                grafico.destroy();

            }

        }

    );


    comercialGraficos = {};

}


/* =========================================================
   UTILITÁRIOS
========================================================= */

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


function formatarMoeda(
    valor
) {

    return Number(
        valor || 0
    ).toLocaleString(
        "pt-BR",
        {

            style: "currency",

            currency: "BRL",

            maximumFractionDigits: 0

        }
    );

}


function formatarMoedaCompacta(
    valor
) {

    const numero =
        Number(valor || 0);


    if (Math.abs(numero) >= 1000000) {

        return (
            "R$ " +
            (numero / 1000000)
                .toLocaleString(
                    "pt-BR",
                    {
                        maximumFractionDigits: 1
                    }
                ) +
            " Mi"
        );

    }


    if (Math.abs(numero) >= 1000) {

        return (
            "R$ " +
            (numero / 1000)
                .toLocaleString(
                    "pt-BR",
                    {
                        maximumFractionDigits: 0
                    }
                ) +
            " Mil"
        );

    }


    return formatarMoeda(
        numero
    );

}