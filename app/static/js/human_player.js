// Récupère ou initialise le numéro de la ligne courante depuis localStorage
let currentLine = localStorage.getItem('currentLine') ? parseInt(localStorage.getItem('currentLine')) : 1;
let currentSlot = 1;  // Slot actuellement sélectionné

// Fonction pour récupérer la combinaison actuelle
function getCombination() {
    let combination = '';
    const colorToLetter = {
        'red': 'R', 'blue': 'B', 'green': 'V', 'yellow': 'J',
        'black': 'N', 'grey': 'G', 'orange': 'O', 'brown': 'M'
    };

    for (let i = 1; i <= length; i++) {
        const slot = document.getElementById(`slot-${currentLine}-${i}`);
        let slotColor = slot ? slot.style.backgroundColor : '';
        for (let colorKey in colorToLetter) {
            if (slotColor === colorKey) {
                combination += colorToLetter[colorKey];
                break;
            }
        }
    }
    console.log(combination.trim());
    return combination.trim();
}

// Fonction pour mettre à jour les evaluation-slot
function updateEvaluationSlots(line, cplaced, iplaced) {
    let slots = document.querySelectorAll(`.evaluation-area-${line} .evaluation-slot`);
    let index = 0;

    for (let i = 0; i < cplaced; i++) {
        if (index < slots.length) {
            slots[index].style.backgroundColor = "red";
            localStorage.setItem(`evaluation-slot-${line}-${index}`, "red");
            index++;
        }
    }

    for (let i = 0; i < iplaced; i++) {
        if (index < slots.length) {
            slots[index].style.backgroundColor = "white";
            localStorage.setItem(`evaluation-slot-${line}-${index}`, "white");
            index++;
        }
    }
}



// Gestion du bouton Submit
const combinationButton = document.getElementById("submit");
if (combinationButton) {
    combinationButton.addEventListener('click', function() {
        currentLine++;
        localStorage.setItem('currentLine', currentLine);
        currentSlot = 1;
    });
}

// Réinitialisation du jeu
function resetGame() {
    localStorage.clear();
}

// Drag & Drop pour sélectionner les couleurs
function handleDragStart(event) {
    event.dataTransfer.setData("text/plain", event.target.getAttribute('data-color'));
}

document.querySelectorAll('.color-option').forEach(function(colorElement) {
    colorElement.addEventListener('dragstart', handleDragStart);
});

// Gestion du drag & drop sur les slots
function handleDragOver(event) {
    const slot = event.currentTarget;
    const parts = slot.id.split('-');
    const slotLine = parseInt(parts[1]);

    if (slotLine !== currentLine) {
        return;
    }
    event.preventDefault();
}

function handleDrop(event) {
    const slot = event.currentTarget;
    const parts = slot.id.split('-');
    const slotLine = parseInt(parts[1]);

    if (slotLine !== currentLine) {
        console.error("Drop interdit sur une ligne inactive.");
        return;
    }
    event.preventDefault();
    const color = event.dataTransfer.getData("text/plain");

    if (color) {
        slot.style.backgroundColor = color;
        slot.classList.remove("animate-drop");
        void slot.offsetWidth;
        slot.classList.add("animate-drop");

        localStorage.setItem(slot.id, color);
        document.getElementById("combination").value = getCombination();
    }
}

document.querySelectorAll('.slot').forEach(function(slotElement) {
    slotElement.addEventListener('dragover', handleDragOver);
    slotElement.addEventListener('drop', handleDrop);
});



function removeResetParam() {
    const url = new URL(window.location);
    url.searchParams.delete('reset');  // Retire le paramètre run_js
    window.history.replaceState({}, document.title, url.toString());  // Met à jour l'URL sans recharger la page
}

// Restauration des couleurs au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    console.log(solution)
    updateEvaluationSlots(currentLine - 1 , cplaced, iplaced);
    for (let line = 1; line < currentLine; line++) {
        for (let slot = 1; slot <= length; slot++) {
            const slotKey = `slot-${line}-${slot}`;
            const savedColor = localStorage.getItem(slotKey);
            if (savedColor) {
                const slotElement = document.getElementById(slotKey);
                if (slotElement) {
                    slotElement.style.backgroundColor = savedColor;
                }
            }
        }

        let slots = document.querySelectorAll(`.evaluation-area-${line} .evaluation-slot`);
        slots.forEach((slot, index) => {
            let savedColor = localStorage.getItem(`evaluation-slot-${line}-${index}`);
            if (savedColor) {
                slot.style.backgroundColor = savedColor;
            }
        });
    }

    const arrow = document.querySelector(".arrow-container");
    if (arrow) {
        const lineHeight = 55;
        const translationY = (currentLine - 1) * lineHeight;
        arrow.style.transform = `translateY(-${Math.min(translationY, (nbr_of_line - 1) * lineHeight)}px)`;
    }

    const params = new URLSearchParams(window.location.search);
    if (params.get('reset') === 'true') {
        resetGame();  // Appelle ta fonction JS
        removeResetParam();  // Retire le paramètre de l'URL
    }
});