---
layout: about
title: home
permalink: /
role: Cosmologist
affiliation: Gran Sasso Science Institute
affiliation_url: https://www.gssi.it/
hero_image: background.jpg # full-width photograph in assets/img/
hero_text: dark # colour of the text on the photograph: dark (bright photo) or light (dark photo)
photo: profile_pic.jpeg # portrait in assets/img/
bio_title: Hello there!

# "My research topics": one block per topic.
# left half:  image and/or formula (LaTeX), with captions
# right half: title, text, links
# below:      media, one or two plots or videos (a video needs a poster, its still picture),
#             and media_caption, a line under all of them
# Files are in assets/research/. Markdown and $$formulas$$ work in text and captions.
research_title: My research topics
research_image: planck-polarisation.jpg # background of the title band
research_credit: "© ESA and the Planck Collaboration" # under the band
research:
  - title: Multi-messenger cosmology
    formula: >-
      \begin{gathered} d_L(z) = c\,(1+z) \int_0^z \frac{dz'}{H(z')} \\[0.6em]
      H^2(z) = H_0^2 \left[ \Omega_{\rm m} (1+z)^3 + (1-\Omega_{\rm m})\, f_{\rm DE}(z) \right] \end{gathered}
    caption: >-
      Gravitational waves give the distance $$d_L$$ and light gives the redshift $$z$$: what remains is $$f_{\rm DE}$$.
    text: >-
      When two neutron stars merge and we catch both the gravitational waves and the gamma-ray burst,
      we get a distance and a redshift at once, and I use them to find out how dark energy evolves
      without assuming a model for it.
    links:
      - { name: My code, url: "https://github.com/AndreaCozzumbo/bright_cosmology/tree/main/code" }
      - { name: Tutorial, url: "https://github.com/samueleronchini/acme_tutorials/tree/main/cosmo_tutorial" }
    media:
      - file: fde-reconstruction.png
        alt: Dark energy density and expansion rate as functions of redshift, reconstructed from simulated Einstein Telescope data, DESI data and both together
        caption: >-
          $$f_{\rm DE}(z)$$ and $$H(z)$$ reconstructed from simulated data of the Einstein Telescope, DESI and the two together.
          The injected dark energy is the red line. From [our paper](https://arxiv.org/abs/2411.02490).

  - title: Modified gravity
    formula: >-
      S = \int d^4x\, \sqrt{-g}\, \sum_{i=2}^{5} \mathcal{L}_i\left[\varphi, g_{\mu\nu}\right] + S_{\rm m}
    caption: Horndeski theories, the most general scalar-tensor theories with second-order equations of motion.
    text: >-
      If dark energy really crosses $$w=-1$$, as recent data hint, the simplest scalar field is not enough,
      so I look for theories of gravity beyond Einstein's that can do it and I test them
      on the data with a Boltzmann solver ([CLASS](http://class-code.net/)).
    media:
      - file: bss-evolution.mp4
        poster: bss-evolution.jpg
        alt: Animation of a scalar field from the early Universe to today, with its potential, its energy budget and its equation of state
        caption: >-
          A broken-shift-symmetric Galileon ghost condensate, from the early Universe to today:
          its equation of state goes below $$-1$$ and crosses back at $$z \simeq 0.83$$.

  - title: Neutrinos and cosmological anomalies
    image: planck-lensing-map.webp
    alt: Full-sky map of the gravitational lensing of the cosmic microwave background measured by Planck
    image_caption: The CMB lensing map measured by Planck (2018). ESA and the Planck Collaboration.
    text: >-
      Cosmological data, taken at face value, seem to like neutrinos with a *negative* mass:
      I study how this odd preference is tied to an anomaly in the gravitational lensing of the cosmic microwave background.
    media:
      - file: lensing-neutrinos.png
        alt: Power spectrum of the CMB lensing potential for total neutrino masses between 0.02 and 0.30 eV
        caption: A larger neutrino mass means less lensing.
      - file: lensing-alens.png
        alt: Power spectrum of the CMB lensing potential for lensing amplitudes between 0.95 and 1.18
        caption: A larger $$A_{\rm lens}^{\phi\phi}$$ means more lensing, so the two can be confused.
    media_caption: "The effective neutrino mass once the lensing anomaly is accounted for: see [our paper](https://arxiv.org/abs/2511.01967)."
---

I'm Andrea. I'm a researcher, a cosmologist to be precise, and I've just finished my PhD in astroparticle physics at the [Gran Sasso Science Institute](https://www.gssi.it/).

My research is mainly about the nature of **dark energy**: what is making the Universe expand faster and faster? Is it really a constant, does it change with time, or is it gravity that we haven't fully understood?

A new way to investigate what dark energy could be is with gravitational waves! I'm a member of [LIGO–Virgo–KAGRA](https://ligo.org/), which detects them from merging black holes and neutron stars, and of the [Einstein Telescope](https://www.einstein-telescope.it/en/), the detector that will hear much farther in the future.

Curious? My papers are in [Publications]({{ '/publications/' | relative_url }}).

**And when I'm not doing physics I'm probably around with a film camera: [here]({{ '/photography/' | relative_url }}) you can find some of my shots.**
