from lxml import etree
from parameterized import parameterized

from odoo.tests import SavepointCase, tagged


@tagged("post_install", "-at_install")
class TestProduct(SavepointCase):
    @parameterized.expand([("product.template"), ("product.product",)])
    def test_action_open_product_creation_dynamic_wizard(self, model):
        action = self.env[model].action_open_product_creation_dynamic_wizard()
        wizard = self.env["product.creation.dynamic.wizard"].browse(action["res_id"])
        self.assertTrue(wizard.exists())
        self.assertEqual(wizard.current_step, 0)

    @parameterized.expand([("product.template"), ("product.product",)])
    def test_load_views_button_create_disabled(self, model):
        self.env["ir.config_parameter"].set_param(
            "product_creation_dynamic_wizard.disable_create_product_button", "True"
        )
        result = self.env[model].load_views(
            [
                (False, "list"),
                (False, "form"),
                (False, "kanban"),
                (False, "pivot"),
            ]
        )
        for view in result["fields_views"].values():
            doc = etree.XML(view["arch"])
            self.assertTrue(doc.attrib.get("create", False))

    @parameterized.expand([("product.template"), ("product.product",)])
    def test_load_views_button_create_not_disabled(self, model):
        result = self.env[model].load_views(
            [
                (False, "list"),
                (False, "form"),
                (False, "kanban"),
                (False, "pivot"),
            ]
        )
        for view in result["fields_views"].values():
            doc = etree.XML(view["arch"])
            self.assertFalse(doc.attrib.get("create", False))
