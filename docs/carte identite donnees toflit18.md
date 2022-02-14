---
title: Réalisation d'une carte d'identité des données de la base Toflit18
date: 2022-01-26
author: Guillaume Brioudes <https://myllaume.fr/>
---

Réalisation d'une série de visualisations pour explorer les données de la base Toflit18.

# Lancement

```
sh install.sh
npm start
```

Se rendre à http://127.0.0.1:8080/Product.html.

# Mise en œuvre

Fichiers :

- Corps de page `/src/product.njk`
- Script (aggrégation des données) `/scripts/product.py`
- Script (visualisation) `/src/static/js/product.js`
- Données `/data/toflit18_all`

Avec Vega-Lite :

- Histogrammes
    - dates (1787 et 1789)
    - directions (import depuis Dunkerque et export vers Dunkerque)
    - localisation de l'enregistrement (bureau de ferme et direction de ferme)
- Matrices
    - dates (1787 et 1789)
    - directions (import depuis Dunkerque et export vers Dunkerque)
    - localisation de l'enregistrement (bureau de ferme et direction de ferme)
    - classification des produits (`product_simplification` et `product_revolutionempire`)

# Selection des viz

```js
Array.from(document.querySelectorAll('svg')).forEach(viz => {
    const parent = viz.parentNode;
    let title = viz.querySelector('.role-title-text')
    if (!title) {
        return
    }
    title = title.textContent
    parent.insertAdjacentHTML('afterbegin', `<span>${title}</span>`)
})
```