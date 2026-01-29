---
title: "A Hybrid Scheme for Fuzzy Dark Matter Simulations Combining the Schrödinger and Hamilton–Jacobi–Madelung Equations"
tags: ["FDM"]
image: "/assets/img/kunkel2025.webp"
date: 2025-07-22
link: "https://iopscience.iop.org/article/10.3847/1538-4365/addc59"
link_text: "Kunkel et al., Astrophys. J. Suppl. Ser. 279, 39 (2025)"
---
The short de Broglie wavelength and rapid oscillations associated with high-velocity flows pose a significant challenge for fuzzy dark matter (FDM) simulations, especially for larger FDM particle mass. To address this limitation, we develop a hybrid numerical scheme in GAMER that integrates the wave-based Schrödinger–Poisson formulation with the fluid-based Hamilton–Jacobi–Madelung equations. This approach uses efficient fluid solvers on large, smooth scales while employing wave solvers on refined grids to capture interference patterns and solitonic structures with high accuracy. The wave solver incorporates a novel local pseudo-spectral method based on Fourier continuations with discrete Gram polynomials, together with a robust boundary-matching algorithm that ensures smooth reconstruction of the wave function across fluid–wave interfaces. This hybrid scheme substantially extends the feasible volume of FDM cosmological simulations.