document.addEventListener("DOMContentLoaded", function () {

    const input = document.getElementById("messageInput");
    const sendButton = document.getElementById("sendButton");
    const messagesContainer = document.getElementById("messages");
    const welcomeScreen = document.getElementById("welcomeScreen");
    const typingIndicator = document.getElementById("typingIndicator");
    const newChatButton = document.getElementById("newChatButton");

    // =========================
    // CSRF
    // =========================

    function getCookie(name) {

        let cookieValue = null;

        if (document.cookie && document.cookie !== "") {

            const cookies = document.cookie.split(";");

            for (let cookie of cookies) {

                cookie = cookie.trim();

                if (cookie.startsWith(name + "=")) {

                    cookieValue = decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );

                    break;
                }
            }
        }

        return cookieValue;
    }


    // =========================
    // ADICIONAR MENSAGEM
    // =========================

    function adicionarMensagem(texto, tipo) {

        const message = document.createElement("div");

        message.classList.add(
            "message",
            tipo === "user"
                ? "message-user"
                : "message-assistant"
        );

        const content = document.createElement("div");

        content.classList.add("message-content");

        // Mantém quebra de linha
        content.innerHTML = texto
            .replace(/\n/g, "<br>");

        message.appendChild(content);

        messagesContainer.appendChild(message);

        messagesContainer.scrollTop =
            messagesContainer.scrollHeight;
    }


    // =========================
    // LOADING
    // =========================

    function mostrarDigitando() {

        if (typingIndicator) {
            typingIndicator.style.display = "flex";
        }

        messagesContainer.scrollTop =
            messagesContainer.scrollHeight;
    }


    function esconderDigitando() {

        if (typingIndicator) {
            typingIndicator.style.display = "none";
        }
    }


    // =========================
    // ENVIAR MENSAGEM
    // =========================

    async function enviarMensagem() {

        const mensagem = input.value.trim();

        if (!mensagem) {
            return;
        }

        // Esconde tela inicial
        if (welcomeScreen) {
            welcomeScreen.style.display = "none";
        }

        // Mostra pergunta do usuário
        adicionarMensagem(
            mensagem,
            "user"
        );

        // Limpa campo
        input.value = "";

        input.style.height = "auto";

        // Desabilita botão
        sendButton.disabled = true;

        mostrarDigitando();

        try {

            const response = await fetch(
                "/agente-comercial/chat/",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie("csrftoken")
                    },

                    body: JSON.stringify({
                        mensagem: mensagem
                    })
                }
            );


            const data = await response.json();

            esconderDigitando();


            if (!response.ok || !data.sucesso) {

                adicionarMensagem(
                    data.erro ||
                    "Não consegui consultar o agente comercial.",
                    "assistant"
                );

                return;
            }


            // Resposta da IA
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

            sendButton.disabled = false;

            input.focus();
        }
    }


    // =========================
    // BOTÃO ENVIAR
    // =========================

    sendButton.addEventListener(
        "click",
        enviarMensagem
    );


    // =========================
    // ENTER
    // =========================

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


    // =========================
    // AUTO RESIZE
    // =========================

    input.addEventListener(
        "input",
        function () {

            this.style.height = "auto";

            this.style.height =
                this.scrollHeight + "px";
        }
    );


    // =========================
    // SUGESTÕES
    // =========================

    document
        .querySelectorAll(".suggestion-card")
        .forEach(function (card) {

            card.addEventListener(
                "click",
                function () {

                    const texto =
                        this.dataset.message;

                    if (!texto) {
                        return;
                    }

                    input.value = texto;

                    enviarMensagem();
                }
            );
        });


    // =========================
    // NOVA CONVERSA
    // =========================

    if (newChatButton) {

        newChatButton.addEventListener(
            "click",
            function () {

                messagesContainer.innerHTML = "";

                if (welcomeScreen) {
                    welcomeScreen.style.display =
                        "flex";
                }

                input.value = "";

                input.style.height = "auto";

                input.focus();
            }
        );
    }

});