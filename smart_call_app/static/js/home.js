
// Functionality for adding and removing input fields
let choiceCount = 2;

function addChoice() {
    if (choiceCount < 8) { 
        choiceCount++;

        // Get the choices and create a wrapper to apply styles to the input field and buttons
        const container = document.getElementById("choicesContainer");
        const choiceWrapper = document.createElement("div");
        choiceWrapper.classList.add("choice-wrapper");
        choiceWrapper.id = "choice" + choiceCount + "-container";

        // Create the new input field
        const newInput = document.createElement("input");
        newInput.type = "text";
        newInput.name = "choice" + choiceCount;
        newInput.placeholder = "Smartphone Choice " + choiceCount;

        // Create the remove button and decrement choiceCount 
        const removeBtn = document.createElement("button");
        removeBtn.classList.add("remove-choice");
        removeBtn.innerText = "X";
        removeBtn.onclick = function () {
            choiceWrapper.remove();
            choiceCount--;
            updateAddButton();
        };

        // Remove previous "+" button before adding a new one
        document.querySelectorAll(".add-choice").forEach(btn => btn.remove());
        const addBtn = document.createElement("button");
        addBtn.classList.add("add-choice");
        addBtn.innerText = "+";
        addBtn.onclick = addChoice;

        // Append elements to the wrapper
        choiceWrapper.appendChild(newInput);
        choiceWrapper.appendChild(removeBtn);

        // Append the new choice to the container
        container.appendChild(choiceWrapper);

        updateAddButton();
    }
}


// Ensure the add button is displayed only on the recently added field
function updateAddButton() {
    const existingChoices = document.querySelectorAll(".choice-wrapper");

    // Remove the add button when the limit of 8 choices is reached
    if (choiceCount === 8) {
        document.querySelectorAll(".add-choice").forEach(btn => btn.remove());
        return; 
    }

    // Add the "+" button to only the last choice in the list
    if (existingChoices.length > 1) {
        const lastChoice = existingChoices[existingChoices.length - 1];
        if (!lastChoice.querySelector(".add-choice")) {
            const newAddBtn = document.createElement("button");
            newAddBtn.classList.add("add-choice");
            newAddBtn.innerText = "+";
            newAddBtn.onclick = addChoice;
            lastChoice.appendChild(newAddBtn);
        }
    }
}