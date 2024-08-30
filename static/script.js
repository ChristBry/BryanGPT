const chatbox = document.querySelector('.chatbox')
const messageInput = document.querySelector('#message-input')
const sendBtn = document.getElementById('send-btn')

function addMessage(message, isUserMessage) {
    const messageDiv = document.createElement('div')
    messageDiv.classList.add('message')

    if (isUserMessage) {
        messageDiv.classList.add('user-message')
    } else {
        messageDiv.classList.add('bot-messsage')
    }

    messageDiv.innerHTML = `<p>${message}</p>`
    //icon.innerHTML = `<img src="/Static/images/hugging.png" class="user-icon">`
    chatbox.appendChild(messageDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function sendMessage() {
    const message = messageInput.value.trim()
    if (message !== "") {
        addMessage(message, true)

        fetch("/api", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                "user_input": message
            })
        })
            .then(response => response.json())
            .then(data => {
                messageInput.value = "";
                const messageDiv = document.createElement('div')
                messageDiv.classList.add("message")
                messageDiv.classList.add("bot-message")
                const content = data.content
                const hasCodeBlock = content.includes("``")
                if (hasCodeBlock) {
                    const codeContent = content.replace(/```([\s\s]+?)```/g, '<p><pre><code>$1</code></pre></p>')
                    messageDiv.innerHTML = `<p>${codeContent}</p>`
                } else {
                    messageDiv.innerHTML = `<p>${content}</p>`
                }
                chatbox.appendChild(messageDiv)
                chatbox.scrollTop = chatbox.scrollHeight
            })
    } else {
        alert("erreur")
    }
}

sendBtn.addEventListener("click", sendMessage);
messageInput.addEventListener("keydown", event => {
    if (event.keyCode === 13 && !event.shiftKey) {
        event.preventDefault();
        sendMessage()
    }
});

/* Afficher la popup lors du chargement de la page */
