document.addEventListener("DOMContentLoaded", function () {

    // =========================================================
    // ELEMENTOS
    // =========================================================

    const input = document.getElementById("messageInput");
    const sendButton = document.getElementById("sendButton");

    const messagesContainer =
        document.getElementById("messages");

    const chatContent =
        document.getElementById("chatContent");

    const welcomeScreen =
        document.getElementById("welcome");

    const typingIndicator =
        document.getElementById("typing");

    const newChatButton =
        document.getElementById("btnNovaConversa");


    // =========================================================
    // CONTROLE
    // =========================================================

    let intervaloDigitando = null;


    // =========================================================
    // CSRF
    // =========================================================

    function getCookie(name) {

        let cookieValue = null;

        if (
            document.cookie &&
            document.cookie !== ""
        ) {

            const cookies =
                document.cookie.split(";");

            for (let cookie of cookies) {

                cookie = cookie.trim();

                if (
                    cookie.startsWith(
                        name + "="
                    )
                ) {

                    cookieValue =
                        decodeURIComponent(
                            cookie.substring(
                                name.length + 1
                            )
                        );

                    break;
                }
            }
        }

        return cookieValue;
    }


    // =========================================================
    // SCROLL
    // =========================================================

    function rolarParaFinal() {

        if (!chatContent) {
            return;
        }

        requestAnimationFrame(() => {

            chatContent.scrollTo({
                top: chatContent.scrollHeight,
                behavior: "smooth"
            });

        });
    }


    // =========================================================
    // ADICIONAR MENSAGEM
    // =========================================================

    function adicionarMensagem(
        texto,
        tipo
    ) {

        if (!messagesContainer) {
            return;
        }

        const message =
            document.createElement("div");

        message.classList.add(
            "message",
            tipo === "user"
                ? "user"
                : "assistant"
        );


        // =====================================================
        // AVATAR DA IA
        // =====================================================

        if (tipo === "assistant") {

            const avatar =
                document.createElement("div");

            avatar.classList.add(
                "message-avatar"
            );

            avatar.textContent = "🤖";

            message.appendChild(avatar);
        }


        // =====================================================
        // CONTEÚDO
        // =====================================================

        const content =
            document.createElement("div");

        content.classList.add(
            "message-content"
        );


        if (tipo === "assistant") {

            // Renderiza Markdown
            if (
                typeof marked !== "undefined" &&
                typeof DOMPurify !== "undefined"
            ) {

                const html =
                    marked.parse(
                        String(texto),
                        {
                            breaks: true,
                            gfm: true
                        }
                    );

                content.innerHTML =
                    DOMPurify.sanitize(
                        html
                    );

            } else {

                // Fallback caso as bibliotecas
                // não estejam disponíveis

                content.textContent =
                    String(texto);
            }

        } else {

            // Mensagem do usuário
            content.textContent =
                String(texto);
        }


        message.appendChild(content);

        messagesContainer.appendChild(
            message
        );


        rolarParaFinal();
    }


    // =========================================================
    // MOSTRAR "DIGITANDO"
    // =========================================================

    function mostrarDigitando() {

        if (!typingIndicator) {
            return;
        }


        // Evita múltiplos intervalos
        if (intervaloDigitando) {

            clearInterval(
                intervaloDigitando
            );

            intervaloDigitando = null;
        }


        const mensagens = [

            "Analisando os dados...",

            "Cruzando CRM e pedidos...",

            "Identificando os principais pontos...",

            "Preparando a análise..."

        ];


        let indice = 0;


        typingIndicator.innerHTML = `

            <div class="typing-avatar">
                🤖
            </div>

            <div class="typing-content">

                <span class="typing-text">
                    ${mensagens[indice]}
                </span>

                <div class="typing-dots">

                    <span></span>
                    <span></span>
                    <span></span>

                </div>

            </div>

        `;


        typingIndicator.classList.add(
            "active"
        );


        intervaloDigitando =
            setInterval(() => {

                indice++;

                if (
                    indice >=
                    mensagens.length
                ) {

                    indice = 0;
                }


                const texto =
                    typingIndicator.querySelector(
                        ".typing-text"
                    );


                if (texto) {

                    texto.textContent =
                        mensagens[indice];
                }


            }, 1800);


        rolarParaFinal();
    }


    // =========================================================
    // ESCONDER "DIGITANDO"
    // =========================================================

    function esconderDigitando() {

        if (intervaloDigitando) {

            clearInterval(
                intervaloDigitando
            );

            intervaloDigitando = null;
        }


        if (typingIndicator) {

            typingIndicator.classList.remove(
                "active"
            );
        }
    }


    // =========================================================
    // ENVIAR MENSAGEM
    // =========================================================

    async function enviarMensagem() {

        if (!input) {
            return;
        }


        const mensagem =
            input.value.trim();


        if (!mensagem) {
            return;
        }


        // =====================================================
        // ESCONDE TELA INICIAL
        // =====================================================

        if (welcomeScreen) {

            welcomeScreen.style.display =
                "none";
        }


        // =====================================================
        // MOSTRA MENSAGEM DO USUÁRIO
        // =====================================================

        adicionarMensagem(
            mensagem,
            "user"
        );


        // =====================================================
        // LIMPA INPUT
        // =====================================================

        input.value = "";

        input.style.height = "auto";


        // =====================================================
        // BLOQUEIA ENVIO
        // =====================================================

        if (sendButton) {

            sendButton.disabled = true;
        }


        // =====================================================
        // MOSTRA PROCESSAMENTO
        // =====================================================

        mostrarDigitando();


        try {

            const response =
                await fetch(
                    "/agente-comercial/chat/",
                    {
                        method: "POST",

                        headers: {

                            "Content-Type":
                                "application/json",

                            "X-CSRFToken":
                                getCookie(
                                    "csrftoken"
                                )
                        },

                        body: JSON.stringify({

                            mensagem:
                                mensagem

                        })
                    }
                );


            // =================================================
            // TENTA LER JSON
            // =================================================

            let data;

            try {

                data =
                    await response.json();

            } catch (erroJson) {

                throw new Error(
                    "Resposta inválida do servidor."
                );
            }


            // =================================================
            // ESCONDE PROCESSAMENTO
            // =================================================

            esconderDigitando();


            // =================================================
            // ERRO DO BACKEND
            // =================================================

            if (
                !response.ok ||
                !data.sucesso
            ) {

                adicionarMensagem(

                    data.erro ||
                    "Não consegui consultar o agente comercial.",

                    "assistant"

                );

                return;
            }


            // =================================================
            // RESPOSTA DA IA
            // =================================================

            adicionarMensagem(

                data.resposta,

                "assistant"

            );


        } catch (erro) {

            console.error(
                "Erro ao chamar agente:",
                erro
            );


            esconderDigitando();


            adicionarMensagem(

                "Não consegui conectar ao agente comercial.",

                "assistant"

            );


        } finally {

            if (sendButton) {

                sendButton.disabled =
                    false;
            }


            input.focus();

        }
    }


    // =========================================================
    // BOTÃO ENVIAR
    // =========================================================

    if (sendButton) {

        sendButton.addEventListener(
            "click",
            enviarMensagem
        );

    }


    // =========================================================
    // ENTER
    // =========================================================

    if (input) {

        input.addEventListener(
            "keydown",
            function (event) {

                if (
                    event.key === "Enter" &&
                    !event.shiftKey
                ) {

                    event.preventDefault();

                    enviarMensagem();

                }

            }
        );

    }


    // =========================================================
    // AUTO RESIZE DO INPUT
    // =========================================================

    if (input) {

        input.addEventListener(
            "input",
            function () {

                this.style.height =
                    "auto";

                this.style.height =
                    this.scrollHeight +
                    "px";

            }
        );

    }


    // =========================================================
    // SUGESTÕES
    // =========================================================

    document
        .querySelectorAll(
            ".suggestion-card"
        )
        .forEach(
            function (card) {

                card.addEventListener(
                    "click",
                    function () {

                        const texto =
                            this.dataset.message;


                        if (!texto) {
                            return;
                        }


                        input.value =
                            texto;


                        input.focus();


                        // Ajusta altura
                        input.style.height =
                            "auto";

                        input.style.height =
                            input.scrollHeight +
                            "px";

                    }
                );

            }
        );


    // =========================================================
    // NOVA CONVERSA
    // =========================================================

    if (newChatButton) {

        newChatButton.addEventListener(
            "click",
            function () {

                // Limpa mensagens
                messagesContainer.innerHTML =
                    "";


                // Mostra tela inicial
                if (welcomeScreen) {

                    welcomeScreen.style.display =
                        "block";
                }


                // Para indicador
                esconderDigitando();


                // Limpa input
                input.value = "";

                input.style.height =
                    "auto";


                input.focus();


                // Volta para o início
                if (chatContent) {

                    chatContent.scrollTo({

                        top: 0,

                        behavior: "smooth"

                    });
                }

            }
        );

    }

});