# -*- coding: utf-8 -*-
import md5
import urllib


class Alipay(object):

    GATEWAY_URL = 'https://mapi.alipay.com/gateway.do'

    def __init__(self, pid, key, seller_email):
        self.key = key
        self.default_params = {'_input_charset': 'utf-8',
                               'partner': pid,
                               'seller_email': seller_email,
                               'payment_type': '1'}

    def _generate_sign(self, params):
        src = '&'.join(['%s=%s' % (key, value) for key,
                        value in sorted(params.iteritems())]) + self.key
        return md5.new(src).hexdigest()

    def _build_url(self, service, **kw):
        params = self.default_params.copy()
        params['service'] = service
        params.update(kw)
        params.update({'sign_type': 'MD5',
                       'sign': self._generate_sign(params)})

        return '%s?%s' % (self.GATEWAY_URL, urllib.urlencode(params))

    def create_direct_pay_by_user_url(self, **kw):
        '''即时到帐'''
        url = self._build_url('create_direct_pay_by_user', **kw)
        return url

    def create_partner_trade_by_buyer_url(self, **kw):
        '''担保交易'''
        url = self._build_url('create_partner_trade_by_buyer', **kw)
        return url

    def trade_create_by_buyer_url(self, **kw):
        '''标准双接口'''
        url = self._build_url('create_partner_trade_by_buyer', **kw)
        return url
