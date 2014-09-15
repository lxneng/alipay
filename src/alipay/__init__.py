# -*- coding: utf-8 -*-
import requests
from hashlib import md5
from .exceptions import MissingParameter
from .exceptions import ParameterValueError
import six
import time
from collections import OrderedDict
if six.PY3:
    from urllib.parse import parse_qs, urlparse, unquote
else:
    from urlparse import parse_qs, urlparse, unquote
from xml.etree import ElementTree
from alipay.exceptions import TokenAuthorizationError

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

def encode_dict(params):
    return {k:six.u(v).encode('utf-8') if isinstance(v, str) else v.encode('utf-8') if isinstance(v, six.string_types) else v for k, v in six.iteritems(params)}

class Alipay(object):

    GATEWAY_URL = 'https://mapi.alipay.com/gateway.do'
    
    NOTIFY_GATEWAY_URL = 'https://mapi.alipay.com/gateway.do?service=notify_verify&partner=%s&notify_id=%s'
    sign_tuple = ('sign_type', 'MD5', 'MD5')

    def __init__(self, pid, key, seller_email):
        self.key = key
        self.pid = pid
        self.default_params = {'_input_charset': 'utf-8',
                               'partner': pid,
                               'seller_email': seller_email,
                               'payment_type': '1'}

    def _generate_md5_sign(self, params):
        src = '&'.join(['%s=%s' % (key, value) for key,
                        value in sorted(params.items())]) + self.key
        return md5(src.encode('utf-8')).hexdigest()

    def _check_params(self, params, names):
        if not all(k in params for k in names):
            raise MissingParameter('missing parameters')
        return

    def signKey(self):
        return False

    def _build_url(self, service, **kw):
        params = self.default_params.copy()
        params['service'] = service
        params.update(kw)
        signkey, signvalue, signdescription = self.sign_tuple
        signmethod = getattr(self, '_generate_%s_sign' % signdescription.lower())
        if signmethod == None:
            raise NotImplementedError("This type '%s' of sign is not implemented yet." % signdescription)
        if self.signKey():
            params.update({signkey: signvalue})
        params.update({signkey: signvalue,
                       'sign': signmethod(params)})

        return '%s?%s' % (self.GATEWAY_URL, urlencode(encode_dict(params)))

    def create_direct_pay_by_user_url(self, **kw):
        '''即时到帐'''
        self._check_params(kw, ['out_trade_no', 'subject'])

        if not kw.get('total_fee') and \
           not (kw.get('price') and kw.get('quantity')):
            raise ParameterValueError('total_fee or (price && quantiry)\
             must have one')

        url = self._build_url('create_direct_pay_by_user', **kw)
        return url

    def create_partner_trade_by_buyer_url(self, **kw):
        '''担保交易'''
        names = ['out_trade_no', 'subject', 'logistics_type',
                 'logistics_fee', 'logistics_payment', 'price', 'quantity']
        self._check_params(kw, names)
        url = self._build_url('create_partner_trade_by_buyer', **kw)
        return url

    def trade_create_by_buyer_url(self, **kw):
        '''标准双接口'''
        names = ['out_trade_no', 'subject', 'logistics_type',
                 'logistics_fee', 'logistics_payment', 'price', 'quantity']
        self._check_params(kw, names)

        url = self._build_url('trade_create_by_buyer', **kw)
        return url
    
    def getSignMethod(self, **kw):
        signkey, signvalue, signdescription = self.sign_tuple
        signmethod = getattr(self, '_generate_%s_sign' % signdescription.lower())
        if signmethod == None:
            raise NotImplementedError("This type '%s' of sign is not implemented yet." % signdescription)
        return signmethod

    def verify_notify(self, **kw):
        sign = kw.pop('sign')
        try:
            kw.pop('sign_type')
        except KeyError:
            pass
        signmethod = self.getSignMethod(**kw)
        if signmethod(kw) == sign:
            return self.checkNotifyRemotely(**kw)
        else:
            return False
        
    def checkNotifyRemotely(self, **kw):
        return requests.get(self.NOTIFY_GATEWAY_URL % (self.pid, kw['notify_id']), headers={'connection': 'close'}).text == 'true'
        
