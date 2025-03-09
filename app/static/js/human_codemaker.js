// Récupère la combinaison en lisant les slots
function getCombination() {
    let combination = '';
    const colorToLetter = {
        'red': 'R', 'blue': 'B', 'green': 'V', 'yellow': 'J',
        'black': 'N', 'grey': 'G', 'orange': 'O', 'brown': 'M'
    };

    // On parcourt tous les slots
    document.querySelectorAll('.slot').forEach(function(slot) {
        // On lit la couleur définie en inline style
        let slotColor = slot.style.backgroundColor;
        // Vérifier si slotColor correspond à l'un des noms attendus
        for (let colorKey in colorToLetter) {
            if (slotColor === colorKey) {
                combination += colorToLetter[colorKey];
                break;
            }
        }
    });
    console.log(combination.trim());
    return combination.trim();
}

// Démarrage du drag : on récupère la couleur via data-color
function handleDragStart(event) {
    // Récupère la couleur à partir de l'attribut data-color
    const color = event.target.getAttribute('data-color');
    event.dataTransfer.setData("text/plain", color);
}

// Ajout de l'écouteur sur les options de couleur
document.querySelectorAll('.color-option').forEach(function(colorElement) {
    colorElement.addEventListener('dragstart', handleDragStart);
});

// Permettre le drop en annulant le comportement par défaut
function handleDragOver(event) {
    event.preventDefault(); // Obligatoire pour permettre le drop
}

// Gestion du drop sur un slot
function handleDrop(event) {
    event.preventDefault();
    const slot = event.currentTarget;
    const color = event.dataTransfer.getData("text/plain");
    
    if (color) {
        slot.style.backgroundColor = color;
        slot.classList.remove("animate-drop");
        // Forcer le reflow pour redémarrer l'animation
        void slot.offsetWidth;
        slot.classList.add("animate-drop");
        document.getElementById("solution").value = getCombination();
    }
}

// Ajout des écouteurs sur les slots
document.querySelectorAll('.slot').forEach(function(slotElement) {
    slotElement.addEventListener('dragover', handleDragOver);
    slotElement.addEventListener('drop', handleDrop);
});
