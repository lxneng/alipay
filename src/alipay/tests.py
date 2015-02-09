# -*- coding: utf-8 -*-
# encoding: utf-8
import unittest
import six
from xml.etree import ElementTree
if six.PY3:
    from urllib.parse import parse_qs, urlparse
else:
    from urlparse import parse_qs, urlparse


class AlipayTests(unittest.TestCase):
    def Alipay(self, *a, **kw):
        from alipay import Alipay
        return Alipay(*a, **kw)

    def WapAlipay(self, *a, **kw):
        from alipay import WapAlipay
        return WapAlipay(*a, **kw)

    def setUp(self):
        self.alipay = self.Alipay(pid='pid', key='key',
                                  seller_email='lxneng@gmail.com')
        self.wapalipay = self.WapAlipay(pid='pid', key='key',
                                        seller_email='lxneng@gmail.com')

    def test_create_direct_pay_by_user_url(self):
        params = {'out_trade_no': '1',
                  'subject': 'test',
                  'price': '0.01',
                  'quantity': 1}
        self.assertIn('create_direct_pay_by_user',
                      self.alipay.create_direct_pay_by_user_url(**params))

    def test_create_direct_pay_by_user_url_with_unicode(self):
        params = {'out_trade_no': '1',
                  'subject': u'测试',
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

    def test_raise_parameter_value_error_when_initializing(self):
        from .exceptions import ParameterValueError
        self.assertRaises(ParameterValueError,
                          self.Alipay, pid='pid', key='key')

    def test_create_wap_direct_pay_by_user_url(self):
        params = {'out_trade_no': '1',
                  'subject': u'测试',
                  'total_fee': '0.01',
                  'seller_account_name': self.wapalipay.seller_email,
                  'call_back_url': 'http://mydomain.com/alipay/callback'}
        url = self.wapalipay.create_direct_pay_token_url(**params)
        self.assertIn('alipay.wap.trade.create.direct', url)
        params = parse_qs(urlparse(url).query, keep_blank_values=True)
        self.assertIn('req_data', params)
        self.assertIn('sec_id', params)
        tree = ElementTree.ElementTree(ElementTree.fromstring(params['req_data'][0]))
        self.assertEqual(self.wapalipay.TOKEN_ROOT_NODE, tree.getroot().tag)

    def test_wap_notimplemented_pay(self):
        params = {}
        self.assertRaises(NotImplementedError,
                          self.wapalipay.trade_create_by_buyer_url, **params)
        self.assertRaises(NotImplementedError,
                          self.wapalipay.create_partner_trade_by_buyer_url, **params)

    def test_wap_unauthorization_token(self):
        from .exceptions import TokenAuthorizationError
        params = {'out_trade_no': '1',
                  'subject': u'测试',
                  'total_fee': '0.01',
                  'seller_account_name': self.wapalipay.seller_email,
                  'call_back_url': 'http://mydomain.com/alipay/callback'}
        self.assertRaises(TokenAuthorizationError,
                          self.wapalipay.create_direct_pay_by_user_url, **params)

    def test_wap_notifyurl(self):
        '''valid MD5 sign
        invalid notify id but should not throw any exception

        sec_id=MD5&v=1.0&notify_data=<notify><payment_type>1</payment_type><subject>测试</subject><trade_no>2014080239826696</trade_no><buyer_email>xxx@gmail.com</buyer_email><gmt_create>2014-08-02 14:49:13</gmt_create><notify_type>trade_status_sync</notify_type><quantity>1</quantity><out_trade_no>BD8Y9JQ2LT8MVXLMT34RTUWEMMBAXMIGBVQGF5CQNZHPYPQHSD4MEI56NQD2OLNV</out_trade_no><notify_time>2014-08-02 15:14:25</notify_time><seller_id>2088411445328172</seller_id><trade_status>TRADE_FINISHED</trade_status><is_total_fee_adjust>N</is_total_fee_adjust><total_fee>0.03</total_fee><gmt_payment>2014-08-02 14:49:27</gmt_payment><seller_email>lxneng@gmail.com</seller_email><gmt_close>2014-08-02 14:49:27</gmt_close><price>0.03</price><buyer_id>2088002293077967</buyer_id><notify_id>6a40ac71fcf17d99b5274b0c6c8970ea7c</notify_id><use_coupon>N</use_coupon></notify>&service=alipay.wap.trade.create.direct&sign=1f0a524dc51ed5bfc7ee2bac62e39534
        '''
        params = {'sec_id': 'MD5', 'v': '1.0',
                  'notify_data': u'<notify><payment_type>1</payment_type><subject>测试</subject><trade_no>2014080239826696</trade_no><buyer_email>xxx@gmail.com</buyer_email><gmt_create>2014-08-02 14:49:13</gmt_create><notify_type>trade_status_sync</notify_type><quantity>1</quantity><out_trade_no>BD8Y9JQ2LT8MVXLMT34RTUWEMMBAXMIGBVQGF5CQNZHPYPQHSD4MEI56NQD2OLNV</out_trade_no><notify_time>2014-08-02 15:14:25</notify_time><seller_id>2088411445328172</seller_id><trade_status>TRADE_FINISHED</trade_status><is_total_fee_adjust>N</is_total_fee_adjust><total_fee>0.03</total_fee><gmt_payment>2014-08-02 14:49:27</gmt_payment><seller_email>lxneng@gmail.com</seller_email><gmt_close>2014-08-02 14:49:27</gmt_close><price>0.03</price><buyer_id>2088002293077967</buyer_id><notify_id>6a40ac71fcf17d99b5274b0c6c8970ea7c</notify_id><use_coupon>N</use_coupon></notify>',
                  'service': 'alipay.wap.trade.create.direct',
                  'sign': '1f0a524dc51ed5bfc7ee2bac62e39534'}
        rt = self.wapalipay.verify_notify(**params)
        self.assertFalse(rt)
