---
title: Réalisation d'une carte d'identité des données de la base Toflit18
date: 2022-02-14
author: Guillaume Brioudes <https://myllaume.fr/>
---

# Noeuds

Réaliser des graphes pour indiquer quels sont les

- villes
- bureaux de ferme
- directions de ferme
- provinces
- amirautés

reliées à Dunquerque en tant que

- ville (Dunkerque)
- bureau de ferme (Dunkerque)
- direction de ferme (Lille)
- province (Flandres)
- amirauté (Dunkerque).

# Liens

Les liens entre ces repères peuvent varier en

- couleur
- tracé

selon

- le tonnage
- l'objet de voyage

des bateaux naviguant entre les repères.

On pourrait même imaginé représenter le tonnage des bateaux entrants et celui des bateaux sortants.

# Observations

Tant que `homeport === 'Dunquerque'` :

- `pointcall_admiralty === Dunkerque`
- `pointcall_province === Flandre`
- `ferme_bureau === Dunkerque`
- `ferme_direction === Lille`

La variables `homeport`, `homeport_admiralty`, `homeport_province`, `homeport_state_1789_fr` contiennent des valeurs différentes (ex : `Tenigmouth`, `Saint Gilles sur Vie`, `Groeningen`…).

# Exploration

- Les ports vers lesquels exporte Dunkerque et les liens qu'ils entretiennent
- Les ports faisant parti de l'amirauté de Dunkerque et les ports
    - vers lesquels ils exporent
    - d'où ils importent
- Réseau des bateaux avec un `flag` anglais/grande bretagne (voir les smogleurs)