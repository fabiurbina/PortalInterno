// ============================================================
// DADOS
// ============================================================

const elementoDados = document.getElementById("dados-pedidos");

let dadosOriginais = [];

if (elementoDados) {
    try {
        dadosOriginais = JSON.parse(elementoDados.textContent);
    } catch (erro) {
        console.error("Erro ao carregar dados dos pedidos:", erro);
        dadosOriginais = [];
    }
}

let dadosFiltrados = [...dadosOriginais];

let pedidosChart = null;
let faturamentoChart = null;


// ============================================================
// FUNÇÕES AUXILIARES
// ============================================================

function valorCampo(obj, ...nomes) {

    for (const nome of nomes) {

        if (
            obj[nome] !== undefined &&
            obj[nome] !== null
        ) {
            return obj[nome];
        }
    }

    return null;
}


// ------------------------------------------------------------
// CONVERTE PARA NÚMERO
// ------------------------------------------------------------

function numero(valor) {

    if (
        valor === null ||
        valor === undefined ||
        valor === ""
    ) {
        return 0;
    }

    if (typeof valor === "number") {
        return Number.isFinite(valor) ? valor : 0;
    }

    let texto = String(valor).trim();

    // Trata valores brasileiros: 1.234,56
    if (
        texto.includes(".") &&
        texto.includes(",")
    ) {
        texto = texto
            .replace(/\./g, "")
            .replace(",", ".");
    }
    else if (texto.includes(",")) {
        texto = texto.replace(",", ".");
    }

    const resultado = Number(texto);

    return Number.isFinite(resultado)
        ? resultado
        : 0;
}


// ------------------------------------------------------------
// VERIFICA SE É "SIM"
// ------------------------------------------------------------

function ehSim(valor) {

    if (
        valor === null ||
        valor === undefined
    ) {
        return false;
    }

    const texto = String(valor)
        .trim()
        .toUpperCase();

    return (
        texto === "S" ||
        texto === "SIM" ||
        texto === "1" ||
        texto === "TRUE"
    );
}


// ------------------------------------------------------------
// FORMATA MOEDA
// ------------------------------------------------------------

function formatarMoeda(valor) {

    return new Intl.NumberFormat(
        "pt-BR",
        {
            style: "currency",
            currency: "BRL"
        }
    ).format(numero(valor));
}


// ------------------------------------------------------------
// FORMATA NÚMERO
// ------------------------------------------------------------

function formatarNumero(valor) {

    return new Intl.NumberFormat(
        "pt-BR"
    ).format(numero(valor));
}


// ------------------------------------------------------------
// CONVERTE DATA PARA OBJETO DATE
// ------------------------------------------------------------

function dataValida(valor) {

    if (!valor) {
        return null;
    }

    // Caso venha YYYY-MM-DD
    if (
        typeof valor === "string" &&
        /^\d{4}-\d{2}-\d{2}$/.test(valor)
    ) {

        const partes = valor.split("-");

        return new Date(
            Number(partes[0]),
            Number(partes[1]) - 1,
            Number(partes[2])
        );
    }


    // Caso venha DD/MM/YYYY
    if (
        typeof valor === "string" &&
        /^\d{2}\/\d{2}\/\d{4}$/.test(valor)
    ) {

        const partes = valor.split("/");

        return new Date(
            Number(partes[2]),
            Number(partes[1]) - 1,
            Number(partes[0])
        );
    }


    const data = new Date(valor);

    if (isNaN(data.getTime())) {
        return null;
    }

    return data;
}


// ------------------------------------------------------------
// NORMALIZA DATA
// Retorna YYYY-MM-DD
// ------------------------------------------------------------

function normalizarData(valor) {

    const data = dataValida(valor);

    if (!data) {
        return null;
    }

    const ano = data.getFullYear();

    const mes = String(
        data.getMonth() + 1
    ).padStart(2, "0");

    const dia = String(
        data.getDate()
    ).padStart(2, "0");

    return `${ano}-${mes}-${dia}`;
}


