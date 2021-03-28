# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ResPartner(models.Model):
    _name = 'person.test'

    name = fields.Char()

    def get_all_persons(self):
        # list = ['']
        # list.append('a')
        # list.append('b')
        # list.append('c')
        # list.append('d')
        persons = self.env['res.partner'].search([])
        all_persons = []
        for person in persons:
            one_person = []
            one_person.append(person.name)
            one_person.append(person.street)
            one_person.append(person.phone)
            all_persons.append(one_person)
            print(person.name)
        return all_persons
