let lastSelectedChoice = "this phone";
let isPredefined = false;

document.addEventListener("DOMContentLoaded", function () {
    const aiPopup = document.getElementById("ai-popup");
    const closeAiBtn = document.getElementById("close-ai");
    const aiInput = document.getElementById("ai-input");
    const sendAiBtn = document.getElementById("send-ai"); 
    const aiMessages = document.getElementById("ai-messages"); 
    const clearChatBtn = document.getElementById("clear-chat");

    aiPopup.style.display = "none";

    // Display saved chat history
    const savedMessages = localStorage.getItem("aiChatHistory");
    if (savedMessages) {
        aiMessages.innerHTML = savedMessages;
    }

    // Send a predefined message to the AI based on user selection
    function sendPredefinedMessage(promptTemplate) {
        const predefinedPrompt = promptTemplate
            .replace("selectedChoice_placeholder", lastSelectedChoice)
            // .replace("opponent_placeholder", lastOpponentChoice); // TODO: Get the opposing phone in the duel to compare with 

        isPredefined = true;
        aiInput.value = predefinedPrompt
        sendMessage();
        aiInput.value = "";
    }

    // Display the AI pop-up when a choice button is right-clicked 
    document.addEventListener("contextmenu", function (event) {
        const choiceButton = event.target.closest(".choice-button");
        if (choiceButton && !choiceButton.disabled) {  
            event.preventDefault();
            lastSelectedChoice = choiceButton.innerText;
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

        // Append and display user message if it is not a predefined prompt
        if (!isPredefined) {
            aiMessages.innerHTML += `<p><strong>You:</strong> ${message}</p>`;  
            localStorage.setItem("aiChatHistory", aiMessages.innerHTML);  
        }
      
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

        // Append the AI response and save the chat history
        .then(data => {

            // Render markdown language properly
            const formattedData = marked.parse(data);
            aiMessages.innerHTML += `<p><strong>Pab:</strong> </p>` + formattedData; 
            aiMessages.scrollTop = aiMessages.scrollHeight; 
            localStorage.setItem("aiChatHistory", aiMessages.innerHTML); 
        })
        .catch(() => {
            aiMessages.innerHTML += `<p><strong>Error:</strong> AI is unavailable.</p>`;
            localStorage.setItem("aiChatHistory", aiMessages.innerHTML);
        });

        aiInput.value = "";
    }
    
    // Handle both click and Enter key events
    sendAiBtn.addEventListener("click", sendMessage);
    aiInput.addEventListener("keypress", event => {
        if (event.key === "Enter") sendMessage();
    });

    // Clear messages from UI and localStorage 
    clearChatBtn.addEventListener("click", function () {
        aiMessages.innerHTML = "";
        localStorage.removeItem("aiChatHistory");
    });

    // Get CSRF token
    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }

    window.sendPredefinedMessage = sendPredefinedMessage;

});
