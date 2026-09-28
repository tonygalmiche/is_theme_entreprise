# -*- coding: utf-8 -*-
{
    "name": "InfoSaône - Couleurs de l'entreprise pour Odoo 20",
    "version": "20.0.1.0.0",
    "author": "InfoSaône / Tony Galmiche",
    "category": "InfoSaône",
    "summary": "Couleur de l'entreprise (barre de menus, boutons, onglets, en-têtes de tableaux) et styles communs des champs",
    "description": """
        La couleur de l'entreprise se saisit dans Paramètres > Paramètres généraux > Thème de l'entreprise.
        Les teintes claire (onglets, en-têtes de tableaux) et foncée (survol des boutons) sont calculées.
        Les champs à saisir et obligatoires ont toujours le même fond gris.
        Option pour supprimer le retour à la ligne du nom des champs.
    """,
    "maintainer": "InfoSaône",
    "website": "http://www.infosaone.com",
    "depends": [
        'base_setup',
        'web',
    ],
    "data": [
        'views/res_config_settings_views.xml',
        'views/webclient_templates.xml',
    ],
    "assets": {
        'web.assets_backend': [
            'is_theme_entreprise/static/src/scss/is_theme_entreprise.scss',
        ],
    },
    "installable": True,
    "auto_install": False,
    "application": False,
    "license": "AGPL-3",
}
