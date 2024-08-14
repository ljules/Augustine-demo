/*
Gestion de la barre de navigation & du carrousel :
--------------------------------------------------
*/

document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.navbar');
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('#navbarNav');
    const toggleNav = document.getElementById('toggle-nav');
    const topCarrousel = document.getElementById('topCarrousel');
    const content = document.querySelector('.main-content'); // Remplace par la classe de ton contenu
    const secondHeader = document.querySelector('.second-header');

    // Fonction pour mettre à jour l'affichage de la navbar
    function updateNavbar() {
        if (topCarrousel.style.display === 'none') {
            navbar.classList.remove('navbar-transparent');
            navbar.classList.add('navbar-opaque');
        } else {
            if (window.scrollY > 50) {
                navbar.classList.remove('navbar-transparent');
                navbar.classList.add('navbar-opaque');
            } else if (!navbarCollapse.classList.contains('show')) {
                navbar.classList.remove('navbar-opaque');
                navbar.classList.add('navbar-transparent');
            }
        }
    }

    // Fonction pour ajuster le padding-top du contenu
    function adjustContentPadding() {
        const navbarHeight = navbar.offsetHeight + 25;
        if (topCarrousel.style.display === 'none') {
            content.style.paddingTop = navbarHeight + 'px';
        } else {
            content.style.paddingTop = '0px'; // Réinitialise le padding si le carrousel est visible
        }
    }

    // Fonction pour mettre à jour la position du second header
    function updateSecondHeaderPosition() {
        const firstHeaderHeight = navbar.offsetHeight;
        const headCarouselHeight = topCarrousel.style.display === 'none' ? 0 : topCarrousel.offsetHeight;
        const trigHeight = headCarouselHeight - firstHeaderHeight;
        const scrollTop = window.scrollY;

        if (scrollTop >= trigHeight) {
            secondHeader.classList.add('fixed-second-header');
            secondHeader.style.top = firstHeaderHeight + 'px';
        } else {
            secondHeader.classList.remove('fixed-second-header');
            secondHeader.style.top = headCarouselHeight ? '0px' : firstHeaderHeight + 'px';
        }
    }

    // Récupérer l'état du carrousel depuis le localStorage au chargement
    const carrouselState = localStorage.getItem('carrouselState');
    if (carrouselState === 'hidden') {
        topCarrousel.style.display = 'none';
    } else {
        topCarrousel.style.display = 'block';
    }

    // Initialisation du padding et mise à jour de l'affichage
    adjustContentPadding();
    updateSecondHeaderPosition();
    updateNavbar();

    // Événements
    window.addEventListener('scroll', function() {
        updateNavbar();
        updateSecondHeaderPosition();
    });

    window.addEventListener('resize', adjustContentPadding);

    if (toggleNav) {
        toggleNav.addEventListener('click', function() {
            const isHidden = topCarrousel.style.display === 'none' || window.getComputedStyle(topCarrousel).display === 'none';
            
            if (isHidden) {
                topCarrousel.style.display = 'block';
                localStorage.setItem('carrouselState', 'visible');
            } else {
                topCarrousel.style.display = 'none';
                localStorage.setItem('carrouselState', 'hidden');
            }
            updateSecondHeaderPosition();
            updateNavbar();
            adjustContentPadding();
        });
    }
});





// Gestion de l'attribut aria-current et classe active pour la barre de navigation :
// ---------------------------------------------------------------------------------

document.addEventListener('DOMContentLoaded', function () {
    const navLinks = document.querySelectorAll('nav a');
    const currentURL = window.location.pathname;

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentURL) {
            const parent = link.closest('.dropdown');
            if (parent) {
                // Si le lien fait partie d'un dropdown, appliquer les modifications au parent
                parent.querySelector('a').classList.add('active');
                parent.querySelector('a').setAttribute('aria-current', 'page');
            } else {
                // Sinon, appliquer les modifications directement au lien
                link.classList.add('active');
                link.setAttribute('aria-current', 'page');
            }
        }
    });
});



