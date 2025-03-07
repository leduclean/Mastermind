// Récupère ou initialise le numéro de la ligne courante depuis localStorage
let currentLine = localStorage.getItem('currentLine') ? parseInt(localStorage.getItem('currentLine')) : 1;
let currentSlot = 1;  // Slot actuellement sélectionné

// Fonction qui change la couleur d'un slot et la sauvegarde dans localStorage
function changeColor(color) {
    const slotId = `slot-${currentLine}-${currentSlot}`;
    const slot = document.getElementById(slotId);
    if (slot) {
        slot.style.backgroundColor = color;
        localStorage.setItem(slotId, color);
        document.getElementById("combination").value = getCombination();
    } else {
        console.error(`Element with ID ${slotId} not found.`);
    }
}

// Fonction pour construire la combinaison actuelle en utilisant la première lettre de chaque couleur
function getCombination() {
    let combination = '';
    const colorToLetter = {
        'red': 'R',    // Rouge
        'blue': 'B',   // Bleu
        'green': 'V',  // Vert (V pour "vert")
        'yellow': 'J', // Jaune (J pour "jaune")
        'black': 'N',  // Noir (N pour "noir")
        'grey': 'G',
        'orange': 'O',
        'brown': 'M'
    };

    // Parcourt les slots de la ligne courante
    for (let i = 1; i <= length; i++) {
        const slot = document.getElementById(`slot-${currentLine}-${i}`);
        // On suppose que le style de fond a été appliqué
        let slotColor = slot ? slot.style.backgroundColor : '';
        // Comparaison basique (attention : "red" peut se retrouver sous forme de rgb(255, 0, 0))
        // Pour simplifier, on suppose que les couleurs sont définies en tant que noms (e.g. "red")
        for (let colorKey in colorToLetter) {
            if (slotColor === colorKey) {
                combination += colorToLetter[colorKey];
                break;
            }
        }
    }
    return combination.trim();
}

// Gestion du changement de slot lors du clic sur un slot (pour définir currentSlot)
document.querySelectorAll('.slot').forEach(function (slotElement) {
    slotElement.addEventListener('click', function () {
        // Extrait le numéro du slot depuis l'ID qui est au format "slot-{line}-{slot}"
        const parts = slotElement.id.split('-');
        if (parts.length === 3) {
            currentSlot = parseInt(parts[2]);
        }
    });
});

// Au chargement de la page, restaure les couleurs de toutes les lignes déjà soumises
document.addEventListener('DOMContentLoaded', function() {
    console.log("Restoration from localStorage, currentLine:", currentLine);
    // On restaure pour toutes les lignes déjà soumises (de 1 à currentLine - 1)
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
    }

    // Mise à jour de la position de la flèche
    const arrow = document.querySelector(".arrow-container");
    if (arrow) {
        const lineHeight = 55; // Hauteur d'une ligne (slot + gap)
        // On considère que la flèche démarre en bas du board (currentLine = 1 correspond à aucune translation)
        const translationY = (currentLine-1) * lineHeight;
        (currentLine < nbr_of_line) ? arrow.style.transform = `translateY(-${translationY}px)` : arrow.style.transform = `translateY(-${(nbr_of_line-1) * lineHeight}px)`;
    }

});


function resetGame() {
    // Supprime la variable de ligne courante
    localStorage.removeItem('currentLine');

    // Récupère toutes les clés du localStorage
    Object.keys(localStorage).forEach(function(key) {
        // Si la clé commence par "slot-", on la supprime
        if (key.startsWith('slot-')) {
            localStorage.removeItem(key);
        }
    });

    // Optionnel : recharger la page pour appliquer les changements
    location.reload();
}


// Lors du clic sur le bouton de soumission, on incrémente currentLine et on sauvegarde cette valeur dans localStorage.
// Remarque : cette fonction doit être appelée via l'événement click du bouton, et le POST doit être géré par le serveur.
const combinationButton = document.getElementById("submit");
if (combinationButton) {
    combinationButton.addEventListener('click', function() {
        // Ici, avant d'envoyer le formulaire, on peut valider ou enregistrer l'état courant
        // Puis on incrémente la ligne actuelle
        currentLine++;
        localStorage.setItem('currentLine', currentLine);
        // Optionnel : réinitialiser currentSlot pour la nouvelle ligne
        currentSlot = 1;
    });
}
