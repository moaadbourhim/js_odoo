# -*- coding: utf-8 -*-

import base64
import requests
import uuid
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Company(models.Model):
    _inherit = 'res.company'

    chorus_url = fields.Char("URL")
    GatewayClientId = fields.Char("GatewayClientId")
    MachineName = fields.Char("MachineName")
    AccessKey = fields.Char("AccessKey")
    OneWayAPI = fields.Boolean("OneWayAPI")
    TemplateId = fields.Char("TemplateId")

class AccountMove(models.Model):
    _inherit = 'account.move'

    chorus_sent = fields.Boolean("Envoyée à chorus", readonly=True)

    ##--##
    bilan_year = fields.Selection(string="BILAN FISCAL", selection=[('2020', '2020'),
                                                               ('2021', '2021'),
                                                               ('2022', '2022'),
                                                               ('2023', '2023'),
                                                               ('2024', '2024'),
                                                               ('2025', '2025'),
                                                               ('2026', '2026'),
                                                               ('2027', '2027'),
                                                               ('2028', '2028'),
                                                               ('2029', '2029'),
                                                               ('2030', '2030')], required=False)

    date_realisation = fields.Datetime(string="Date de realisation", store=True, compute='_compute_date_realisation')

    gp_chantier_id = fields.Many2one(comodel_name="project.group", string="Group chantier", store=True, compute='_compute_gp_chantier', inverse='_set_gp_chantier')

    @api.depends('invoice_line_ids', 'invoice_line_ids.sale_line_ids', 'invoice_line_ids.sale_line_ids.date_realisation_so')
    def _compute_date_realisation(self):
        for rec in self:
            if rec.date_realisation:
                max_date = rec.date_realisation
            elif rec.invoice_line_ids:
                if rec.invoice_line_ids[0].sale_line_ids:
                    if rec.invoice_line_ids[0].sale_line_ids[0].date_realisation_so:
                        max_date = rec.invoice_line_ids[0].sale_line_ids[0].date_realisation_so
                else:
                    return
            else:
                return

            if rec.invoice_line_ids:
                for line in rec.invoice_line_ids:
                    if line.sale_line_ids:
                        for sale_line in line.sale_line_ids:
                            if sale_line.date_realisation_so > max_date:
                                max_date = sale_line.date_realisation_so

        rec.date_realisation = max_date

    @api.depends('invoice_line_ids',
                 'invoice_line_ids.sale_line_ids',
                 'invoice_line_ids.sale_line_ids.order_id',
                 'invoice_line_ids.sale_line_ids.order_id.group_chantier_id')
    def _compute_gp_chantier(self):
        for rec in self:
            if rec.invoice_line_ids and rec.invoice_line_ids.sale_line_ids:
                rec.gp_chantier_id = rec.invoice_line_ids[0].sale_line_ids[0].order_id.group_chantier_id

    def _set_gp_chantier(self):
        for rec in self:
            for invoice_line in rec.invoice_line_ids:
                for sale_line in invoice_line.sale_line_ids:
                    for sale_order in sale_line.order_id:
                        sale_order.group_chantier_id = rec.gp_chantier_id


    def get_token(self,url,GatewayClientId,MachineName,AccessKey,OneWayAPI):
        url = url+'/api/login/gc'
        data = {
         "GatewayClientId": GatewayClientId,
         "MachineName": MachineName,
         "AccessKey": AccessKey,
         "OneWayAPI": OneWayAPI,
        }
        res = requests.post(url, json=data)
        if res.status_code == 200:
            return res.text
        else:
            return False

    def facturation_chorus(self):
        send_url = self.company_id.chorus_url+'/api/documents/send'
        GatewayClientId = self.company_id.GatewayClientId
        MachineName = self.company_id.MachineName
        AccessKey = self.company_id.AccessKey
        OneWayAPI = self.company_id.OneWayAPI
        TemplateId = self.company_id.TemplateId
        token = self.get_token(self.company_id.chorus_url,GatewayClientId,MachineName,AccessKey,OneWayAPI)
        headers = {'Authorization': 'Bearer ' + token}
        report_name = ""
        pdf = self.env.ref('account_extend.gecop_invoice_siret_report_id').sudo()._render_qweb_pdf([self.id], report_name)[0]
        file = base64.b64encode(pdf).decode('utf-8')
        data = {
            "DocumentId": str(uuid.uuid1()),
            "TemplateId": TemplateId,
            "FileName": f"{self.name.replace('/','')}.pdf",
            "FileSize": len(pdf),
            "FileContent": file,
            "Variables": ""
        }

        res = requests.post(send_url, json=data, headers=headers)

        if res.status_code == 200:
            self.chorus_sent = True

        else:
            raise ValidationError('Echec transfert!')

        return res.status_code

