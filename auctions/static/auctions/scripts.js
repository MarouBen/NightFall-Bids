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

  