// ------------------------------------------------------------
// FORMATA DATA PARA EXIBIÇÃO
// ------------------------------------------------------------

function formatarData(valor) {

    const data = dataValida(valor);

    if (!data) {
        return "";
    }

    return data.toLocaleDateString(
        "pt-BR",
        {
            day: "2-digit",
            month: "2-digit"
        }
    );
}


// ============================================================
// IDENTIFICA STATUS
// ============================================================

function pedidoCancelado(pedido) {

    return ehSim(
        valorCampo(
            pedido,
            "cancelado",
            "Cancelado"
        )
    );
}


function pedidoFaturado(pedido) {

    const faturado = ehSim(
        valorCampo(
            pedido,
            "faturado",
            "Faturado"
        )
    );

    const status = String(
        valorCampo(
            pedido,
            "statusPedido",
            "status_pedido"
        ) || ""
    ).trim().toLowerCase();


    return (
        faturado ||
        status === "faturado"
    );
}


function pedidoAFaturar(pedido) {

    if (pedidoCancelado(pedido)) {
        return false;
    }

    return !pedidoFaturado(pedido);
}


// ============================================================
// OBTÉM VALOR DO PEDIDO
// ============================================================

function valorPedido(pedido) {

    return numero(
        valorCampo(
            pedido,
            "Valor do Pedido",
            "valor_pedido",
            "valorPedido"
        )
    );
}


// ============================================================
// ATUALIZA CARDS
// ============================================================

function atualizarCards(dados) {

    let totalPedidos = dados.length;

    let valorPedidos = 0;

    let totalFaturados = 0;

    let valorFaturado = 0;

    let totalCancelados = 0;

    let totalAFaturar = 0;


    dados.forEach(pedido => {

        const valor = valorPedido(pedido);

        valorPedidos += valor;


        // ----------------------------------------------------
        // CANCELADO
        // ----------------------------------------------------

        if (pedidoCancelado(pedido)) {

            totalCancelados++;

            return;
        }


        // ----------------------------------------------------
        // FATURADO
        // ----------------------------------------------------

        if (pedidoFaturado(pedido)) {

            totalFaturados++;

            valorFaturado += valor;

            return;
        }


        // ----------------------------------------------------
        // A FATURAR
        // ----------------------------------------------------

        totalAFaturar++;

    });


    // --------------------------------------------------------
    // VALOR EM ABERTO
    // --------------------------------------------------------

    const valorAberto = Math.max(
        valorPedidos - valorFaturado,
        0
    );


    // --------------------------------------------------------
    // CONVERSÃO
    // --------------------------------------------------------

    const conversaoQuantidade =
        totalPedidos > 0
            ? (
                totalFaturados /
                totalPedidos
            ) * 100
            : 0;


    const conversaoValor =
        valorPedidos > 0
            ? (
                valorFaturado /
                valorPedidos
            ) * 100
            : 0;


    // --------------------------------------------------------
    // ATUALIZA CARDS
    // --------------------------------------------------------

    document.getElementById(
        "totalPedidos"
    ).textContent =
        formatarNumero(totalPedidos);


    document.getElementById(
        "valorPedidos"
    ).textContent =
        formatarMoeda(valorPedidos);


    document.getElementById(
        "totalFaturados"
    ).textContent =
        formatarNumero(totalFaturados);


    document.getElementById(
        "valorFaturado"
    ).textContent =
        formatarMoeda(valorFaturado);


    document.getElementById(
        "totalCancelados"
    ).textContent =
        formatarNumero(totalCancelados);


    document.getElementById(
        "totalAFaturar"
    ).textContent =
        formatarNumero(totalAFaturar);


    // --------------------------------------------------------
    // STATUS
    // --------------------------------------------------------

    document.getElementById(
        "statusFaturados"
    ).textContent =
        formatarNumero(totalFaturados);


    document.getElementById(
        "statusAFaturar"
    ).textContent =
        formatarNumero(totalAFaturar);


    document.getElementById(
        "statusCancelados"
    ).textContent =
        formatarNumero(totalCancelados);


    const totalStatus =
        totalFaturados +
        totalAFaturar +
        totalCancelados;


    const percentualFaturados =
        totalStatus > 0
            ? (
                totalFaturados /
                totalStatus
            ) * 100
            : 0;


    const percentualAFaturar =
        totalStatus > 0
            ? (
                totalAFaturar /
                totalStatus
            ) * 100
            : 0;


    const percentualCancelados =
        totalStatus > 0
            ? (
                totalCancelados /
                totalStatus
            ) * 100
            : 0;


    document.getElementById(
        "progressFaturados"
    ).style.width =
        `${percentualFaturados}%`;


    document.getElementById(
        "progressAFaturar"
    ).style.width =
        `${percentualAFaturar}%`;


    document.getElementById(
        "progressCancelados"
    ).style.width =
        `${percentualCancelados}%`;


    // --------------------------------------------------------
    // CONVERSÃO
    // --------------------------------------------------------

    document.getElementById(
        "conversaoQuantidade"
    ).textContent =
        `${conversaoQuantidade.toFixed(1)}%`;


    document.getElementById(
        "conversaoValor"
    ).textContent =
        `${conversaoValor.toFixed(1)}%`;


    // --------------------------------------------------------
    // VALOR ABERTO
    // --------------------------------------------------------

    document.getElementById(
        "valorAberto"
    ).textContent =
        formatarMoeda(valorAberto);


    const percentualValor =
        valorPedidos > 0
            ? (
                valorFaturado /
                valorPedidos
            ) * 100
            : 0;


    document.getElementById(
        "progressValor"
    ).style.width =
        `${Math.min(percentualValor, 100)}%`;

}


