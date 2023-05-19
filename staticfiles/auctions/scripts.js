const form = document.getElementById("search_form");
const input = document.getElementById("search_input");

input.addEventListener('keyup', function(event) {
if (event.keyCode === 13) {
    event.preventDefault();
    form.submit();
    }
});

function scrollToTarget() {
  document.getElementById("scrollTarget").scrollIntoView({ behavior: 'smooth' });
}


const registerButton = document.getElementById("register");
const loginButton = document.getElementById("login");
const container = document.getElementById("LR_container");

registerButton.addEventListener("click", () => {
  container.classList.add("right-panel-active");
});
loginButton.addEventListener("click", () => {
  container.classList.remove("right-panel-active");
});