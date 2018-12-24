from odoo import api, _
from odoo import fields, models
from datetime import date
from io import StringIO
import base64
import logging
logger=logging.getLogger('_______boubaker ____________')

class Product(models.Model):
    _inherit = 'product.template'

    qty_low_stock_notify = fields.Integer(string='Notify for Qty Below', default=100,
                                           help='When stock on hand falls below this number, it will be included in the low stock report.')

    @api.multi
    def send_low_stock_via_email(self):
        header_label_list=["REF", "Name", "Qty On Hand","Qty Incoming","Low Stock Qty"]
        ## Get email template
        template = self.env['mail.template'].search([('name', '=', 'Low Stock Automated Report')], limit=1)
        if template:
            default_body = template.body_html
            custom_body  = """
                <table border="1">
                    <th>%s</th>
                    <th>%s</th>
                    <th style="text-align:center;">%s</th>
                    <th style="text-align:center;">%s</th>
                    <th style="text-align:center;">%s</th>
            """ %(header_label_list[0], header_label_list[1], header_label_list[2], header_label_list[3], header_label_list[4])
            ## Check for low stock products
            product_ids  = self.env['product.product'].search([('active', '=', True), ('sale_ok', '=', True), ('default_code', '!=', False)])
            for product in product_ids:
                default_code = product.default_code
                if not default_code or default_code == '':
                    continue
                qty_available = product.qty_available
                qty_incoming  = product.incoming_qty
                qty_low_stock_notify = product.qty_low_stock_notify
                if qty_available <= qty_low_stock_notify and qty_low_stock_notify >= 0: ## set low_stock_notify = -1 to never be notified
                    custom_body += """
                        <tr style="font-size:14px;">
                            <td>%s</td>
                            <td>%s</td>
                            <td style="text-align:center;">%s</td>
                            <td style="text-align:center;">%s</td>
                            <td style="text-align:center;">%s</td>
                        </tr>
                    """ %(default_code, product.name, str(qty_available), str(qty_incoming), str(qty_low_stock_notify))
            custom_body  += "</table>"
            template.body_html = default_body + custom_body
            logger.info("___template_body_html________: %s ",template.body_html)
            send_email = template.send_mail(template.id, force_send=True)
            logger.info("___send_email________: %s ",send_email)
            template.body_html = default_body
            return True 