// ============================================================
// GRÁFICO — PEDIDOS POR DATA DE INCLUSÃO
// ============================================================

function atualizarGraficoPedidos(dados) {

    const agrupado = {};


    dados.forEach(pedido => {

        const data = normalizarData(
            valorCampo(
                pedido,
                "dIncl",
                "DIncl"
            )
        );


        if (!data) {
            return;
        }


        agrupado[data] =
            (agrupado[data] || 0) + 1;

    });


    const datas =
        Object.keys(agrupado).sort();


    const labels =
        datas.map(data => {

            return formatarData(data);

        });


    const valores =
        datas.map(data => {

            return agrupado[data];

        });


    const canvas =
        document.getElementById(
            "pedidosChart"
        );


    if (!canvas) {
        return;
    }


    if (pedidosChart) {
        pedidosChart.destroy();
    }


    pedidosChart = new Chart(
        canvas,
        {

            type: "line",

            data: {

                labels: labels,

                datasets: [
                    {

                        label: "Pedidos",

                        data: valores,

                        tension: 0.35,

                        fill: true,

                        borderWidth: 2,

                        pointRadius: 3,

                        pointHoverRadius: 5

                    }
                ]

            },


            options: {

                responsive: true,

                maintainAspectRatio: false,


                interaction: {

                    intersect: false,

                    mode: "index"

                },


                plugins: {

                    legend: {
                        display: false
                    },

                    tooltip: {

                        callbacks: {

                            label: function(context) {

                                return (
                                    " " +
                                    formatarNumero(
                                        context.raw
                                    ) +
                                    " pedidos"
                                );

                            }

                        }

                    }

                },


                scales: {

                    y: {

                        beginAtZero: true,

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


// ============================================================
// GRÁFICO — FATURAMENTO POR DATA
// ============================================================

function atualizarGraficoFaturamento(dados) {

    const agrupado = {};


    dados.forEach(pedido => {

        // ----------------------------------------------------
        // Só entra faturamento efetivamente realizado
        // ----------------------------------------------------

        if (pedidoCancelado(pedido)) {
            return;
        }


        if (!pedidoFaturado(pedido)) {
            return;
        }


        const data = normalizarData(
            valorCampo(
                pedido,
                "dfat",
                "dFat",
                "DFat"
            )
        );


        if (!data) {
            return;
        }


        const valor =
            valorPedido(pedido);


        agrupado[data] =
            (agrupado[data] || 0) + valor;

    });


    const datas =
        Object.keys(agrupado).sort();


    const labels =
        datas.map(data => {

            return formatarData(data);

        });


    const valores =
        datas.map(data => {

            return agrupado[data];

        });


    const canvas =
        document.getElementById(
            "faturamentoChart"
        );


    if (!canvas) {
        return;
    }


    if (faturamentoChart) {
        faturamentoChart.destroy();
    }


    faturamentoChart = new Chart(
        canvas,
        {

            type: "line",

            data: {

                labels: labels,

                datasets: [
                    {

                        label: "Faturamento",

                        data: valores,

                        tension: 0.35,

                        fill: true,

                        borderWidth: 2,

                        pointRadius: 3,

                        pointHoverRadius: 5

                    }
                ]

            },


            options: {

                responsive: true,

                maintainAspectRatio: false,


                interaction: {

                    intersect: false,

                    mode: "index"

                },


                plugins: {

                    legend: {
                        display: false
                    },

                    tooltip: {

                        callbacks: {

                            label: function(context) {

                                return (
                                    " " +
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

                            callback: function(value) {

                                return formatarMoeda(
                                    value
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


// ============================================================
// ESTADO VAZIO
// ============================================================

function atualizarEstadoVazio(dados) {

    const emptyState =
        document.getElementById(
            "emptyState"
        );


    if (!emptyState) {
        return;
    }


    if (dados.length === 0) {

        emptyState.style.display =
            "block";

    } else {

        emptyState.style.display =
            "none";

    }

}


// ============================================================
// ATUALIZA DASHBOARD
// ============================================================

function atualizarDashboard(dados) {

    dadosFiltrados = [...dados];


    atualizarCards(
        dados
    );


    atualizarGraficoPedidos(
        dados
    );


    atualizarGraficoFaturamento(
        dados
    );


    atualizarEstadoVazio(
        dados
    );

}


// ============================================================
// FILTRO POR DATA DE INCLUSÃO
// ============================================================

function aplicarFiltro() {

    const dataInicio =
        document.getElementById(
            "dataInicio"
        ).value;


    const dataFim =
        document.getElementById(
            "dataFim"
        ).value;


    // --------------------------------------------------------
    // Sem filtro
    // --------------------------------------------------------

    if (!dataInicio && !dataFim) {

        atualizarDashboard(
            dadosOriginais
        );

        return;
    }


    dadosFiltrados =
        dadosOriginais.filter(pedido => {

            const dataPedido =
                normalizarData(
                    valorCampo(
                        pedido,
                        "dIncl",
                        "DIncl"
                    )
                );


            if (!dataPedido) {
                return false;
            }


            // ------------------------------------------------
            // DATA INICIAL
            // ------------------------------------------------

            if (
                dataInicio &&
                dataPedido < dataInicio
            ) {

                return false;

            }


            // ------------------------------------------------
            // DATA FINAL
            // ------------------------------------------------

            if (
                dataFim &&
                dataPedido > dataFim
            ) {

                return false;

            }


            return true;

        });


    atualizarDashboard(
        dadosFiltrados
    );

}


// ============================================================
// LIMPAR FILTRO
// ============================================================

function limparFiltro() {

    document.getElementById(
        "dataInicio"
    ).value = "";


    document.getElementById(
        "dataFim"
    ).value = "";


    atualizarDashboard(
        dadosOriginais
    );

}


// ============================================================
// INICIALIZAÇÃO
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        console.log(
            "📦 Dashboard de pedidos iniciado."
        );


        console.log(
            "Pedidos recebidos:",
            dadosOriginais.length
        );


        atualizarDashboard(
            dadosOriginais
        );

    }
);