/**
 * -----------------------------
 * Utility basics fonctions 
 * -----------------------------
 */

/**

/**
 * Converts a CSS color name (or any valid CSS color string) to an rgb() string.
 *
 * @param {string} color - The CSS color string (e.g., "firebrick", "#f00", "rgb(255,0,0)").
 * @returns {string} - The computed rgb() value.
 */
export function convertColorToRGB(color) {
    // Create a temporary element
    const tempElem = document.createElement("div");
    tempElem.style.color = color;
    document.body.appendChild(tempElem);
    
    // Get the computed color which will be in rgb format
    const computedColor = window.getComputedStyle(tempElem).color;
    
    // Clean up the temporary element
    document.body.removeChild(tempElem);
    
    return computedColor;
  }
  
  /**
   * Shades a color by a given percentage.
   * Supports hexadecimal, rgb() formats, and CSS color names.
   *
   * @param {string} color - The input color string.
   * @param {number} percent - The percentage to modify brightness (negative to darken).
   * @returns {string} - The shaded color in rgb() format.
   */
export function shadeColor(color, percent) {
    let r, g, b;
  
    // If the color is not in hex or rgb format, convert it (handles color names)
    if (!color.startsWith("#") && !color.startsWith("rgb")) {
      color = convertColorToRGB(color);
    }
  
    // Check for hexadecimal color format
    if (color.startsWith("#")) {
      let hex = color.slice(1);
  
      // Handle shorthand hex format (#RGB)
      if (hex.length === 3) {
        hex = hex.split("").map(char => char + char).join("");
      }
  
      // Convert hex to decimal values
      r = parseInt(hex.substring(0, 2), 16);
      g = parseInt(hex.substring(2, 4), 16);
      b = parseInt(hex.substring(4, 6), 16);
    }
    // Check for rgb() format
    else if (color.startsWith("rgb")) {
      let rgbValues = color.match(/\d+/g).map(Number);
      [r, g, b] = rgbValues;
    } else {
      console.error("Unsupported color format:", color);
      return color; // Return original color if format is invalid
    }
  
    // Modify each color component based on the percentage
    r = Math.min(255, Math.max(0, r + (r * percent) / 100));
    g = Math.min(255, Math.max(0, g + (g * percent) / 100));
    b = Math.min(255, Math.max(0, b + (b * percent) / 100));
  
    return `rgb(${Math.round(r)}, ${Math.round(g)}, ${Math.round(b)})`;
  }
  

/**
 * Fills a slot with a given color.
 * Applies a darker shade for a gradient effect and marks the slot as filled.
 * 
 * @param {HTMLElement} slotElement - The slot element to fill.
 * @param {string} color - The color to apply.
 */
export function fillSlot(slotElement, color, onload = false) {
  // Calculate a darker shade for gradient effect
  const darkerColor = shadeColor(color, -20);

  // Dynamically apply the color and its darker variant as CSS properties
  slotElement.style.setProperty("--slot-color", color);
  slotElement.style.setProperty("--slot-color-dark", darkerColor);

  // Add a class to indicate that the slot is filled
  if (onload){
    slotElement.classList.add("onload");
  } else{
    slotElement.classList.add('filled');
  }
}

export function updateArrow(currentLine){
  // Adjust the arrow indicator's position based on the current line
  const arrow = document.querySelector(".arrow-container");
  if (arrow) {
    const lineHeight = 67;
    const translationY = (currentLine - 1) * lineHeight;
    arrow.style.transform = `translateY(-${Math.min(translationY, (nbr_of_line - 1) * lineHeight)}px)`;
  }
}