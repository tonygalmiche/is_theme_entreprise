# is_theme_entreprise

Module Odoo 18 développé par [InfoSaône](http://www.infosaone.com) : couleur de l'entreprise dans l'interface et styles communs des champs, sans SCSS spécifique dans chaque module client.

Cahier des charges : `~/Documents/Développement/Documentation/modules-generiques/is_theme_entreprise.md`.

## Paramétrage

*Paramètres → Paramètres généraux → Thème de l'entreprise* (par société) :

- **Couleur de l'entreprise** : code `#RRGGBB` (ex. `#EF582C`). Vide = thème Odoo standard.
- **Éclaircissement** (80 % par défaut) : donne la couleur claire, affichée pour contrôle.
- **Pas de retour à la ligne du nom des champs**.

Après modification, recharger la page (F5).

## Ce qui change

| Élément | Couleur |
|---|---|
| Barre de menus | couleur de l'entreprise, texte blanc ou noir selon la luminosité |
| Boutons principaux | couleur de l'entreprise, plus foncée au survol |
| Liens, cases cochées, étape active de la barre d'état | couleur de l'entreprise (foncée si elle est trop claire pour être lisible sur fond blanc) |
| En-têtes de tableaux one2many / many2many, onglet actif | couleur claire |
| Champs à saisir / obligatoires | gris fixes, toujours actifs |

## Fonctionnement

- `static/src/scss/is_theme_entreprise.scss` : styles statiques utilisant des variables CSS `--is-theme-*`, actifs seulement avec les classes `is_theme_actif` / `is_theme_label_nowrap` du `<body>` (sauf les gris des champs).
- `views/webclient_templates.xml` : héritage de `web.webclient_bootstrap` qui ajoute les variables dans l'en-tête de la page et les classes sur le `<body>`, côté serveur (pas de JS).
- `models/res_company.py` : champs, contrôle du format, calcul des couleurs (`_is_theme_couleurs`) et société courante lue dans le cookie `cids` du sélecteur de société.
