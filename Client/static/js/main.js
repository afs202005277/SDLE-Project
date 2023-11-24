particlesJS.load('particles-js', '../static/config/particles.json', function() {
    console.log('particles.js loaded - callback');
  });

window.addEventListener("DOMContentLoaded", function () {
  const loader = document.querySelector(".loader");
  const overlay = this.document.querySelector(".overlay");
  overlay.style.opacity = 0;
  overlay.style.visibility = 'hidden';
  loader.style.opacity = 0;
  loader.style.visibility = 'hidden';

  window.addEventListener("beforeunload", function () {
    overlay.style.opacity = 1;
    overlay.style.visibility = 'visible';
    loader.style.opacity = 1;
    loader.style.visibility = 'visible';
  });
});