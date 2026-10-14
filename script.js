
const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");
const messages = document.getElementById("messages");
const typing = document.getElementById("typing");
const sendButton = document.getElementById("send-button");
const newChatButton = document.getElementById("new-chat");

let history = [];

function addMessage(text, role) {
    const message = document.createElement("div");
    message.className = `message ${role}`;

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    // Render the response as text rather than executable HTML.
    bubble.textContent = text;

    message.appendChild(bubble);
    messages.appendChild(message);

    messages.scrollTop = messages.scrollHeight;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = input.value.trim();

    if (!message) return;

    addMessage(message, "user");

    input.value = "";
    input.disabled = true;
    sendButton.disabled = true;

    typing.classList.remove("hidden");

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message,
                history: history
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "The request failed.");
        }

        addMessage(data.reply, "bot");

        history.push(
            { role: "user", content: message },
            { role: "assistant", content: data.reply }
        );

        history = history.slice(-10);

    } catch (error) {
        console.error(error);

        addMessage(
            "Sorry, something went wrong. Please try again.",
            "bot"
        );

    } finally {
        typing.classList.add("hidden");
        input.disabled = false;
        sendButton.disabled = false;
        input.focus();
    }
});

newChatButton.addEventListener("click", () => {
    history = [];

    messages.replaceChildren();

    addMessage(
        "Hey! 👋 I'm Nova AI. What would you like to explore today?",
        "bot"
    );

    input.focus();
});

