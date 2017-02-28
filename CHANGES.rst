Changelog
==============================


0.7.4 - Feb.28, 2017
--------------------------------

- add `refund_fastpay_by_platform_pwd` method
  https://github.com/lxneng/alipay/pull/26

0.7.3 - Dec.14, 2015
--------------------------------

- replace open() calls with io.open() for Python 3 compatibility,
  fix `UnicodeDecodeError`
- add `create_direct_pay_by_user_url` doc for Wap site


0.7.2 - Nov.1, 2015
--------------------------------

- add `single_trade_query` method
  https://github.com/lxneng/alipay/pull/20

0.7.1 - Sep.16, 2015
--------------------------------

- Fix verify_notify raise KeyError: 'sign' bug
  https://github.com/lxneng/alipay/pull/18

0.7 - Sep.07, 2015
--------------------------------

- add `create_forex_trade_url` method
- add `create_forex_trade_wap_url` method
- add `create_batch_trans_notify_url` method

0.6 - Jul.27, 2015
--------------------------------

- add `send_goods_confirm_by_platform` method

0.5 - Apr.16, 2015
--------------------------------

- add `add_alipay_qrcode` method

0.4.2 - Feb.14, 2015
--------------------------------

- Fix argument type error of verify_notify in README

- FIX SEVERE FAULT IN `check_notify_remotely`


0.4.1 - Feb.09, 2015
--------------------------------

- Resolved README.rst is not formatted on pypi.python.org

0.4 - Feb.09, 2015
--------------------------------

- Seller id support


0.3 - Aug.03, 2014
--------------------------------

- Add wap payment support

0.2.3 - Nov.20, 2013
--------------------------------

- english version readme doc

0.2.2 - Nov.12, 2013
--------------------------------

- add includeme func for pyramid

- update readme

0.2.1 - Nov.11, 2013
--------------------------------

- fix rst doc

0.2 - Nov.11, 2013
--------------------------------

- add unittest

- update readme

- add verify_notify func

- add check_parameters func

- add travis.yml

- add tox.ini

0.1 - Nov.11, 2013
------------------------------

- first commit
