// Récupère ou initialise le numéro de la ligne courante depuis localStorage
let currentLine = localStorage.getItem('currentLine') ? parseInt(localStorage.getItem('currentLine')) : 1;
let currentSlot = 1;  // Slot actuellement sélectionné


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

// Au chargement de la page, restaure les couleurs de toutes les lignes déjà soumises
document.addEventListener('DOMContentLoaded', function() {
    // console.log("Restoration from localStorage, currentLine:", currentLine);
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

// Déclenché au début du drag and drop 
function handleDragStart(event) {
    // On envoie le nom de la couleur; ici on suppose que la classe contient le nom de la couleur
    // Si votre élément a plusieurs classes, vous pouvez utiliser event.target.classList pour sélectionner la bonne
    event.dataTransfer.setData("text/plain", event.target.classList[1]); 
}

// Attacher l'événement sur toutes les options de couleur
document.querySelectorAll('.color-option').forEach(function(colorElement) {
    colorElement.addEventListener('dragstart', handleDragStart);
});

// Fonction pour autoriser le drop sur un slot
function handleDragOver(event) {
    event.preventDefault(); // Nécessaire pour autoriser le drop
}

// Gestionnaire de l'événement dragover (pour autoriser le drop)
function handleDragOver(event) {
    const slot = event.currentTarget;
    // Extraction du numéro de ligne depuis l'id (format "slot-{line}-{number}")
    const parts = slot.id.split('-');
    const slotLine = parseInt(parts[1]);
    // Si le slot n'appartient pas à la ligne courante, on n'autorise pas le drop
    if (slotLine !== currentLine) {
        return;
    }
    event.preventDefault(); // Nécessaire pour permettre le drop
}

// Gestionnaire de l'événement drop
function handleDrop(event) {
    const slot = event.currentTarget;
    const parts = slot.id.split('-');
    const slotLine = parseInt(parts[1]);
    // Vérifie que le drop se fait sur un slot de la currentLine
    if (slotLine !== currentLine) {
        console.error("Drop interdit sur une ligne inactive.");
        return;
    }
    event.preventDefault();
    const color = event.dataTransfer.getData("text/plain");
    // console.log("Dropped color:", color);
    if (color) {
        // Appliquer la couleur et lancer l'animation
        slot.style.backgroundColor = color;
        slot.classList.remove("animate-drop");
        // Forcer le reflow pour redémarrer l'animation
        void slot.offsetWidth;
        slot.classList.add("animate-drop");

        // Sauvegarde en localStorage et mise à jour de la combinaison
        localStorage.setItem(slot.id, color);
        document.getElementById("combination").value = getCombination();
    }
}

// Attacher les événements sur chaque slot
document.querySelectorAll('.slot').forEach(function(slotElement) {
    slotElement.addEventListener('dragover', handleDragOver);
    slotElement.addEventListener('drop', handleDrop);
});
