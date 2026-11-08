// script.js (Member 1)
// Only job: open and close the navigation menu on mobile screens.

// 1. Find the menu button and the links list using their id names
const menuButton = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");

// 2. When the button is clicked, add or remove the CSS class "open".
//    style.css shows the menu only when it has the class "open".
if (menuButton && navLinks) {
  menuButton.addEventListener("click", function () {
    navLinks.classList.toggle("open");
  });
}
