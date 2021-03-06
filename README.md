# Datasprint PORTIC 2022

Ce répertoire contient à la fois un ensemble de ressources et les productions des participants du datasprint PORTIC 2022 qui se tiendra les 15, 16, 17, 18.

## Installation

Prérequis : installer [git](https://git-scm.com/), [python](https://www.python.org/downloads/) et [pip](https://pypi.org/project/pip/), puis éventuellement créez votre environnement virtuel.

Si vous êtes sur linux, il vous faudra aussi installer `curl` et `unzip` si ces deux commandes ne sont pas déjà présentes sur votre machine.

Puis dans votre terminal, lancer les commandes suivantes :

```
git clone git@github.com:medialab/portic-datasprint-2022.git
cd portic-datasprint-2022
# cela va lancer des pip install, assurez-vous bien d'être dans un vitualenv python dédié auparavant
./install.sh
```

Pour éviter que le git contienne plein de commits de merge, lancer la ligne de configuration suivante est très utile:

```
git config pull.rebase true
```

## Mise à jour des données

Si les données de base venaient à être mises à jour en cours de datasprint, une commande permet de les mettre à jour sur votre copie locale du répertoire (dans le dossier `data`) :

```
./load_data.sh
```

## Contenus du répertoire

- `data` -> données à plat proposées pour le datasprint
- `preliminary_inquiry` -> code permettant de générer un atlas de visualisations préliminaires
- `productions` -> les productions du datasprint, à organiser et réorganiser par modules d'enquête (ex. `module_01`)
- `examples` -> exemples de mobilisation de la bibliothèque seule et avec différentes technologies associées à des notebooks jupyter
- `lib` -> la bibliothèque créée spécifiquement pour le datasprint. Elle pourra éventuellement être améliorée pendant le datasprint

## Bibliothèque python pour le datasprint

Nous avons préparé une bibliothèque python censée faciliter la récupération et la manipulation des données des bases.

Cette bibliothèque propose une abstraction permettant de manipuler les données avec une API unifiée, ainsi qu'une série d'utilitaires. Elle a vocation à être potentiellement enrichie pendant le datasprint.


### Installer la bibliothèque

La bibliothèque python est installée localement par le script `install.sh` (ou via `pip install -e lib`) puis est accessible sous le nom de `dunkerquesprint`.
Ne pas oublier de la réinstaller après un git pull si besoin.

### Utiliser la bibliothèque

Voir :

- [la doc en ligne](https://medialab.github.io/portic-datasprint-2022/).
- [la doc en jupyter notebook exécutable](https://github.com/medialab/portic-datasprint-2021/blob/main/documentation_lib.ipynb)


Les méthodes de base à retenir pour travailler avec les données du datasprint sont :

- pour récupérer les pointcalls associés aux pointcalls du datasprint :

```python
from dunkerquesprint import Portic
portic_client = Portic()
# récupérer les pointcalls de l'année 1789 taggés avec le source_subset associé au corpus du datasprint (équivalent à tous les pointcalls qui concernent les amirautés de La Rochelle, Marennes et Sables d'Olonne)
pointcalls = portic_client.get_pointcalls(year=1789)
```

- pour récupérer les flux Toflit18 associés au datasprint :

```python
from poitousprint import Toflit
toflit_client = Toflit()
# Récupérer les flux qui concernent le bureau des fermes de Dunkerque en 1789
flows = toflit_client.get_flows(year=1789, customs_office='Dunkerque')
```


Les données de base sont disponibles à :

* pour toflit18 : sur le répertoire [`medialab/toflit18_data/base courante.zip`](https://github.com/medialab/toflit18_data/blob/master/base/bdd%20courante.csv.zip) et via le [datascape](http://toflit18.medialab.sciences-po.fr/#/home)
* pour PORTIC : à [http://data.portic.fr/api/](http://data.portic.fr/api/) (documentation originale [ici](https://gitlab.huma-num.fr/portic/porticapi))

### Utilitaire de transformation de notebooks en fichiers HTML

Le répertoire contient également un utilitaire permettant de transformer tous les notebooks d'un dossier donné en fichiers HTML/pages web sur le site github.io associé à ce répertoire.

```bash
python cipynb.py [chemin relatif vers le dossier] -to html
```

Ces derniers sont ensuite accessibles en ligne à `https://medialab.github.io/portic-datasprint-2022/[chemin relatif vers chaque fichier html]`
