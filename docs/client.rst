.. _client:

Client requests
===============
As **Open-Needs Server** provides a REST API, a lot of libraries and tools can be used to access it.

This documentation is focusing on using `Python <https://python.org>`_
together with the `Requests <https://docs.python-requests.org/en/latest/>`_ library.

A complete API documentation (including curl based examples) is available by running **Open-Needs Server** and
accessing http://127.0.0.1:9595/docs or http://127.0.0.1:9595/redoc.


Example
-------
**Open-Needs Server** is using some predefined data for testing.
This data gets loaded via the REST-API and therefore is a good showcase, how API and Authentication are working.

You can find data and script in the repository under `/data/`.

The script can be executed with ``python data/install_data.py data/rocketlab.json``.
(An **Open-Needs Server** must be running!)


install_data.py
~~~~~~~~~~~~~~~

.. literalinclude:: ../data/install_data.py
   :language: python

