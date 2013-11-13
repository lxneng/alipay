支付宝非官方Python API
=======================================

.. image:: https://travis-ci.org/lxneng/alipay.png?branch=master
   :target: https://travis-ci.org/lxneng/alipay

.. image:: https://pypip.in/d/alipay/badge.png
        :target: https://crate.io/packages/alipay/

介绍
---------------------------------------

支付宝非官方Python API

安装
---------------------------------------

::
    
    pip install alipay

用法
---------------------------------------

初始化
~~~~~~~~~~~~~~~~~~~~~~~

::

    >>> from alipay import Alipay
    >>> alipay = Alipay(pid='your_alipay_pid', key='your_alipay_key', seller_email='your_seller_mail')

生成即时到账支付链接
~~~~~~~~~~~~~~~~~~

::

	>>> alipay.create_direct_pay_by_user_url(out_trade_no='your_order_id', subject='your_order_subject', total_fee='100.0', return_url='your_order
	_return_url', notify_url='your_order_notify_url')
	'https://mapi.alipay.com/gateway.do?seller_email=.....'

生成担保交易支付链接
~~~~~~~~~~~~~~~~~~

::

	>>> params = {
	... 'out_trade_no': 'your_order_id',
	... 'subject': 'your_order_subject',
	... 'logistics_type': 'DIRECT',
	... 'logistics_fee': '0',
	... 'logistics_payment': 'SELLER_PAY',
	... 'price': '10.00',
	... 'quantity': '12',
	... 'return_url': 'your_order_return_url',
	... 'notify_url': 'your_order_notify_url'
	... }
	>>> alipay.create_direct_pay_by_user_url(**params)
	'https://mapi.alipay.com/gateway.do?seller_email=.....'

生成标准双接口支付链接
~~~~~~~~~~~~~~~~~~~~

::

	>>> alipay.trade_create_by_buyer_url(**params)
	'https://mapi.alipay.com/gateway.do?seller_email=.....'


集成到Pyramid项目中
~~~~~~~~~~~~~~~~~~~~

配置

::

	pyramid.includes = alipay

在View中取出alipay对象

::

	alipay = self.request.registry['alipay']


参考资料
---------------------------------------

- `ruby alipay gem <https://github.com/chloerei/alipay>`_

- `支付宝 API 向导（Ruby 版） <http://blog.chloerei.com/articles/51-alipay-payment-in-ruby>`_

- `官方文档 <https://b.alipay.com/order/techService.htm>`_
