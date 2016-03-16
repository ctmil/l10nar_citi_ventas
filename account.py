# -*- coding: utf-8 -*-
from openerp import models, api, fields


class account_period(models.Model):
	_inherit = "account.period"

        @api.model
        def _create_citi_file(self):
		periods = self.search([])
		for period in periods:	
			file_name = "/tmp/ventas" + period.code.replace('/','') + '.txt'
			file_name_alicuota = "/tmp/ventas_alicuotas" + period.code.replace('/','') + '.txt'
			fo = open(file_name,'wb')
			fa = open(file_name_alicuota,'wb')
			invoices = self.env['account.invoice'].search([('period_id','=',period.id),('type','in',('out_invoice','out_refund'))])
			for invoice in invoices:
				date_invoice = invoice.date_invoice
				date_invoice = date_invoice[:4]+date_invoice[5:7]+date_invoice[8:10]
				invoice_type = str(invoice.journal_id.journal_class_id.afip_code).encode('utf-8').zfill(3)
				point_of_sale = str(invoice.journal_id.point_of_sale).encode('utf-8').zfill(5)
				invoice_number = str(invoice.internal_number[5:]).encode('utf-8').zfill(20)
				invoice_number_to = str(invoice.internal_number[5:]).encode('utf-8').zfill(20)
				document_afip_code = str(invoice.partner_id.document_type_id.afip_code).encode('utf-8').zfill(2)
				document_number = str(invoice.partner_id.document_number).encode('utf-8').zfill(20)
                                if document_afip_code == '99':
                                        #                  12345678901234567890
                                        document_number = '00000000000000000000'
				customer = invoice.partner_id.name.ljust(30).encode('utf-8')
				if len(customer) > 30:
					customer = customer[:30]
				# amount_untaxed = str(int(invoice.amount_untaxed * 100 )).encode('utf-8').zfill(15)
				amount_untaxed = str(int(invoice.amount_total * 100 )).encode('utf-8').zfill(15)
				column_10 = '0'.encode('utf-8').zfill(15)
				column_11 = '0'.encode('utf-8').zfill(15)
				column_12 = '0'.encode('utf-8').zfill(15)
				column_13 = '0'.encode('utf-8').zfill(15)
				column_14 = '0'.encode('utf-8').zfill(15)
				column_15 = '0'.encode('utf-8').zfill(15)
				# amount_tax = str(int(invoice.amount_tax*100)).encode('utf-8').zfill(15)
				amount_tax = str(int(0)).encode('utf-8').zfill(15)
				currency_code = 'PES'.encode('utf-8')
				currency_rate = '0001000000'.encode('utf-8')
				alicuotas = '1'.encode('utf-8')
				codigo_operacion = ' '.encode('utf-8')
				otros_tributos = '0'.encode('utf-8').zfill(15)
				date_due = '00000000'.encode('utf-8')
				string_write = date_invoice + invoice_type + point_of_sale + invoice_number 
				string_write = string_write + invoice_number_to  + document_afip_code + document_number
				string_write = string_write + customer + amount_untaxed + column_10 + column_11 + column_12 
				string_write = string_write + column_13 + column_14 + column_15 
				string_write = string_write + amount_tax + currency_code + currency_rate + alicuotas
				string_write = string_write + codigo_operacion + otros_tributos + date_due + '\n'
				string_alicuota_write = invoice_type + point_of_sale + invoice_number + amount_untaxed + '0005' + amount_tax + '\n'
				fo.write(string_write)
				fa.write(string_alicuota_write)
			fo.close()
			fa.close()
                return None


