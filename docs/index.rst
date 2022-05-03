Open-Needs Server
=================

.. image:: /_static/open-needs-server-logo.png
   :align: center

**Open-Needs Server** is a REST-API based server for handling life-cycle objects of any kind.
It provides functions for configuration, validation and presentation of stored life cycle objects.

It can be used as central database for tools like `Sphinx-Needs <https://sphinx-needs.com>`_ and
data from processes like **SW Development**, **Toolchain classifications**, **SW Architecture**, **Safety
Analysis** and much more.

**Open-Needs Server** is completely flexible and can be adapted to any user specific needs.
Its functionality can be enhanced by using available or self-written extensions, to **check process constrains**,
**analyse data** or **validate inputs**.

**Open-Needs Server** belongs to the **Open-Needs** community, which creates and
maintains Open-Source tools for life-cycle processes inside docs-as-code toolchain environments.

.. warning::

   **Open-Needs Server** is still in the **alpha phase** and APIs may change in future.

Quickstart
----------

1. Install Open-Needs Server: ``pip install open-needs-server``.
2. Run server from command line: ``ons``
3. Open browser: http://127.0.0.1:9595


For more details please read the pages :ref:`install` or :ref:`config`.

Screenshots
-----------

.. md-tab-set::

   .. md-tab-item:: Start page

      .. image:: /_static/screenshots/start.png
         :align: center

   .. md-tab-item:: Admin Panel

      .. image:: /_static/screenshots/admin_panel_1.png
         :align: center

      |

      .. image:: /_static/screenshots/admin_panel_2.png
         :align: center

   .. md-tab-item:: Swagger Docs

      .. image:: /_static/screenshots/swagger_1.png
         :align: center

      |

      .. image:: /_static/screenshots/swagger_2.png
         :align: center

   .. md-tab-item:: Redoc Docs

      .. image:: /_static/screenshots/redoc.png
         :align: center



Sitemap
-------

.. toctree::

   installation
   configuration
   client
   contributing
   changelog
   license
