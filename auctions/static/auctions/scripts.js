// Get the dropdown button element
const dropdownButton = document.querySelector('.dropdown-toggle');
  
// Get the dropdown menu items
const dropdownItems = document.querySelectorAll('.dropdown-item');

// Loop through the dropdown menu items and add a click event listener to each one
dropdownItems.forEach(item => {
  item.addEventListener('click', () => {
    // Update the title of the dropdown button with the selected option
    dropdownButton.textContent = item.textContent;
  });
});