from odoo.tests import common
from odoo import fields


class TestPayrollRate(common.TransactionCase):

    def setUp(self):
        super(TestPayrollRate, self).setUp()
        self.employee = self.env['hr.employee'].create({
            'birthday': '1985-03-14',
            'country_id': self.ref('base.us'),
            'department_id': self.ref('hr.dep_rd'),
            'gender': 'male',
            'name': 'Jared'
        })
        self.contract = self.env['hr.contract'].create({
            'name': 'test',
            'employee_id': self.employee.id,
            'type_id': self.ref('hr_contract.hr_contract_type_emp'),
            'struct_id': self.ref('hr_payroll.structure_base'),
            'resource_calendar_id': self.ref('resource.resource_calendar_std'),
            'wage': 21.50,
            'date_start': '2018-01-01',
            'state': 'open',
            'schedule_pay': 'monthly',
        })
        self.payslip = self.env['hr.payslip'].create({
            'employee_id': self.employee.id,
        })

    def test_payslip_timesheet(self):
        rate = self.payslip.get_rate('TEST')
        self.assertFalse(rate)
        test_rate = self.env['hr.payroll.rate'].create({
            'name': 'Test Rate',
            'code': 'TEST',
            'rate': 1.65,
            'date_from': '2018-01-01',
        })

        rate = self.payslip.get_rate('TEST')
        self.assertEqual(rate, test_rate)
