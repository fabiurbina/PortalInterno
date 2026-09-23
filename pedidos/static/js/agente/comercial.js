document.addEventListener("DOMContentLoaded", function () {

    const input = document.getElementById("messageInput");
    const sendButton = document.getElementById("sendButton");

    const messages = document.getElementById("messages");
    const welcome = document.getElementById("welcome");

    const typing = document.getElementById("typing");

    const novaConversa = document.getElementById(
        "btnNovaConversa"
    );


    // ======================================================
    // AUTO RESIZE DO TEXTAREA
    // ======================================================

    input.addEventListener("input", function () {

        this.style.height = "auto";

        this.style.height =
            Math.min(this.scrollHeight, 140) + "px";

    });


    // ======================================================
    // ENVIAR COM ENTER
    // SHIFT + ENTER = NOVA LINHA
    // ======================================================

    input.addEventListener("keydown", function (event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            enviarMensagem();

        }

    });


    // ======================================================
    // BOTÃO ENVIAR
    // ======================================================

    sendButton.addEventListener(
        "click",
        enviarMensagem
    );


    // ======================================================
    // PERGUNTAS SUGERIDAS
    // ======================================================

    document
        .querySelectorAll(".suggestion-card")
        .forEach(function (card) {

            card.addEventListener(
                "click",
                function () {

                    const pergunta =
                        this.dataset.question;

                    input.value = pergunta;

                    input.dispatchEvent(
                        new Event("input")
                    );

                    enviarMensagem();

                }
            );

        });


    // ======================================================
    // NOVA CONVERSA
    // ======================================================

    novaConversa.addEventListener(
        "click",
        function () {

            messages.innerHTML = "";

            welcome.style.display = "block";

            input.value = "";

            input.style.height = "auto";

            input.focus();

        }
    );


    // ======================================================
    // ENVIAR MENSAGEM
    // ======================================================

    function enviarMensagem() {

        const texto =
            input.value.trim();

        if (!texto) {
            return;
        }


        // Esconde welcome

        welcome.style.display = "none";


        // Adiciona mensagem do usuário

        adicionarMensagem(
            texto,
            "user"
        );


        // Limpa campo

        input.value = "";

        input.style.height = "auto";


        // Mostra loading

        mostrarLoading();


        /*
         * TEMPORÁRIO
         *
         * Ainda não estamos chamando o Django.
         *
         * Na próxima etapa vamos conectar aqui:
         *
         * fetch("/agente-comercial/chat/", ...)
         *
         */


        setTimeout(function () {

            esconderLoading();

            adicionarMensagem(

                "Estou conectado à interface. Na próxima etapa vamos ligar esta conversa ao seu agente comercial e ao Groq.",

                "assistant"

            );

        }, 800);

    }


    // ======================================================
    // ADICIONAR MENSAGEM
    // ======================================================

    function adicionarMensagem(
        texto,
        tipo
    ) {

        const message =
            document.createElement("div");


        message.className =
            "message " + tipo;


        const avatar =
            document.createElement("div");


        avatar.className =
            "message-avatar";


        avatar.textContent =
            tipo === "user"
                ? "👤"
                : "🤖";


        const content =
            document.createElement("div");


        content.className =
            "message-content";


        content.textContent =
            texto;


        if (tipo === "user") {

            message.appendChild(content);

            message.appendChild(avatar);

        } else {

            message.appendChild(avatar);

            message.appendChild(content);

        }


        messages.appendChild(message);


        scrollChat();

    }


    // ======================================================
    // LOADING
    // ======================================================

    function mostrarLoading() {

        typing.classList.add("active");

        scrollChat();

    }


    function esconderLoading() {

        typing.classList.remove("active");

    }


    // ======================================================
    // SCROLL
    // ======================================================

    function scrollChat() {

        const container =
            document.getElementById(
                "chatContent"
            );

        container.scrollTop =
            container.scrollHeight;

    }

});