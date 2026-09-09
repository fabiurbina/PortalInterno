document.addEventListener("DOMContentLoaded", function () {

    // ==========================================================
    // DADOS VINDOS DO DJANGO
    // ==========================================================

    const dreLabels = window.financeiroData.dreLabels;
    const dreValues = window.financeiroData.dreValues;

    const categoriaLabels = window.financeiroData.categoriaLabels;
    const categoriaValues = window.financeiroData.categoriaValues;

    const statusLabels = window.financeiroData.statusLabels;
    const statusValues = window.financeiroData.statusValues;

    const slaLabels = window.financeiroData.slaLabels;
    const slaValues = window.financeiroData.slaValues;

    const evolucaoLabels = window.financeiroData.evolucaoLabels;
    const evolucaoDespesas = window.financeiroData.evolucaoDespesas;
    const evolucaoPago = window.financeiroData.evolucaoPago;


    // ==========================================================
    // FORMATAÇÃO MONETÁRIA
    // ==========================================================

    function formatarMoeda(valor) {

        return new Intl.NumberFormat(
            "pt-BR",
            {
                style: "currency",
                currency: "BRL"
            }
        ).format(valor);

    }


    // ==========================================================
    // EVOLUÇÃO FINANCEIRA
    // ==========================================================

    const elementoEvolucao =
        document.getElementById("graficoEvolucao");

    if (elementoEvolucao) {

        new Chart(
            elementoEvolucao,
            {

                type: "line",

                data: {

                    labels: evolucaoLabels,

                    datasets: [

                        {
                            label: "Despesas",
                            data: evolucaoDespesas,
                            tension: 0.3,
                            borderWidth: 2,
                            fill: false
                        },

                        {
                            label: "Pago",
                            data: evolucaoPago,
                            tension: 0.3,
                            borderWidth: 2,
                            fill: false
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

                        tooltip: {

                            callbacks: {

                                label: function (context) {

                                    return (
                                        context.dataset.label
                                        + ": "
                                        + formatarMoeda(
                                            context.raw
                                        )
                                    );

                                }

                            }

                        }

                    },

                    scales: {

                        y: {

                            ticks: {

                                callback: function (value) {

                                    return formatarMoeda(value);

                                }

                            }

                        }

                    }

                }

            }
        );

    }


    // ==========================================================
    // STATUS FINANCEIRO
    // ==========================================================

    const elementoStatus =
        document.getElementById("graficoStatus");

    if (elementoStatus) {

        new Chart(
            elementoStatus,
            {

                type: "doughnut",

                data: {

                    labels: statusLabels,

                    datasets: [

                        {
                            data: statusValues,
                            borderWidth: 0
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
                                        context.label
                                        + ": "
                                        + formatarMoeda(
                                            context.raw
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


    // ==========================================================
    // SLA
    // ==========================================================

    const elementoSLA =
        document.getElementById("graficoSLA");

    if (elementoSLA) {

        new Chart(
            elementoSLA,
            {

                type: "doughnut",

                data: {

                    labels: slaLabels,

                    datasets: [

                        {
                            data: slaValues,
                            borderWidth: 0
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
                                        context.label
                                        + ": "
                                        + formatarMoeda(
                                            context.raw
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


    // ==========================================================
    // DESPESAS POR DRE
    // ==========================================================

    const elementoDRE =
        document.getElementById("graficoDRE");

    if (elementoDRE) {

        new Chart(
            elementoDRE,
            {

                type: "bar",

                data: {

                    labels: dreLabels,

                    datasets: [

                        {
                            label: "Despesas",
                            data: dreValues,
                            borderWidth: 0
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

                            ticks: {

                                callback: function (value) {

                                    return formatarMoeda(value);

                                }

                            }

                        }

                    }

                }

            }
        );

    }


    // ==========================================================
    // DESPESAS POR CATEGORIA
    // ==========================================================

    const elementoCategoria =
        document.getElementById("graficoCategoria");

    if (elementoCategoria) {

        new Chart(
            elementoCategoria,
            {

                type: "bar",

                data: {

                    labels: categoriaLabels,

                    datasets: [

                        {
                            label: "Despesas",
                            data: categoriaValues,
                            borderWidth: 0
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

                            ticks: {

                                callback: function (value) {

                                    return formatarMoeda(value);

                                }

                            }

                        }

                    }

                }

            }
        );

    }

});