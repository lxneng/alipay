import unittest


class AlipayTests(unittest.TestCase):
    def Alipay(self, *a, **kw):
        from alipay import Alipay
        return Alipay(*a, **kw)

    def setUp(self):
        self.alipay = self.Alipay(pid='pid', key='key',
                                  seller_email='lxneng@gmail.com')

    def test_create_direct_pay_by_user_url(self):
        params = {'out_trade_no': '1',
                  'subject': 'test',
                  'price': '0.01',
                  'quantity': 1}
        self.assertIn('create_direct_pay_by_user',
                      self.alipay.create_direct_pay_by_user_url(**params))

    def test_create_partner_trade_by_buyer_url(self):
        params = {'out_trade_no': '1',
                  'subject': 'test',
                  'logistics_type': 'POST',
                  'logistics_fee': '0',
                  'logistics_payment': 'SELLER_PAY',
                  'price': '0.01',
                  'quantity': 1}
        self.assertIn('create_partner_trade_by_buyer',
                      self.alipay.create_partner_trade_by_buyer_url(**params))

    def test_trade_create_by_buyer_url(self):
        params = {'out_trade_no': '1',
                  'subject': 'test',
                  'logistics_type': 'POST',
                  'logistics_fee': '0',
                  'logistics_payment': 'SELLER_PAY',
                  'price': '0.01',
                  'quantity': 1}
        self.assertIn('trade_create_by_buyer',
                      self.alipay.trade_create_by_buyer_url(**params))

    def test_raise_missing_parameter_in_create_direct_pay_by_user_url(self):
        from .exceptions import MissingParameter
        params = {'out_trade_no': '1',
                  'price': '0.01',
                  'quantity': 1}
        self.assertRaises(MissingParameter,
                          self.alipay.create_direct_pay_by_user_url, **params)

    def test_raise_parameter_value_error_in_create_direct_pay_by_user_url(self
                                                                          ):
        from .exceptions import ParameterValueError
        params = {'out_trade_no': '1',
                  'subject': 'test',
                  'quantity': 1}
        self.assertRaises(ParameterValueError,
                          self.alipay.create_direct_pay_by_user_url,
                          **params)
