// JavaScript para ocultar/mostrar el nav según el scroll
let lastScroll = 0;
const nav = document.getElementById('mainNav');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    if (currentScroll > lastScroll && currentScroll > 30) {
        // Bajando
        nav.classList.add('nav-hide');
    } else {
        // Subiendo
        nav.classList.remove('nav-hide');
    }
    lastScroll = currentScroll;
});

// Fondo dinámico difuminado en la sección hero
const heroImages = [
    'assets/images/parking1.jpeg',
    'assets/images/parking2.jpeg',
    'assets/images/parking3.jpeg',
    'assets/images/parking4.jpeg'
];
let heroIndex = 0;
const heroBg = document.getElementById('heroBg');
function setHeroBg() {
    heroBg.style.backgroundImage = `url('${heroImages[heroIndex]}')`;
}
setHeroBg();
setInterval(() => {
    heroIndex = (heroIndex + 1) % heroImages.length;
    setHeroBg();
}, 4000);
