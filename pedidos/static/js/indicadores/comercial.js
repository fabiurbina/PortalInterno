/* =========================================================
   DASHBOARD COMERCIAL - VIESANO
========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    console.log("Dashboard Comercial: JS carregado.");

    if (typeof Chart === "undefined") {

        console.error("Chart.js não foi carregado.");

        return;
    }

    console.log("Dashboard Comercial: Chart.js carregado.");


    /* =====================================================
       CONFIGURAÇÕES GERAIS
    ===================================================== */

    const baseOptions = {

        responsive: true,

        maintainAspectRatio: false,

        animation: {
            duration: 700
        },

        plugins: {

            legend: {
                display: false
            },

            tooltip: {

                backgroundColor: "rgba(7, 24, 39, 0.95)",

                titleColor: "#ffffff",

                bodyColor: "#ffffff",

                padding: 10,

                cornerRadius: 6
            }
        }
    };


    const gridOptions = {

        color: "rgba(40, 50, 60, 0.12)",

        drawBorder: false
    };


    /* =====================================================
       1. PIPELINE POR ETAPA
    ===================================================== */

    const pipelineCanvas =
        document.getElementById("comercialPipeline");


    if (pipelineCanvas) {

        new Chart(

            pipelineCanvas,

            {

                type: "bar",

                data: {

                    labels: [

                        "01 Prospect",

                        "02 Des.PeD",

                        "05 Negociação",

                        "06 Conclusão"

                    ],

                    datasets: [

                        {

                            data: [

                                8,

                                13,

                                4,

                                7

                            ],

                            borderWidth: 0,

                            borderRadius: 3

                        }

                    ]
                },


                options: {

                    ...baseOptions,

                    indexAxis: "y",

                    scales: {

                        x: {

                            beginAtZero: true,

                            grid: gridOptions,

                            ticks: {

                                precision: 0
                            }
                        },

                        y: {

                            grid: {

                                display: false
                            }
                        }
                    }
                }
            }
        );

    }


    /* =====================================================
       2. TEMPERATURA
    ===================================================== */

    const temperaturaCanvas =
        document.getElementById("comercialTemperatura");


    if (temperaturaCanvas) {

        new Chart(

            temperaturaCanvas,

            {

                type: "bar",

                data: {

                    labels: [

                        "10",

                        "25",

                        "40",

                        "60",

                        "100"

                    ],

                    datasets: [

                        {

                            data: [

                                8,

                                3,

                                9,

                                7,

                                5

                            ],

                            borderWidth: 0,

                            borderRadius: 3

                        }

                    ]
                },


                options: {

                    ...baseOptions,

                    indexAxis: "y",

                    scales: {

                        x: {

                            beginAtZero: true,

                            grid: gridOptions,

                            ticks: {

                                precision: 0
                            }
                        },

                        y: {

                            grid: {

                                display: false
                            }
                        }
                    }
                }
            }
        );

    }


    /* =====================================================
       3. SOLUÇÃO
    ===================================================== */

    const solucaoCanvas =
        document.getElementById("comercialSolucao");


    if (solucaoCanvas) {

        new Chart(

            solucaoCanvas,

            {

                type: "doughnut",

                data: {

                    labels: [

                        "A definir",

                        "Mão de Obra",

                        "Parcial Service",

                        "Full-Service"

                    ],

                    datasets: [

                        {

                            data: [

                                15,

                                7,

                                6,

                                4

                            ],

                            borderWidth: 0

                        }

                    ]
                },


                options: {

                    ...baseOptions,

                    cutout: "62%",

                    plugins: {

                        legend: {

                            display: true,

                            position: "right",

                            labels: {

                                boxWidth: 10,

                                padding: 10,

                                font: {

                                    size: 10
                                }
                            }
                        }
                    }
                }
            }
        );

    }


    /* =====================================================
       4. STATUS
    ===================================================== */

    const statusCanvas =
        document.getElementById("comercialStatus");


    if (statusCanvas) {

        new Chart(

            statusCanvas,

            {

                type: "doughnut",

                data: {

                    labels: [

                        "Em Aberto",

                        "Concluído"

                    ],

                    datasets: [

                        {

                            data: [

                                28,

                                3

                            ],

                            borderWidth: 0

                        }

                    ]
                },


                options: {

                    ...baseOptions,

                    cutout: "62%",

                    plugins: {

                        legend: {

                            display: true,

                            position: "bottom",

                            labels: {

                                boxWidth: 10,

                                padding: 10,

                                font: {

                                    size: 10
                                }
                            }
                        }
                    }
                }
            }
        );

    }


    /* =====================================================
       5. OPORTUNIDADES EM ABERTO POR LEAD
    ===================================================== */

    const leadsCanvas =
        document.getElementById("comercialLeads");


    if (leadsCanvas) {

        new Chart(

            leadsCanvas,

            {

                type: "bar",

                data: {

                    labels: [

                        "EON ZLIFE INDUSTRIA E COMERCIO DE...",

                        "EXO NUTRITION LTDA",

                        "FITSTAR 3 SUPLEMENTOS NUTRICION...",

                        "RELAXMEDIC IMPORTAÇÃO E EXPORTA...",

                        "M.LABS COM. DISTRIB. E INDUST. DE..."

                    ],

                    datasets: [

                        {

                            data: [

                                100000,

                                94000,

                                50000,

                                50000,

                                41250

                            ],

                            borderWidth: 0,

                            borderRadius: 3

                        }

                    ]
                },


                options: {

                    ...baseOptions,

                    indexAxis: "y",

                    scales: {

                        x: {

                            beginAtZero: true,

                            grid: gridOptions,

                            ticks: {

                                callback: function (value) {

                                    return (

                                        "R$ " +

                                        Number(value)
                                            .toLocaleString(
                                                "pt-BR"
                                            )

                                    );

                                }
                            }
                        },

                        y: {

                            grid: {

                                display: false
                            }
                        }
                    }
                }
            }
        );

    }


    /* =====================================================
       6. DESFECHO
    ===================================================== */

    const desfechoCanvas =
        document.getElementById("comercialDesfecho");


    if (desfechoCanvas) {

        new Chart(

            desfechoCanvas,

            {

                type: "bar",

                data: {

                    labels: [

                        "Conquistado",

                        "Suspenso"

                    ],

                    datasets: [

                        {

                            data: [

                                2,

                                1

                            ],

                            borderWidth: 0,

                            borderRadius: 3

                        }

                    ]
                },


                options: {

                    ...baseOptions,

                    scales: {

                        y: {

                            beginAtZero: true,

                            grid: gridOptions,

                            ticks: {

                                precision: 0
                            }
                        },

                        x: {

                            grid: {

                                display: false
                            }
                        }
                    }
                }
            }
        );

    }


    /* =====================================================
       7. EVOLUÇÃO DO PIPELINE
    ===================================================== */

    const evolucaoCanvas =
        document.getElementById("comercialEvolucao");


    if (evolucaoCanvas) {

        new Chart(

            evolucaoCanvas,

            {

                type: "line",

                data: {

                    labels: [

                        "jun/2026",

                        "jul/2026",

                        "ago/2026"

                    ],

                    datasets: [

                        {

                            data: [

                                180000,

                                240000,

                                251000

                            ],

                            tension: 0.35,

                            fill: true,

                            pointRadius: 4,

                            pointHoverRadius: 6,

                            borderWidth: 2

                        }

                    ]
                },


                options: {

                    ...baseOptions,

                    scales: {

                        y: {

                            beginAtZero: true,

                            grid: gridOptions,

                            ticks: {

                                callback: function (value) {

                                    return (

                                        "R$ " +

                                        (
                                            value / 1000
                                        ).toLocaleString(
                                            "pt-BR"
                                        ) +

                                        " Mil"

                                    );

                                }
                            }
                        },

                        x: {

                            grid: {

                                display: false
                            }
                        }
                    }
                }
            }
        );

    }


    console.log(
        "Dashboard Comercial: gráficos inicializados."
    );

});


/* =========================================================
   FILTRO COMERCIAL
========================================================= */

function aplicarFiltroComercial() {

    const dataInicio =
        document.getElementById(
            "comercialDataInicio"
        )?.value;


    const dataFim =
        document.getElementById(
            "comercialDataFim"
        )?.value;


    console.log(
        "Filtro comercial:",
        dataInicio,
        "até",
        dataFim
    );


    /*
     * PRÓXIMA ETAPA
     *
     * Aqui vamos conectar os filtros
     * com o Django.
     *
     * O Django irá consultar a
     * vw_ia_comercial.
     */
}