.. _contribute:

Contributing
============

Dev Environment
---------------

Documentation build
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install -r requirements/docs.txt
   cd docs
   make html

Docker
~~~~~~

Build container via: ``docker build -t ons . ``

Start bash into container via: ``docker run -it --entrypoint  /bin/bash ons``
