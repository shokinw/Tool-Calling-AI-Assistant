
const form = document.getElementById("chat-form");
const input = document.getElementById("question");
const chat = document.getElementById("chat");
const sendButton = document.getElementById("send-button");
const welcome = document.getElementById("welcome");

function addMessage(text, type) {
    const message = document.createElement("div");
    message.className = `message ${type}`;
    message.textContent = text;
    chat.appendChild(message);
    chat.scrollTop = chat.scrollHeight;
    return message;
}

async function sendQuestion(question) {
    if (!question.trim() || sendButton.disabled) return;

    welcome?.remove();

    addMessage(question, "user");
    input.value = "";
    sendButton.disabled = true;
    sendButton.textContent = "…";

    const loading = addMessage("Thinking and checking available tools…", "assistant");

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || `Request failed (${response.status})`);
        }

        loading.textContent = data.answer;
    } catch (error) {
        loading.classList.add("error");
        loading.textContent =
            `Could not reach the assistant. Make sure your FastAPI server is running. Details: ${error.message}`;
    } finally {
        sendButton.disabled = false;
        sendButton.textContent = "↑";
        input.focus();
        chat.scrollTop = chat.scrollHeight;
    }
}

form.addEventListener("submit", (event) => {
    event.preventDefault();
    sendQuestion(input.value);
});

document.querySelectorAll(".suggestion").forEach((button) => {
    button.addEventListener("click", () => {
        sendQuestion(button.dataset.question);
    });
});

input.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        form.requestSubmit();
    }
});
