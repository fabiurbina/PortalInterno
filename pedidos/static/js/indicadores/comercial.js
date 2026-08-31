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

        console.log(
            "Dashboard Comercial iniciado."
        );


        definirPeriodoInicial();


        carregarDadosComercial();

    }
);


/* =========================================================
   PERÍODO INICIAL
========================================================= */

function definirPeriodoInicial() {

    const inicio =
        document.getElementById(
            "comercialDataInicio"
        );

    const fim =
        document.getElementById(
            "comercialDataFim"
        );


    if (!inicio || !fim) {

        return;
    }


    const hoje =
        new Date();


    const primeiroMes =
        new Date(
            hoje.getFullYear(),
            hoje.getMonth() - 2,
            1
        );


    inicio.value =
        formatarDataInput(
            primeiroMes
        );


    fim.value =
        formatarDataInput(
            hoje
        );

}


/* =========================================================
   DATA YYYY-MM-DD
========================================================= */

function formatarDataInput(data) {

    const ano =
        data.getFullYear();


    const mes =
        String(
            data.getMonth() + 1
        ).padStart(2, "0");


    const dia =
        String(
            data.getDate()
        ).padStart(2, "0");


    return `${ano}-${mes}-${dia}`;

}


/* =========================================================
   CARREGAR DADOS
========================================================= */

async function carregarDadosComercial() {

    const inicio =
        document.getElementById(
            "comercialDataInicio"
        )?.value;


    const fim =
        document.getElementById(
            "comercialDataFim"
        )?.value;


    if (!inicio || !fim) {

        return;
    }


    try {

        mostrarCarregandoComercial();


        const url =
            `/indicadores/comercial/dados/?inicio=${inicio}&fim=${fim}`;


        const response =
            await fetch(url, {

                headers: {

                    "X-Requested-With":
                        "XMLHttpRequest"

                }

            });


        if (!response.ok) {

            throw new Error(
                `Erro HTTP ${response.status}`
            );

        }


        const dados =
            await response.json();


        if (dados.erro) {

            throw new Error(
                dados.erro
            );

        }


        atualizarDashboardComercial(
            dados
        );


    } catch (erro) {

        console.error(
            "Erro no dashboard comercial:",
            erro
        );


        mostrarErroComercial(
            erro.message
        );

    }

}


/* =========================================================
   ATUALIZAR DASHBOARD
========================================================= */

function atualizarDashboardComercial(
    dados
) {

    atualizarKPIs(
        dados
    );


    atualizarGraficos(
        dados
    );


    atualizarTabelaConquistados(
        dados.conquistados || []
    );


    atualizarTabelaMaiores(
        dados.maiores_convertidos || []
    );


    atualizarTabelaPipeline(
        dados.maiores_pipeline || []
    );


    const atualizado =
        document.getElementById(
            "comercialAtualizado"
        );


    if (atualizado) {

        atualizado.textContent =
            new Date().toLocaleString(
                "pt-BR"
            );

    }

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
        dados.total_conquistadas || 0
    );


    definirTexto(
        "comercialKpiTaxa",
        formatarPercentual(
            dados.taxa_conversao
        )
    );


    definirTexto(
        "comercialKpiPipeline",
        formatarMoeda(
            dados.valor_pipeline
        )
    );


    definirTexto(
        "comercialKpiConvertido",
        formatarMoeda(
            dados.valor_conquistado
        )
    );


    definirTexto(
        "comercialKpiPedidos",
        dados.total_pedidos || 0
    );


    definirTexto(
        "comercialKpiTicket",
        formatarMoeda(
            dados.ticket_medio
        )
    );


    const clientes =
        document.getElementById(
            "comercialQtdClientesConvertidos"
        );


    if (clientes) {

        clientes.textContent =
            `${dados.clientes_convertidos || 0} clientes`;

    }

}


/* =========================================================
   GRÁFICOS
========================================================= */

function atualizarGraficos(
    dados
) {

    destruirGraficos();


    criarGraficoPipeline(
        dados
    );


    criarGraficoTemperatura(
        dados
    );


    criarGraficoSolucao(
        dados
    );


    criarGraficoStatus(
        dados
    );


    criarGraficoConversao(
        dados
    );


    criarGraficoDesfecho(
        dados
    );

}


/* =========================================================
   PIPELINE
========================================================= */

