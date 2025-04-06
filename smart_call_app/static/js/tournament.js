let lastSelectedChoice = "this phone";
let isPredefined = false;

document.addEventListener("DOMContentLoaded", function () {
    const aiPopup = document.getElementById("ai-popup");
    const closeAiBtn = document.getElementById("close-ai");
    const aiInput = document.getElementById("ai-input");
    const sendAiBtn = document.getElementById("send-ai"); 
    const aiMessages = document.getElementById("ai-messages"); 
    const clearChatBtn = document.getElementById("clear-chat");
    const roundColumns = Array.from(document.querySelectorAll('.round-column'));

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
            .replace("opponent_placeholder", lastOpponentChoice); 

        isPredefined = true;
        aiInput.value = predefinedPrompt
        sendMessage();
        aiInput.value = "";
        isPredefined = false;
    }

    // Display the AI pop-up when a choice button is right-clicked 
    document.addEventListener("contextmenu", function (event) {
        const choiceButton = event.target.closest(".choice-button");
        if (choiceButton && !choiceButton.disabled) {  
            event.preventDefault();
            lastSelectedChoice = choiceButton.innerText;
            lastOpponentChoice = choiceButton.dataset.opponent; // Get the opposing phone in the duel to compare with 
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

            // Render AI Markdown properly
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


    // Apply the removal animation based on the first choice that the user clicks in a new round
    document.querySelectorAll('form.duel-form button[type="submit"]').forEach(button => {
        
        // For each button, add a click event listener
        button.addEventListener('click', event => {

            // Find the form and the round this button belongs to
            const currentRoundColumn = button.closest('form').closest('.round-column');

            const visibleRounds = roundColumns.filter(round => round.offsetParent !== null);

            // Make sure at least 2 visible rounds displat at a time (completed and new active round)
            if (visibleRounds.length >= 2) {

                const firstVisibleRound = visibleRounds[0]; 
                const secondVisibleRound = visibleRounds[1];

                // If a choice was selected in the second visible round, fade the completed round by applying the fade out class
                if (currentRoundColumn === secondVisibleRound) {

                    const alreadySelected = secondVisibleRound.querySelector('button.winner, button.loser');
                    if (!alreadySelected) {

                        // Prevent the form from submitting immediately on this click, but this removes the clicked button’s data from the POST request form
                        event.preventDefault();

                        // So, manually set the hidden winner field before submitting to ensure all necessary data is sent to the backend 
                        const winnerInput = form.querySelector('input[name="winner"]');
                        if (winnerInput) {
                            winnerInput.value = button.value;
                        }

                        firstVisibleRound.classList.add('fade-out');

                        // Delay the page load to show the fading animation
                        setTimeout(() => {
                            const form = button.closest('form'); 
                            form.submit(); 
                        }, 500);
                        return;
                    }
                }
            }
        });
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
