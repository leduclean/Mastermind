/**
 * -----------------------------
 * Global Variables Initialization
 * -----------------------------
 */
let currentLine = localStorage.getItem("currentLine")
  ? parseInt(localStorage.getItem("currentLine"))
  : 1;

// Note: The following variables (length, cplaced, iplaced, nbr_of_line, solution)
// are assumed to be defined elsewhere in your application.

import {
  fillSlot,
  updateArrow,
  displayLoose,
  displayWin,
  resetPopup,
} from "./basics.js";

/**
 * -----------------------------
 * Game Functions
 * -----------------------------
 */

/**
 * Updates the evaluation slots for a given line.
 * Red slots indicate correct placement and white slots indicate misplaced colors.
 *
 * @param {number} line - The line number to update.
 * @param {number} cplaced - Number of correctly placed colors.
 * @param {number} iplaced - Number of misplaced colors.
 */
function updateEvaluationSlots(line, cplaced, iplaced) {
  let slots = document.querySelectorAll(
    `.evaluation-area-${line} .evaluation-slot`,
  );
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

/**
 * Resets the game by clearing all data from local storage.
 */

/**
 *
 *
 * Generates the combination string based on the current line's filled slots.
 * It maps each slot's background color to a letter defined in colorToLetter.
 *
 * @returns {string} - The combination string.
 */
function getCombination() {
  let combination = "";
  const colorToLetter = {
    firebrick: "R",
    royalblue: "B",
    limegreen: "V",
    yellow: "J",
    darkorange: "O",
    black: "N",
    sienna: "M",
    gray: "G",
  };

  // Iterate through each slot in the current line
  for (let i = 1; i <= length; i++) {
    const slot = document.getElementById(`slot-${currentLine}-${i}`);
    let slotColor = slot
      ? window.getComputedStyle(slot).getPropertyValue("--slot-color")
      : "";
    console.log(slotColor);

    // Map the slot color to its corresponding letter
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

/**
 * -----------------------------
 * Drag & Drop Event Handlers
 * -----------------------------
 */

/**
 * Handles the drag start event for color options.
 * Stores the dragged color value in the data transfer object.
 *
 * @param {DragEvent} event - The dragstart event.
 */
function handleDragStart(event) {
  event.dataTransfer.setData(
    "text/plain",
    event.target.getAttribute("data-color"),
  );
}

/**
 * Handles the drag over event on a slot.
 * Allows drop only if the slot belongs to the current active line.
 *
 * @param {DragEvent} event - The dragover event.
 */
function handleDragOver(event) {
  const slot = event.currentTarget;
  const parts = slot.id.split("-");
  const slotLine = parseInt(parts[1]);

  // Allow drop only on the current active line
  if (slotLine !== currentLine) {
    return;
  }
  event.preventDefault();
}

/**
 * Handles the drop event on a slot.
 * Fills the slot with the dragged color, updates local storage, and refreshes the combination.
 *
 * @param {DragEvent} event - The drop event.
 */
function handleDrop(event) {
  const slot = event.currentTarget;
  const parts = slot.id.split("-");
  const slotLine = parseInt(parts[1]);

  // Prevent dropping if the slot is not in the current active line
  if (slotLine !== currentLine) {
    console.error("Drop not allowed on an inactive line.");
    return;
  }
  event.preventDefault();

  const color = event.dataTransfer.getData("text/plain");
  if (color) {
    fillSlot(slot, color);
    localStorage.setItem(slot.id, color);
    // Update the combination input field with the current combination
    document.getElementById("combination").value = getCombination();
    console.log(document.getElementById("combination").value);
  }
}

/**
 * -----------------------------
 * Event Listeners & Initialization
 * -----------------------------
 */

// Add event listener to the submit button to progress to the next line
const combinationButton = document.getElementById("submit");
if (combinationButton) {
  combinationButton.addEventListener("click", function () {
    currentLine++;
    localStorage.setItem("currentLine", currentLine);
  });
}

// Add dragstart listener to all color option elements
document.querySelectorAll(".color-option").forEach(function (colorElement) {
  colorElement.addEventListener("dragstart", handleDragStart);
});

// Add dragover and drop listeners to all slot elements
document.querySelectorAll(".slot").forEach(function (slotElement) {
  slotElement.addEventListener("dragover", handleDragOver);
  slotElement.addEventListener("drop", handleDrop);
});

/**
 * DOMContentLoaded event handler.
 * Restores the game state from local storage and updates UI elements.
 */
document.addEventListener("DOMContentLoaded", function () {
  const params = new URLSearchParams(window.location.search);

  if (params.get("reset") === "true") {
    // Supprimer le paramètre reset avant de recharger la page
    removeResetParam();

    // Attendre un petit délai avant le rechargement
    setTimeout(() => {
      resetGame();
    }, 100); // Petit délai pour éviter une boucle infinie
  }
});

// Vérifier dans le sessionStorage
if (sessionStorage.getItem("popreset") === "true") {
  resetPopup();
  console.log("resetpop");
  // Supprimer le flag pour éviter de réafficher le popup lors d'autres rechargements
  sessionStorage.removeItem("popreset");
  cplaced = 0;
}

if (error) {
  // if there is an error, we don't go through and we stay to the current line
  currentLine--;
  localStorage.setItem("currentLine", currentLine);
}
if (cplaced == length) {
  displayWin(currentLine - 1);
}
if (currentLine > nbr_of_line) {
  displayLoose();
}

// Update evaluation slots for the previous line
updateEvaluationSlots(currentLine - 1, cplaced, iplaced);

// Restore filled slots for each completed line
for (let line = 1; line < currentLine; line++) {
  for (let slot = 1; slot <= length; slot++) {
    const slotKey = `slot-${line}-${slot}`;
    const savedColor = localStorage.getItem(slotKey);
    if (savedColor) {
      const slotElement = document.getElementById(slotKey);
      if (slotElement) {
        fillSlot(slotElement, savedColor, true);
      }
    }
  }

  // Restore evaluation slot colors for this line
  let evalSlots = document.querySelectorAll(
    `.evaluation-area-${line} .evaluation-slot`,
  );
  evalSlots.forEach((slot, index) => {
    let savedColor = localStorage.getItem(`evaluation-slot-${line}-${index}`);
    if (savedColor) {
      slot.style.backgroundColor = savedColor;
    }
  });
}

updateArrow(currentLine);

function resetGame() {
  sessionStorage.setItem("popreset", "true");
  localStorage.clear();
  console.log("clear");
  location.reload();
}
/**
 * Removes the "reset" parameter from the URL without reloading the page.
 */
function removeResetParam() {
  const url = new URL(window.location);
  url.searchParams.delete("reset");
  window.history.replaceState({}, document.title, url.toString());
}

window.resetGame = resetGame;
