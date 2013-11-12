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
        self.assertEqual(self.alipay.create_direct_pay_by_user_url(**params),
                         'https://mapi.alipay.com/gateway.do?seller_email=lxneng%40gmail.com&service=create_direct_pay_by_user&price=0.01&_input_charset=utf-8&sign=99a55d52ba4f9f026137b5d68cd1b60e&out_trade_no=1&payment_type=1&sign_type=MD5&partner=pid&subject=test&quantity=1')

    def test_create_partner_trade_by_buyer_url(self):
        params = {'out_trade_no': '1',
                  'subject': 'test',
                  'logistics_type': 'POST',
                  'logistics_fee': '0',
                  'logistics_payment': 'SELLER_PAY',
                  'price': '0.01',
                  'quantity': 1}
        self.assertEqual(self.alipay.create_partner_trade_by_buyer_url(**params),
                         'https://mapi.alipay.com/gateway.do?seller_email=lxneng%40gmail.com&logistics_fee=0&logistics_type=POST&service=create_partner_trade_by_buyer&price=0.01&sign_type=MD5&_input_charset=utf-8&sign=129b75d1e2d10197f3f0dbd34cec8dc2&out_trade_no=1&payment_type=1&logistics_payment=SELLER_PAY&partner=pid&subject=test&quantity=1')

    def test_trade_create_by_buyer_url(self):
        params = {'out_trade_no': '1',
                  'subject': 'test',
                  'logistics_type': 'POST',
                  'logistics_fee': '0',
                  'logistics_payment': 'SELLER_PAY',
                  'price': '0.01',
                  'quantity': 1}
        self.assertEqual(self.alipay.trade_create_by_buyer_url(**params),
                         'https://mapi.alipay.com/gateway.do?seller_email=lxneng%40gmail.com&logistics_fee=0&logistics_type=POST&service=trade_create_by_buyer&price=0.01&sign_type=MD5&_input_charset=utf-8&sign=956d6bb1dd56f7ef26689ed9a5711035&out_trade_no=1&payment_type=1&logistics_payment=SELLER_PAY&partner=pid&subject=test&quantity=1')

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
