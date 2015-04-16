An Unofficial Alipay API for Python
=======================================

.. image:: https://travis-ci.org/lxneng/alipay.png?branch=master
    :target: https://travis-ci.org/lxneng/alipay

.. image:: https://pypip.in/d/alipay/badge.png
    :target: https://crate.io/packages/alipay/

Overview
---------------------------------------

An Unofficial Alipay API for Python, It Contain these API:

- Generate direct payment url
- Generate partner trade payment url
- Generate Standard mixed payment url
- Verify notify

official document: https://b.alipay.com/order/techService.htm

Install
---------------------------------------

.. code-block:: bash

    pip install alipay

Usage
---------------------------------------

Initialization
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> from alipay import Alipay
    >>> alipay = Alipay(pid='your_alipay_pid', key='your_alipay_key', seller_email='your_seller_mail')

Or you can use `seller_id` instead of `seller_email`:

.. code-block:: python

    >>> alipay = Alipay(pid='your_alipay_pid', key='your_alipay_key', seller_id='your_seller_id')

Generate direct payment url
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..

    生成即时到账支付链接

Introduction: https://b.alipay.com/order/productDetail.htm?productId=2012111200373124

.. code-block:: python

	>>> alipay.create_direct_pay_by_user_url(out_trade_no='your_order_id', subject='your_order_subject', total_fee='100.0', return_url='your_order
	_return_url', notify_url='your_order_notify_url')
	'https://mapi.alipay.com/gateway.do?seller_email=.....'

Generate partner trade payment url
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..

    生成担保交易支付链接

Introduction: https://b.alipay.com/order/productDetail.htm?productId=2012111200373121

.. code-block:: python

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
	>>> alipay.create_partner_trade_by_buyer_url(**params)
	'https://mapi.alipay.com/gateway.do?seller_email=.....'

Generate Standard mixed payment url
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..

    生成标准双接口支付链接

Introduction: https://b.alipay.com/order/productDetail.htm?productId=2012111300373136

.. code-block:: python

	>>> alipay.trade_create_by_buyer_url(**params)
	'https://mapi.alipay.com/gateway.do?seller_email=.....'

Generate Creating QR code url
~~~~~~~~~~~~~~~~~~~

..

    生成创建 QR 码链接

Introduction: https://b.alipay.com/order/productDetail.htm?productId=2012120700377303

.. code-block:: python

    >>> alipay.add_alipay_qrcode_url(**params)
    'https://mapi.alipay.com/gateway.do?seller_id=.......'

Note: 如果你的 `biz_data` 中有 Unicode 字符，在 dumps 的时候需要把 `ensure_ascii` 设置为 `False`，即 :code:`json.dumps(d, ensure_ascii=False)` 否则会遇到错误


Verify notify
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

verify notify from alipay server, example in Pyramid Application

.. code-block:: python

    def alipy_notify(request):
    	alipay = request.registry['alipay']
    	if alipay.verify_notify(**request.params):
    		# this is a valid notify, code business logic here
    	else:
    	    # this is a invalid notify


Example in Pyramid Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Include alipay either by setting your includes in your .ini, or by calling config.include('alipay').

.. code-block:: python

	pyramid.includes = alipay

now in your View

.. code-block:: python

	def some_view(request):
		alipay = request.registry['alipay']
		url = alipay.create_direct_pay_by_user_url(...)


Reference
---------------------------------------

- `Ruby Alipay GEM <https://github.com/chloerei/alipay>`_
- `Official document <https://b.alipay.com/order/techService.htm>`_
