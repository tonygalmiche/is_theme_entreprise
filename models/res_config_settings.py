# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_theme_couleur          = fields.Char(related='company_id.is_theme_couleur', readonly=False)
    is_theme_eclaircissement  = fields.Integer(related='company_id.is_theme_eclaircissement', readonly=False)
    is_theme_couleur_claire   = fields.Char(related='company_id.is_theme_couleur_claire')
    is_theme_label_nowrap     = fields.Boolean(related='company_id.is_theme_label_nowrap', readonly=False)
