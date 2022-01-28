---
title: Table des données de la base Navigo
date: 2022-01-28
author: Guillaume Brioudes <https://myllaume.fr/>
---

- `homeport` : port d'attache du navire. On peut y rechercher la valeur `Dunkerque`
- `tonnage` : quantité transportée, à relativiser avec `tonnage_uncertainity`
- `cargo_item_action` : action du bateau
- `commodity_purpose` : mission (objet du voyage). Généralement le nom de la machandise transportée. Les entrées ont besoin d'être *clusterisées* (voir `/scripts/commodity.openrefine.json`)