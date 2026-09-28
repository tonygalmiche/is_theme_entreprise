# -*- coding: utf-8 -*-
import re

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.http import request


COULEUR_RE      = re.compile(r'^#[0-9A-Fa-f]{6}$')
TAUX_FONCE      = 0.15  # Part de noir pour la teinte foncée (survol des boutons)
CONTRASTE_MINI  = 3.0   # Contraste minimum avec le blanc pour un texte ou un lien lisible


def _hex_vers_rgb(couleur):
    return tuple(int(couleur[i:i + 2], 16) for i in (1, 3, 5))


def _rgb_vers_hex(rgb):
    return '#%02X%02X%02X' % tuple(int(round(min(255, max(0, v)))) for v in rgb)


def _melange(rgb, cible, taux):
    """Mélange rgb avec cible (0 = noir, 255 = blanc) selon taux (0 à 1)"""
    return tuple(v + (cible - v) * taux for v in rgb)


def _luminance(rgb):
    """Luminance relative (WCAG)"""
    def canal(v):
        v = v / 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (canal(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _contraste_blanc(rgb):
    return 1.05 / (_luminance(rgb) + 0.05)


class ResCompany(models.Model):
    _inherit = 'res.company'

    is_theme_couleur         = fields.Char("Couleur de l'entreprise", help="Code hexadécimal, ex. #EF582C. Vide = thème Odoo standard")
    is_theme_eclaircissement = fields.Integer("Éclaircissement (%)", default=80, help="Part de blanc mélangé à la couleur de l'entreprise pour obtenir la couleur claire (onglets, en-têtes de tableaux)")
    is_theme_couleur_claire  = fields.Char("Couleur claire", compute='_compute_is_theme_couleur_claire')
    is_theme_label_nowrap    = fields.Boolean("Pas de retour à la ligne du nom des champs")

    @api.depends('is_theme_couleur', 'is_theme_eclaircissement')
    def _compute_is_theme_couleur_claire(self):
        for obj in self:
            couleurs = obj._is_theme_couleurs()
            obj.is_theme_couleur_claire = couleurs and couleurs['claire']

    @api.constrains('is_theme_couleur')
    def _check_is_theme_couleur(self):
        for obj in self:
            if obj.is_theme_couleur and not COULEUR_RE.match(obj.is_theme_couleur):
                raise ValidationError("La couleur de l'entreprise doit être au format #RRGGBB (ex. #EF582C) : %s" % obj.is_theme_couleur)

    @api.constrains('is_theme_eclaircissement')
    def _check_is_theme_eclaircissement(self):
        for obj in self:
            if not 0 <= obj.is_theme_eclaircissement <= 100:
                raise ValidationError("L'éclaircissement doit être compris entre 0 et 100 %.")

    def _is_theme_couleurs(self):
        """Couleurs dérivées de la couleur de l'entreprise, ou {} si elle n'est pas saisie"""
        self.ensure_one()
        if not self.is_theme_couleur or not COULEUR_RE.match(self.is_theme_couleur):
            return {}
        rgb = _hex_vers_rgb(self.is_theme_couleur)
        taux = min(100, max(0, self.is_theme_eclaircissement)) / 100
        fonce = _melange(rgb, 0, TAUX_FONCE)

        # Couleur lisible sur fond blanc (liens, cases cochées) : on fonce tant que le contraste est insuffisant
        lisible = rgb
        while _contraste_blanc(lisible) < CONTRASTE_MINI:
            lisible = _melange(lisible, 0, 0.1)

        return {
            'couleur': _rgb_vers_hex(rgb),
            'claire' : _rgb_vers_hex(_melange(rgb, 255, taux)),
            'foncee' : _rgb_vers_hex(fonce),
            'lisible': _rgb_vers_hex(lisible),
            'lisible_rgb': '%d, %d, %d' % tuple(int(round(v)) for v in lisible),
            'survol'     : _rgb_vers_hex(_melange(lisible, 0, TAUX_FONCE)),
            'survol_rgb' : '%d, %d, %d' % tuple(int(round(v)) for v in _melange(lisible, 0, TAUX_FONCE)),
            'texte'  : '#FFFFFF' if _contraste_blanc(rgb) >= CONTRASTE_MINI else '#000000',
        }

    @api.model
    def _is_theme_societe_courante(self):
        """Société sélectionnée dans le client web (cookie cids), sinon société par défaut de l'utilisateur"""
        user = self.env.user
        company = user.company_id
        cids = request and request.cookies.get('cids')
        if cids:
            try:
                cid = int(cids.replace(',', '-').split('-')[0])
            except ValueError:
                cid = False
            if cid in user.company_ids.ids:
                company = self.env['res.company'].browse(cid)
        return company.sudo()

    @api.model
    def _is_theme_valeurs(self):
        """Classes du <body> et variables CSS injectées dans web.webclient_bootstrap"""
        company = self._is_theme_societe_courante()
        couleurs = company._is_theme_couleurs()
        classes = []
        css = ''
        if couleurs:
            classes.append('is_theme_actif')
            css = (
                ':root {'
                '--is-theme-couleur: %(couleur)s;'
                '--is-theme-couleur-claire: %(claire)s;'
                '--is-theme-couleur-foncee: %(foncee)s;'
                '--is-theme-couleur-lisible: %(lisible)s;'
                '--is-theme-texte: %(texte)s;'
                '--bs-link-color: %(lisible)s;'
                '--bs-link-color-rgb: %(lisible_rgb)s;'
                '--bs-link-hover-color: %(survol)s;'
                '--bs-link-hover-color-rgb: %(survol_rgb)s;'
                '}'
            ) % couleurs
        if company.is_theme_label_nowrap:
            classes.append('is_theme_label_nowrap')
        return {'classes': ' '.join(classes), 'css': css}
