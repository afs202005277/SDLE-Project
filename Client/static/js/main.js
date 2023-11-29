particlesJS.load('particles-js', '../static/config/particles.json', function() {
    console.log('particles.js loaded - callback');
  });

window.addEventListener("DOMContentLoaded", function () {
  const loader = document.querySelector(".loader");
  const overlay = this.document.querySelector(".overlay");
  setTimeout(() => {
    overlay.style.opacity = 0;
    overlay.style.visibility = 'hidden';
    loader.style.opacity = 0;
    loader.style.visibility = 'hidden';
  }, 500);
  window.addEventListener("beforeunload", function () {
    overlay.style.opacity = 1;
    overlay.style.visibility = 'visible';
    loader.style.opacity = 1;
    loader.style.visibility = 'visible';
  });
},);

const iconDiv = document.querySelector('#passwordInput > div')
const input = document.querySelector('#passwordInput > input')

if (iconDiv && input) {
  iconDiv.addEventListener('click', function() {
    const passwordIcon = iconDiv.children[0]
    const type = input.getAttribute('type')
    if (type == 'password') {
      input.setAttribute('type', 'text')
      passwordIcon.classList.replace('fa-eye', 'fa-eye-slash')
    }
    else {
      input.setAttribute('type', 'password')
      passwordIcon.classList.replace('fa-eye-slash', 'fa-eye')
    }
  })  
}