function criarGraficoPipeline(
    dados
) {

    const canvas =
        document.getElementById(
            "comercialPipeline"
        );


    if (!canvas) {

        return;
    }


    const etapas =
        dados.pipeline_por_status || {};


    comercialGraficos.pipeline =
        new Chart(

            canvas,

            {

                type: "bar",

                data: {

                    labels:
                        Object.keys(
                            etapas
                        ),

                    datasets: [

                        {

                            data:
                                Object.values(
                                    etapas
                                ),

                            borderWidth: 0,

                            borderRadius: 4

                        }

                    ]

                },


                options:
                    opcoesGraficoBase(
                        true
                    )

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


    const temperatura =
        dados.temperatura || {};


    comercialGraficos.temperatura =
        new Chart(

            canvas,

            {

                type: "bar",

                data: {

                    labels:
                        Object.keys(
                            temperatura
                        ),

                    datasets: [

                        {

                            data:
                                Object.values(
                                    temperatura
                                ),

                            borderWidth: 0,

                            borderRadius: 4

                        }

                    ]

                },


                options:
                    opcoesGraficoBase(
                        true
                    )

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


    const solucao =
        dados.solucao || {};


    comercialGraficos.solucao =
        new Chart(

            canvas,

            {

                type: "doughnut",

                data: {

                    labels:
                        Object.keys(
                            solucao
                        ),

                    datasets: [

                        {

                            data:
                                Object.values(
                                    solucao
                                ),

                            borderWidth: 0

                        }

                    ]

                },


                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    cutout: "62%",

                    plugins: {

                        legend: {

                            display: true,

                            position: "right",

                            labels: {

                                boxWidth: 10,

                                padding: 8,

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


    const status =
        dados.status || {};


    comercialGraficos.status =
        new Chart(

            canvas,

            {

                type: "doughnut",

                data: {

                    labels:
                        Object.keys(
                            status
                        ),

                    datasets: [

                        {

                            data:
                                Object.values(
                                    status
                                ),

                            borderWidth: 0

                        }

                    ]

                },


                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    cutout: "62%",

                    plugins: {

                        legend: {

                            display: true,

                            position: "bottom",

                            labels: {

                                boxWidth: 10,

                                padding: 8,

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


/* =========================================================
   CONVERSÃO
========================================================= */

function criarGraficoConversao(
    dados
) {

    const canvas =
        document.getElementById(
            "comercialConversao"
        );


    if (!canvas) {

        return;
    }


    comercialGraficos.conversao =
        new Chart(

            canvas,

            {

                type: "doughnut",

                data: {

                    labels: [

                        "Pipeline não convertido",

                        "Convertido"

                    ],

                    datasets: [

                        {

                            data: [

                                Math.max(
                                    0,
                                    Number(
                                        dados.valor_pipeline || 0
                                    ) -
                                    Number(
                                        dados.valor_conquistado || 0
                                    )
                                ),

                                Number(
                                    dados.valor_conquistado || 0
                                )

                            ],

                            borderWidth: 0

                        }

                    ]

                },


                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    cutout: "68%",

                    plugins: {

                        legend: {

                            display: true,

                            position: "bottom",

                            labels: {

                                boxWidth: 10,

                                padding: 8,

                                font: {

                                    size: 10

                                }

                            }

                        },

                        tooltip: {

                            callbacks: {

                                label:
                                    function (
                                        contexto
                                    ) {

                                        return (

                                            " " +

                                            formatarMoeda(
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
   DESFECHO
========================================================= */

function criarGraficoDesfecho(
    dados
) {

    const canvas =
        document.getElementById(
            "comercialDesfecho"
        );


    if (!canvas) {

        return;
    }


    comercialGraficos.desfecho =
        new Chart(

            canvas,

            {

                type: "bar",

                data: {

                    labels: [

                        "Convertidas",

                        "Não convertidas"

                    ],

                    datasets: [

                        {

                            data: [

                                Number(
                                    dados.total_conquistadas || 0
                                ),

                                Math.max(

                                    0,

                                    Number(
                                        dados.total_oportunidades || 0
                                    )

                                    -

                                    Number(
                                        dados.total_conquistadas || 0
                                    )

                                )

                            ],

                            borderWidth: 0,

                            borderRadius: 4

                        }

                    ]

                },


                options:
                    opcoesGraficoBase(
                        false
                    )

            }

        );

}


/* =========================================================
   OPÇÕES DOS GRÁFICOS
========================================================= */

function opcoesGraficoBase(
    horizontal
) {

    return {

        responsive: true,

        maintainAspectRatio: false,

        indexAxis:
            horizontal
                ? "y"
                : "x",

        plugins: {

            legend: {

                display: false

            }

        },

        scales: {

            x: {

                beginAtZero: true,

                grid: {

                    color:
                        "rgba(40,50,60,.12)",

                    drawBorder: false

                }

            },

            y: {

                beginAtZero: true,

                grid: {

                    color:
                        "rgba(40,50,60,.12)",

                    drawBorder: false

                }

            }

        }

    };

}


/* =========================================================
   TABELA DE CONVERTIDOS
========================================================= */

function atualizarTabelaConquistados(
    clientes
) {

    const tabela =
        document.getElementById(
            "comercialTabelaConquistados"
        );


    if (!tabela) {

        return;
    }


    tabela.innerHTML = "";


    if (!clientes.length) {

        tabela.innerHTML = `

            <tr>

                <td
                    colspan="6"
                    class="comercial-loading"
                >

                    Nenhum cliente convertido
                    no período.

                </td>

            </tr>

        `;

        return;
    }


    clientes.forEach(

        cliente => {

            const linha =
                document.createElement(
                    "tr"
                );


            const pipeline =
                Number(
                    cliente.pipeline || 0
                );


            const convertido =
                Number(
                    cliente.valor_conquistado || 0
                );


            const taxa =
                pipeline > 0

                    ? (
                        convertido /
                        pipeline
                    ) * 100

                    : 0;


            linha.innerHTML = `

                <td>
                    ${escapeHtml(
                        cliente.cliente || "-"
                    )}
                </td>

                <td class="text-right">
                    ${cliente.oportunidades || 0}
                </td>

                <td class="text-right">
                    ${cliente.pedidos || 0}
                </td>

                <td class="text-right">
                    ${formatarMoeda(
                        pipeline
                    )}
                </td>

                <td class="text-right comercial-valor-convertido">
                    ${formatarMoeda(
                        convertido
                    )}
                </td>

                <td class="text-right comercial-taxa-cliente">
                    ${formatarPercentual(
                        taxa
                    )}
                </td>

            `;


            tabela.appendChild(
                linha
            );

        }

    );

}


/* =========================================================
   MAIORES CONVERSÕES
========================================================= */

function atualizarTabelaMaiores(
    dados
) {

    const tabela =
        document.getElementById(
            "comercialTabelaMaiores"
        );


    if (!tabela) {

        return;
    }


    tabela.innerHTML = "";


    dados
        .slice(0, 8)
        .forEach(

            item => {

                const linha =
                    document.createElement(
                        "tr"
                    );


                linha.innerHTML = `

                    <td>
                        ${escapeHtml(
                            item.cliente || "-"
                        )}
                    </td>

                    <td class="text-right comercial-valor-convertido">
                        ${formatarMoeda(
                            item.valor || 0
                        )}
                    </td>

                `;


                tabela.appendChild(
                    linha
                );

            }

        );

}


/* =========================================================
   MAIORES PIPELINES
========================================================= */

function atualizarTabelaPipeline(
    dados
) {

    const tabela =
        document.getElementById(
            "comercialTabelaPipeline"
        );


    if (!tabela) {

        return;
    }


    tabela.innerHTML = "";


    dados
        .slice(0, 8)
        .forEach(

            item => {

                const linha =
                    document.createElement(
                        "tr"
                    );


                linha.innerHTML = `

                    <td>
                        ${escapeHtml(
                            item.cliente || "-"
                        )}
                    </td>

                    <td class="text-right">
                        ${formatarMoeda(
                            item.valor || 0
                        )}
                    </td>

                `;


                tabela.appendChild(
                    linha
                );

            }

        );

}


/* =========================================================
   FILTRO
========================================================= */

function aplicarFiltroComercial() {

    carregarDadosComercial();

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
   LOADING
========================================================= */

function mostrarCarregandoComercial() {

    const elementos = [

        "comercialKpiTotal",

        "comercialKpiAtivos",

        "comercialKpiConquistadas",

        "comercialKpiTaxa",

        "comercialKpiPipeline",

        "comercialKpiConvertido",

        "comercialKpiPedidos",

        "comercialKpiTicket"

    ];


    elementos.forEach(

        id => {

            definirTexto(
                id,
                "..."
            );

        }

    );

}


/* =========================================================
   ERRO
========================================================= */

function mostrarErroComercial(
    mensagem
) {

    console.error(
        mensagem
    );


    const tabela =
        document.getElementById(
            "comercialTabelaConquistados"
        );


    if (tabela) {

        tabela.innerHTML = `

            <tr>

                <td
                    colspan="6"
                    class="comercial-loading"
                >

                    Não foi possível carregar
                    os dados comerciais.

                </td>

            </tr>

        `;

    }

}


/* =========================================================
   UTILITÁRIOS
========================================================= */

function definirTexto(
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


function formatarPercentual(
    valor
) {

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


function escapeHtml(
    valor
) {

    const div =
        document.createElement(
            "div"
        );


    div.textContent =
        valor;


    return div.innerHTML;

}