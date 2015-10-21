# -*- coding: utf-8 -*-
from __future__ import absolute_import
import time
from hashlib import md5
from datetime import datetime
from xml.etree import ElementTree
from collections import OrderedDict

import six
import requests
from pytz import timezone
from six.moves.urllib.parse import (
    parse_qs,
    urlparse,
    unquote,
    urlencode
)

from .exceptions import MissingParameter
from .exceptions import ParameterValueError
from .exceptions import TokenAuthorizationError


def encode_dict(params):
    return {k: six.u(v).encode('utf-8')
            if isinstance(v, str) else v.encode('utf-8')
            if isinstance(v, six.string_types) else v
            for k, v in six.iteritems(params)}


class Alipay(object):

    GATEWAY_URL = 'https://mapi.alipay.com/gateway.do'

    NOTIFY_GATEWAY_URL = 'https://mapi.alipay.com/gateway.do'\
        '?service=notify_verify&partner=%s&notify_id=%s'

    sign_tuple = ('sign_type', 'MD5', 'MD5')
    sign_key = False

    def __init__(self, pid, key, seller_email=None, seller_id=None):
        self.key = key
        self.pid = pid
        self.default_params = {'_input_charset': 'utf-8',
                               'partner': pid,
                               'payment_type': '1'}
        # 优先使用 seller_id （与接口端的行为一致）
        if seller_id is not None:
            self.default_params['seller_id'] = seller_id
        elif seller_email is not None:
            self.default_params['seller_email'] = seller_email
        else:
            raise ParameterValueError(
                "seller_email and seller_id must have one.")

    def _generate_md5_sign(self, params):
        src = '&'.join(['%s=%s' % (key, value) for key,
                        value in sorted(params.items())]) + self.key
        return md5(src.encode('utf-8')).hexdigest()

    def _check_params(self, params, names):
        if not all(k in params for k in names):
            raise MissingParameter('missing parameters')

    def _build_url(self, service, paramnames=None, **kw):
        '''
        创建带签名的请求地址，paramnames为需要包含的参数名，用于避免出现过多的参数，默认使用全部参数
        '''
        params = self.default_params.copy()
        params['service'] = service
        params.update(kw)
        if paramnames:
            params = dict([(k, params[k]) for k in paramnames if k in params])
        signkey, signvalue, signdescription = self.sign_tuple
        signmethod = getattr(
            self,
            '_generate_%s_sign' % signdescription.lower(),
            None  # getattr raise AttributeError if not default provided
        )
        if signmethod is None:
            raise NotImplementedError(
                "This type '%s' of sign is not implemented yet."
                % signdescription)
        if self.sign_key:
            params.update({signkey: signvalue})
        params.update({signkey: signvalue,
                       'sign': signmethod(params)})

        return '%s?%s' % (self.GATEWAY_URL, urlencode(encode_dict(params)))

    def create_direct_pay_by_user_url(self, **kw):
        '''即时到帐'''
        self._check_params(kw, ('out_trade_no', 'subject'))

        if not kw.get('total_fee') and \
           not (kw.get('price') and kw.get('quantity')):
            raise ParameterValueError(
                'total_fee or (price && quantiry) must have one.')

        url = self._build_url('create_direct_pay_by_user', **kw)
        return url

    def create_partner_trade_by_buyer_url(self, **kw):
        '''担保交易'''
        names = ('out_trade_no', 'subject', 'logistics_type',
                 'logistics_fee', 'logistics_payment', 'price', 'quantity')
        self._check_params(kw, names)
        url = self._build_url('create_partner_trade_by_buyer', **kw)
        return url

    def create_batch_trans_notify_url(self,
                                      batch_list=(),
                                      tzinfo='Asia/Shanghai',
                                      **kw):
        '''批量付款'''
        names = ('account_name', 'batch_no', 'notify_url')
        self._check_params(kw, names)
        batch_no = kw['batch_no']
        detail_data = ''
        total_fee = 0.0
        total_num = 0
        for itm in batch_list:
            total_fee += float(itm['fee'])
            total_num += 1
            detail_data += '^'.join((batch_no + str(total_num),
                                     itm['account'], itm['name'],
                                     str(itm['fee']), itm['note'] + '|'))
        kw['detail_data'] = detail_data
        utcnow = datetime.utcnow()
        local_now = timezone(tzinfo).fromutc(utcnow)
        kw['batch_num'] = total_num
        kw['batch_fee'] = total_fee
        kw['email'] = self.default_params['seller_email']
        kw['pay_date'] = local_now.strftime('%Y%m%d')
        url = self._build_url('batch_trans_notify', **kw)
        return url

    def trade_create_by_buyer_url(self, **kw):
        '''标准双接口'''
        names = ('out_trade_no', 'subject', 'logistics_type',
                 'logistics_fee', 'logistics_payment', 'price', 'quantity')
        self._check_params(kw, names)

        url = self._build_url('trade_create_by_buyer', **kw)
        return url

    def create_forex_trade_url(self, **kw):
        '''Create website payment for foreigners (With QR code)'''
        names = ('out_trade_no', 'subject')
        self._check_params(kw, names)

        url = self._build_url('create_forex_trade', **kw)
        return url

    def create_forex_trade_wap_url(self, **kw):
        '''Create mobile payment for foreigners'''
        names = ('out_trade_no', 'subject')
        self._check_params(kw, names)

        url = self._build_url('create_forex_trade_wap', **kw)
        return url

    def add_alipay_qrcode_url(self, **kw):
        '''二维码管理 - 添加'''
        self._check_params(kw, ('biz_data', 'biz_type'))

        utcnow = datetime.utcnow()
        shanghainow = timezone('Asia/Shanghai').fromutc(utcnow)

        kw['method'] = 'add'
        kw['timestamp'] = shanghainow.strftime('%Y-%m-%d %H:%M:%S')

        url = self._build_url('alipay.mobile.qrcode.manage', **kw)
        return url

    def send_goods_confirm_by_platform(self, **kw):
        ''''确认发货'''
        names = ('trade_no', 'logistics_name')
        self._check_params(kw, names)
        url = self._build_url('send_goods_confirm_by_platform', **kw)
        return url

    def add_alipay_qrcode(self, **kw):
        return requests.get(self.add_alipay_qrcode_url(**kw))

    def get_sign_method(self, **kw):
        signkey, signvalue, signdescription = self.sign_tuple
        signmethod = getattr(
            self,
            '_generate_%s_sign' % signdescription.lower(),
            None
        )
        if signmethod is None:
            raise NotImplementedError(
                "This type '%s' of sign is not implemented yet."
                % signdescription)
        return signmethod

    def verify_notify(self, **kw):
        sign = kw.pop('sign', '')
        kw.pop('sign_type', '')
        signmethod = self.get_sign_method(**kw)
        if signmethod(kw) == sign:
            return self.check_notify_remotely(**kw)
        else:
            return False

    def check_notify_remotely(self, **kw):
        remote_result = requests.get(
            self.NOTIFY_GATEWAY_URL % (self.pid, kw['notify_id']),
            headers={'connection': 'close'}
        ).text
        return remote_result == 'true'

    def single_trade_query(self, **kw):
        '''
        单笔交易查询,返回xml.
        out_trade_no或者trade_no参数必须有一个.
        该接口需要联系支付宝客服签约.
        '''
        if 'trade_no' not in kw and 'out_trade_no' not in kw:
            raise MissingParameter('missing parameters')
        url = self._build_url('single_trade_query', paramnames=['service', 'partner', '_input_charset', 'sign', 'sign_type', 'trade_no', 'out_trade_no'], **kw)
        remote_result = requests.get(url, headers={'connection': 'close'}).text
        return remote_result

