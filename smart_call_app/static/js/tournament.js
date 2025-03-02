
document.addEventListener("DOMContentLoaded", function () {
    const aiPopup = document.getElementById("ai-popup");
    const closeAiBtn = document.getElementById("close-ai");

    aiPopup.style.display = "none";

    // Display the AI popup when a choice button is right-clicked 
    document.addEventListener("contextmenu", function (event) {
        const choiceButton = event.target.closest(".choice-button");
        if (choiceButton && !choiceButton.disabled) {  
            event.preventDefault();
            aiPopup.style.display = "block"; 
        }
    });
    
    closeAiBtn.addEventListener("click", function () {
        aiPopup.style.display = "none";
    });
});