'''Wap支付接口'''
class WapAlipay(Alipay):
    GATEWAY_URL = 'http://wappaygw.alipay.com/service/rest.htm'
    TOKEN_ROOT_NODE = 'direct_trade_create_req'
    AUTH_ROOT_NODE = 'auth_and_execute_req'
    _xmlnode = '<%s>%s</%s>'
    sign_tuple = ('sec_id', 'MD5', 'MD5')

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
        names = ['subject', 'out_trade_no', 'total_fee', 'seller_account_name',
                 'call_back_url', ]
        self._check_params(kw, names)
        req_data = ''.join([self._xmlnode % (key, value, key) for (key, value) in six.iteritems(kw)])
        req_data = self._xmlnode %(self.TOKEN_ROOT_NODE, req_data, self.TOKEN_ROOT_NODE)
        if '&' in req_data:
            raise ParameterValueError('character \'&\' is not allowed.')
        params = {'req_data': req_data, 'req_id': time.time()}
        url = self._build_url('alipay.wap.trade.create.direct', **params)
        return url
    
    def create_direct_pay_by_user_url(self, **kw):
        '''即时到帐'''
        if 'token' not in kw:
            url = self.create_direct_pay_token_url(**kw)
            alipayres = requests.post(url, headers={'connection': 'close'}).text
            params = parse_qs(urlparse(alipayres).path, keep_blank_values=True)
            if 'res_data' in params:
                tree = ElementTree.ElementTree(ElementTree.fromstring(unquote(params['res_data'][0])))
                token = tree.find("request_token").text
            else:
                raise TokenAuthorizationError(unquote(params['res_error'][0]))
        else:
            token = kw['token']
        params = {'req_data': self._xmlnode %(self.AUTH_ROOT_NODE, (self._xmlnode %('request_token', token,'request_token')) , self.AUTH_ROOT_NODE)}
        url = self._build_url('alipay.wap.auth.authAndExecute', **params)
        return url
    
    def trade_create_by_buyer_url(self, **kw):
        raise NotImplementedError("This type of pay is not supported in wap.")
    
    def create_partner_trade_by_buyer_url(self, **kw):
        raise NotImplementedError("This type of pay is not supported in wap.")
    
    def signKey(self):
        return True
    
    def checkNotifyRemotely(self, **kw):
        if 'notify_data' in kw:
            notifydata = unquote(kw['notify_data'])
            notifydata = six.u(notifydata).encode('utf-8') if isinstance(notifydata, str) else notifydata.encode('utf-8') if isinstance(notifydata, six.string_types) else notifydata
            tree = ElementTree.ElementTree(ElementTree.fromstring(notifydata))
            return super(WapAlipay, self).checkNotifyRemotely(**{'notify_id': tree.find("notify_id").text})
        return True
    
    def _generate_md5_notify_sign(self, kw):
        newpara = OrderedDict()
        newpara['service'] = kw['service']
        newpara['v'] = kw['v']
        newpara['sec_id'] = kw['sec_id']
        newpara['notify_data'] = kw['notify_data']
        src = '&'.join(['%s=%s' % (key, value) for key,
                        value in newpara.items()]) + self.key
        return md5(src.encode('utf-8')).hexdigest()
    
    def getSignMethod(self, **kw):
        if 'notify_data' in kw:
            signkey, signvalue, signdescription = self.sign_tuple
            signmethod = getattr(self, '_generate_%s_notify_sign' %(signdescription.lower()))
            if signmethod == None:
                raise NotImplementedError("This type '%s' of sign is not implemented yet." %(signdescription))
            return signmethod
        return super(WapAlipay, self).getSignMethod(**kw)

def includeme(config):
    settings = config.registry.settings
    config.registry['alipay'] = Alipay(
        pid=settings.get('alipay.pid'),
        key=settings.get('alipay.key'),
        seller_email=settings.get('alipay.seller_email'))
