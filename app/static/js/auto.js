// Vérifie que le script est chargé
console.log("auto.js chargé !");

// Vérifie que la variable attempts est bien définie
console.log("attempts:", attempts);

// Variables globales
let currentAttempt = 1;
let totalAttempts = attempts.length;
const letterToColor = {
    'R': 'red',    // Rouge
    'B': 'blue',   // Bleu
    'V': 'green',  // Vert
    'J': 'yellow', // Jaune
    'N': 'black',  // Noir
    'G': 'grey',   // Gris
    'O': 'orange', // Orange
    'M': 'brown',  // Marron
};

// Fonction pour afficher les tentatives successives
function displayNextAttempt() {
    console.log("displayNextAttempt appelée, currentAttempt:", currentAttempt);

    // Vérifier que nous avons encore des tentatives à traiter
    if (currentAttempt < totalAttempts) {
        // Récupérer l'essai actuel de la liste `attempts`
        var attemptStr = attempts[currentAttempt];
        console.log("Traitement de l'essai:", attemptStr);

        // Vérifier que la structure de l'essai correspond au format attendu
        var match = attemptStr.match(/Essai (\d+) : ([A-Z]+) \((\d+) bien placées, (\d+) mal placées\)/);

        // Si l'essai correspond au format, extraire les données
        if (match) {
            console.log("Regex matchée:", match);

            var attemptNum = parseInt(match[1]);  // Numéro de l'essai
            var combination = match[2];            // Combinaison testée
            var cplaced = parseInt(match[3]);     // Nombre de bien placés
            var iplaced = parseInt(match[4]);     // Nombre de mal placés

            // Mettre à jour les plots avec les couleurs de la combinaison testée
            for (let i = 0; i < combination.length; i++) {
                var slot = document.getElementById(`slot-${currentAttempt}-${i + 1}`);
                console.log(slot)
                if (slot) {
                    console.log(`Mise à jour du slot${i + 1} avec la couleur`, combination[i]);
                    slot.style.backgroundColor = letterToColor[combination[i]];
                }
            }

            // Afficher l'évaluation de l'essai (bien placés et mal placés)
            var evalContainer = document.getElementById("evaluation");
            if (!evalContainer) {
                evalContainer = document.createElement("p");
                evalContainer.id = "evaluation";
                document.body.appendChild(evalContainer);
            }
            evalContainer.innerHTML = `Essai ${attemptNum}: ${cplaced} bien placés, ${iplaced} mal placés`;

            // Passer à l'essai suivant après un délai
            currentAttempt++;
            setTimeout(displayNextAttempt, 3000);  // Attente de 1 seconde avant de passer à l'essai suivant
        } else {
            evalContainer.innerHTML = `${attempts[-1]}`;
        }
    } else {
        console.log("Fin des tentatives");
    }
}

// Déclencher l'affichage des tentatives après le chargement de la page
window.onload = function() {
    console.log("window.onload appelé");
    if (attempts.length > 0) {
        setTimeout(displayNextAttempt, 1000);  // Démarrer après 1 seconde
    } else {
        console.warn("Aucune tentative disponible dans attempts.");
    }
};
