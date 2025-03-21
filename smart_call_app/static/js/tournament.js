
document.addEventListener("DOMContentLoaded", function () {
    const aiPopup = document.getElementById("ai-popup");
    const closeAiBtn = document.getElementById("close-ai");
    const aiInput = document.getElementById("ai-input");
    const sendAiBtn = document.getElementById("send-ai"); 
    const aiMessages = document.getElementById("ai-messages"); 

    aiPopup.style.display = "none";

    // Display the AI pop-up when a choice button is right-clicked 
    document.addEventListener("contextmenu", function (event) {
        const choiceButton = event.target.closest(".choice-button");
        if (choiceButton && !choiceButton.disabled) {  
            event.preventDefault();
            aiPopup.style.display = "block"; 
        }
    });

    // Close AI pop-up 
    closeAiBtn.addEventListener("click", function () {
        aiPopup.style.display = "none";
    });

    // Send message on click or Enter key
    function sendMessage() {
        const message = aiInput.value.trim();
        if (!message) return;

        // Append user message
        aiMessages.innerHTML += `<p><strong>You:</strong> ${message}</p>`;

        // Send request to Django
        fetch(window.location.pathname + "chat/", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCSRFToken(),
            },
            body: `query=${encodeURIComponent(message)}`,
        })
        .then(response => response.text())

        // Append the AI response
        .then(data => {
            aiMessages.innerHTML += `<p>${data}</p>`; 
            aiMessages.scrollTop = aiMessages.scrollHeight; 
        })
        .catch(() => {
            aiMessages.innerHTML += `<p><strong>Error:</strong> AI is unavailable.</p>`;
        });

        aiInput.value = "";
    }

    // Handle both click and Enter key events
    sendAiBtn.addEventListener("click", sendMessage);
    aiInput.addEventListener("keypress", event => {
        if (event.key === "Enter") sendMessage();
    });

    // Get CSRF token
    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }

});
