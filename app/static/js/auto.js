
import { fillSlot } from './basics.js';
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

// Fonction pour mettre à jour les evaluation-slot



    /* Updates the evaluation slots for a given line.
  * Red slots indicate correct placement and white slots indicate misplaced colors.
  * 
  * @param { number } line - The line number to update.
  * @param { number } cplaced - Number of correctly placed colors.
  * @param { number } iplaced - Number of misplaced colors.
  */
function updateEvaluationSlots(line, cplaced, iplaced) {
    let slots = document.querySelectorAll(`.evaluation-area-${line} .evaluation-slot`);
    let index = 0;

    // Met à jour les slots pour les couleurs bien placées
    for (let i = 0; i < cplaced; i++) {
        if (index < slots.length) {
            slots[index].style.backgroundColor = "red";
            localStorage.setItem(`evaluation-slot-${line}-${index}`, "red");
            index++;
        }
    }

    // Met à jour les slots pour les couleurs mal placées
    for (let i = 0; i < iplaced; i++) {
        if (index < slots.length) {
            slots[index].style.backgroundColor = "white";
            localStorage.setItem(`evaluation-slot-${line}-${index}`, "white");
            index++;
        }
    }
}
// Fonction pour afficher les tentatives successives
function displayNextAttempt() {
    console.log("displayNextAttempt appelée, currentAttempt:", currentAttempt);

    // Vérifier que nous avons encore des tentatives à traiter
    if (currentAttempt <= totalAttempts) {
        // Récupérer l'essai actuel de la liste `attempts`
        let to_extract = attempts[currentAttempt - 1];
        let combination = to_extract[0]
        let cplaced = parseInt(to_extract[1][0]);    // Nombre de bien placés
        let iplaced = parseInt(to_extract[1][2]);    // Nombre de mal placés
        console.log(combination, cplaced, iplaced);

        // Mettre à jour les plots avec les couleurs de la combinaison testée
        for (let i = 0; i < combination.length; i++) {
            let slot = document.getElementById(`slot-${currentAttempt}-${i + 1}`);
            if (slot) {
                let color = letterToColor[combination[i]];
                fillSlot(slot, color);
                localStorage.setItem(slot, color);
            } else {
                console.warn(`Slot slot-${currentAttempt}-${i + 1} introuvable`);
            }
        }

        // Mettre à jour les slots d'évaluation
        updateEvaluationSlots(currentAttempt , cplaced, iplaced);

        // Mettre à jour la position de la flèche
        const arrow = document.querySelector(".arrow-container");
        if (arrow) {
            const lineHeight = 65; // Hauteur d'une ligne (slot + gap)
            const translationY = (currentAttempt - 1) * lineHeight;
            arrow.style.transform = `translateY(-${Math.min(translationY, (totalAttempts - 1) * lineHeight)}px)`;
        }



        for (let i = 0; i < combination.length; i++) {
            let slot = document.getElementById(`slot-${currentAttempt - 1}-${i + 1}`);
            if (slot) {
                slot.classList.add("onload");
                slot.classList.remove("filled");
            }
        }
        let slots = document.querySelectorAll(`.evaluation-area-${currentAttempt} .evaluation-slot`);
        slots.forEach((slot, index) => {
            let savedColor = localStorage.getItem(`evaluation-slot-${currentAttempt}-${index}`);
            if (savedColor) {
                fillSlot(slot, savedColor, true)
                console.log('random')
            }
        });

        // Passer à l'essai suivant après un délai
        currentAttempt++;
        setTimeout(displayNextAttempt, 3000);
    }
}

function removeResetParam() {
    const url = new URL(window.location);
    url.searchParams.delete('reset');  // Retire le paramètre run_js
    window.history.replaceState({}, document.title, url.toString());  // Met à jour l'URL sans recharger la page
}
// Déclencher l'affichage des tentatives après le chargement de la page
window.onload = function () {
    console.log("window.onload appelé");
    if (attempts.length > 0) {
        setTimeout(displayNextAttempt, 1000);
    } else {
        console.warn("Aucune tentative disponible dans attempts.");
    }
    const params = new URLSearchParams(window.location.search);
    if (params.get('reset') === 'true') {
        localStorage.clear();
        removeResetParam();  // Retire le paramètre de l'URL
    }
};


