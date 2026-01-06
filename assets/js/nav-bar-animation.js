document.addEventListener('DOMContentLoaded', function () {
    "use strict";

    // --- Configuration ---
    const SCROLL_DISTANCE = 100; // Pixels to scroll before the color changes
    const mainNav = document.getElementById('nav-bar');
    
    // Performance flag to control scroll function execution rate
    let isScrolling = false; 
    
    // Exit if the navbar element isn't found
    if (!mainNav) {
        return;
    }

    // --- Core Logic: Function to handle class toggling based on scroll position ---
    const navbarSolidify = function () {
        const currentScrollY = window.scrollY;
        
        // 1. Check Scroll Position
        if (currentScrollY === 0) {
            // At the very top: Make transparent
            mainNav.classList.remove('bg-dark', 'navbar-scrolled');
            mainNav.classList.add('navbar-transparent');
        } else if (currentScrollY > SCROLL_DISTANCE) {
            // Scrolled down: Make solid (bg-dark)
            mainNav.classList.remove('navbar-transparent');
            mainNav.classList.add('bg-dark', 'navbar-scrolled');
        } else {
             // Between 0 and SCROLL_DISTANCE: Maintain transparency
             mainNav.classList.remove('bg-dark', 'navbar-scrolled');
             mainNav.classList.add('navbar-transparent');
        }

        // Reset the flag after the function runs
        isScrolling = false; 
    };

    // --- Performance Optimization (Throttling) ---
    const scrollHandler = function () {
        // Only run the logic if the flag is false
        if (!isScrolling) {
        isScrolling = true;
        // Schedule the heavy work (navbarSolidify) to run after 250ms
        window.requestAnimationFrame(navbarSolidify);
        // Note: requestAnimationFrame is generally better than setTimeout for smooth animation/scroll
        }
    };

    // --- Mobile/Toggle Fix ---
    const navToggler = document.querySelector('.navbar-toggler');
    if (navToggler) {
        navToggler.addEventListener('click', function() {
            // Force solid background when the toggler is clicked (i.e., menu opens on mobile)
            if (mainNav.classList.contains('navbar-transparent')) {
                mainNav.classList.add('bg-dark', 'navbar-scrolled');
                mainNav.classList.remove('navbar-transparent');
            }
        });
    }

    // --- Event Listeners ---
    
    // 1. Run the function immediately on load to set the initial state
    navbarSolidify();

    // 2. Attach the optimized scroll handler to the window scroll event

    window.addEventListener('scroll', scrollHandler);
});