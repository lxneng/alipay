An Unofficial Alipay API for Python
=======================================

.. image:: https://img.shields.io/travis/lxneng/alipay.svg
    :target: https://travis-ci.org/lxneng/alipay

.. image:: https://img.shields.io/pypi/v/alipay.svg
    :target: https://pypi.python.org/pypi/alipay/

.. image:: https://img.shields.io/pypi/dm/alipay.svg
    :target: https://pypi.python.org/pypi/alipay/

Overview
---------------------------------------

An Unofficial Alipay API for Python, It Contain these API:

- Generate direct payment url
- Generate partner trade payment url
- Generate standard mixed payment url
- Generate batch trans pay url
- Generate send goods confirm url
- Generate forex trade url
- Generate QR code url
- Verify notify
- Single Trade Query
- Generate Refund With Pwd URL

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

Generate standard mixed payment url
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..

    生成标准双接口支付链接

Introduction: https://b.alipay.com/order/productDetail.htm?productId=2012111300373136

.. code-block:: python

    >>> alipay.trade_create_by_buyer_url(**params)
    'https://mapi.alipay.com/gateway.do?seller_email=.....'

Generate batch trans pay url
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..

    生成批量付款链接

Introduction: https://b.alipay.com/order/productDetail.htm?productId=2012111200373121

.. code-block:: python

	>>> params = {
	... 'batch_list': (), #批量付款用户列表
	... 'account_name': 'seller_account_name', #卖家支付宝名称
	... 'batch_no': 'batch_id', #转账流水号，须唯一
	... 'notify_url': 'your_batch_notify_url' #异步通知地址
	... }
	>>> alipay.create_batch_trans_notify_url(**params)
	'https://mapi.alipay.com/gateway.do?seller_email=xxx&detail_data=....'

Note: batch_list 为批量付款用户列表，具体格式如下例子：(如涉及中文请使用unicode字符)

.. code-block:: python

	>>> batch_list = ({'account': 'test@xxx.com', #支付宝账号
	...                'name': u'测试', #支付宝用户姓名
	...                'fee': '100', #转账金额
	...                'note': 'test'},
	...               {'account': 'test@xxx.com', #支付宝账号
	...                'name': u'测试', #支付宝用户姓名
	...                'fee': '100', #转账金额
	...                'note': 'test'}) #转账原因

Generate send goods confirm url
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..

    生成确认发货链接

Introduction: https://cshall.alipay.com/support/help_detail.htm?help_id=491097

.. code-block:: python

    >>> params = {
    ... 'trade_no': 'your_alipay_trade_id',
    ... 'logistics_name': 'your_logicstic_name',
    ... 'transport_type': 'EXPRESS',
    ... 'invocie_no': 'your_invocie_no'
    ... }
    >>> alipay.send_goods_confirm_by_platform(**params)
    'https://mapi.alipay.com/gateway.do?sign=.....&trade_no=...'

Generate forex trade url
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..

    - Create website payment for foreigners (With QR code)
    - Create mobile payment for foreigners

Introduction: http://global.alipay.com/ospay/home.htm

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
    >>> # Create website payment for foreigners
    >>> alipay.create_forex_trade_url(**params)
    'https://mapi.alipay.com/gateway.do?service=create_forex_trade......'
    >>> # Create mobile payment for foreigners
    >>> alipay.create_forex_trade_wap_url(**params)
    'https://mapi.alipay.com/gateway.do?service=create_forex_trade_wap......'


Generate QR code url
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


Single Trade Query
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..

    单笔交易查询

文档：http://wenku.baidu.com/link?url=WLjyz-H6AlfDLIU7kR4LcVNQgxSTMxX61fW0tDCE8yZbqXflCd0CVFsZaIKbRFDvVLaFlq0Q3wcJ935A7Kw-mRSs0iA4wQu8cLaCe5B8FIq

.. code-block:: python

	import re
	xml = alipay.single_trade_query(out_trade_no="10000005")
	res = re.findall('<trade_status>(\S+)</trade_status>', xml) # use RE to find trade_status, xml parsing is more useful, in fact.
	status = None if not res else res[0]
	print status # will print out TRADE_SUCCESS when trade is success

Generate Refund With Pwd URL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..

    生成即时到账有密退款链接

Introduction: https://doc.open.alipay.com/docs/doc.htm?spm=a219a.7629140.0.0.XRddqH&treeId=62&articleId=104744&docType=1

.. code-block:: python

    >>> params = {
    ... 'batch_list': (), #批量退款数据集
    ... 'batch_no': 'batch_id', #退款批次号，须唯一
    ... 'notify_url': 'your_batch_notify_url' #异步通知地址
    ... }
    >>> alipay.refund_fastpay_by_platform_pwd(**params)
    'https://mapi.alipay.com/gateway.do?seller_email=xxx&detail_data=....'

Note: batch_list 为批量退款数据集，具体格式如下例子：(如涉及中文请使用unicode字符)

.. code-block:: python

    >>> batch_list = ({'trade_no': 'xxxxxxxx', #原付款支付宝交易号
    ...                'fee': '100', #退款总金额
    ...                'note': 'test'}, #退款原因
    ...               {'trade_no': 'xxxxxxxx', #原付款支付宝交易号
    ...                'fee': '100', #退款总金额
    ...                'note': 'test'}) #退款原因

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