'''Wap支付接口'''


class WapAlipay(Alipay):
    GATEWAY_URL = 'http://wappaygw.alipay.com/service/rest.htm'
    TOKEN_ROOT_NODE = 'direct_trade_create_req'
    AUTH_ROOT_NODE = 'auth_and_execute_req'
    _xmlnode = '<%s>%s</%s>'
    sign_tuple = ('sec_id', 'MD5', 'MD5')
    sign_key = True

    def __init__(self, pid, key, seller_email):
        super(WapAlipay, self).__init__(pid, key, seller_email)
        self.seller_email = seller_email
        self.default_params = {'format': 'xml',
                               'v': '2.0',
                               'partner': pid,
                               '_input_charset': 'utf-8',
                               }

    def create_direct_pay_token_url(self, **kw):
        '''即时到帐token'''
        names = ('subject', 'out_trade_no', 'total_fee', 'seller_account_name',
                 'call_back_url', )
        self._check_params(kw, names)
        req_data = ''.join([self._xmlnode % (key, value, key)
                            for (key, value) in six.iteritems(kw)])
        req_data = self._xmlnode % (
            self.TOKEN_ROOT_NODE, req_data, self.TOKEN_ROOT_NODE)
        if '&' in req_data:
            raise ParameterValueError('character \'&\' is not allowed.')
        params = {'req_data': req_data, 'req_id': time.time()}
        url = self._build_url('alipay.wap.trade.create.direct', **params)
        return url

    def create_direct_pay_by_user_url(self, **kw):
        '''即时到帐'''
        if 'token' not in kw:
            url = self.create_direct_pay_token_url(**kw)
            alipayres = requests.post(
                url, headers={'connection': 'close'}).text
            params = parse_qs(urlparse(alipayres).path, keep_blank_values=True)
            if 'res_data' in params:
                tree = ElementTree.ElementTree(
                    ElementTree.fromstring(unquote(params['res_data'][0])))
                token = tree.find("request_token").text
            else:
                raise TokenAuthorizationError(unquote(params['res_error'][0]))
        else:
            token = kw['token']
        params = {'req_data': self._xmlnode % 
                  (self.AUTH_ROOT_NODE,
                   (self._xmlnode % ('request_token', token, 'request_token')),
                   self.AUTH_ROOT_NODE)}
        url = self._build_url('alipay.wap.auth.authAndExecute', **params)
        return url

    def trade_create_by_buyer_url(self, **kw):
        raise NotImplementedError("This type of pay is not supported in wap.")

    def create_partner_trade_by_buyer_url(self, **kw):
        raise NotImplementedError("This type of pay is not supported in wap.")

    def check_notify_remotely(self, **kw):
        if 'notify_data' in kw:
            notifydata = unquote(kw['notify_data'])
            if isinstance(notifydata, str):
                notifydata = six.u(notifydata).encode('utf-8')
            elif isinstance(notifydata, six.string_types):
                notifydata = notifydata.encode('utf-8')
            tree = ElementTree.ElementTree(ElementTree.fromstring(notifydata))
            return super(WapAlipay, self).check_notify_remotely(
                **{'notify_id': tree.find("notify_id").text})
        return True

    def _generate_md5_notify_sign(self, kw):
        newpara = OrderedDict()
        newpara['service'] = kw['service']
        newpara['v'] = kw['v']
        newpara['sec_id'] = kw['sec_id']
        newpara['notify_data'] = kw['notify_data']
        src = '&'.join(['%s=%s' % (key, value)
                        for key, value in newpara.items()]) + self.key
        return md5(src.encode('utf-8')).hexdigest()

    def get_sign_method(self, **kw):
        if 'notify_data' in kw:
            signkey, signvalue, signdescription = self.sign_tuple
            signmethod = getattr(
                self,
                '_generate_%s_notify_sign' % signdescription.lower(),
                None
            )
            if signmethod is None:
                raise NotImplementedError(
                    "This type '%s' of sign is not implemented yet."
                    % signdescription)
            return signmethod
        return super(WapAlipay, self).get_sign_method(**kw)


def includeme(config):
    settings = config.registry.settings
    config.registry['alipay'] = Alipay(
        pid=settings.get('alipay.pid'),
        key=settings.get('alipay.key'),
        seller_email=settings.get('alipay.seller_email'))
