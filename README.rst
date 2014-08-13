python-gtbmm
============

A python library providing an interface to interact with the Guaranty Trust Bank Mobile Money service

Installing
==========

You can install python-gtbmm via `PyPi`_. To install the latest stable version::

  $ pip install python-gtbmmm

.. _PyPi: http://pypi.python.org/pypi/python-gtbmm

Usage
=====

Using python-gtbmm in your project is very easy::

  import gtbmm
  mm = gtbmm.GTBMobileMoney('2348012345678', '1111') # specify your account number and pin
  transactions = mm.history()
  result = mm.send('2348012345679', '1000') # send 1000 naira to 2348012345679

License
=======

python-gtbmm is free software, available under the BSD license.

Dependencies
============

* `lxml <http://lxml.de/>`_
* `Requests <http://docs.python-requests.org/en/latest/>`_
* `pytest <http://pytest.org/latest/>`_

Contributing
============

Please feel free to fork this project and submit pull requests. If you've found a bug, 
also feel free to fix it and submit a pull request. If you can't submit a patch, then 
report bugs by creating an issue on the `issue tracker`_.

.. _issue tracker: https://github.com/timbaobjects/python-gtbmm/issues
