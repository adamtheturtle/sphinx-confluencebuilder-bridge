|Build Status| |codecov| |PyPI|

Sphinx Confluence Builder Bridge
================================

Extension for Sphinx which enables using directives and roles from `Atlassian® Confluence® Builder for Sphinx <https://sphinxcontrib-confluencebuilder.readthedocs.io>`_ in other Sphinx builders such as HTML.

.. contents::

Installation
------------

``sphinx-confluencebuilder-bridge`` is compatible with Sphinx 7.2.0+ using Python 3.10+.

.. code-block:: console

   $ pip install sphinx-confluencebuilder-bridge

Setup
-----

Add the following to ``conf.py`` to enable the extension:

.. code-block:: python

   """Configuration for Sphinx."""

   extensions = ["sphinxcontrib.confluencebuilder"]  # Example existing extensions

   extensions += ["sphinx_confluencebuilder_bridge"]

Contributing
------------

See `CONTRIBUTING.rst <./CONTRIBUTING.rst>`_.

.. |Build Status| image:: https://github.com/adamtheturtle/sphinx-confluencebuilder-bridge/actions/workflows/ci.yml/badge.svg?branch=main
   :target: https://github.com/adamtheturtle/sphinx-confluencebuilder-bridge/actions
.. _code-block: http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code-block
.. |codecov| image:: https://codecov.io/gh/adamtheturtle/sphinx-confluencebuilder-bridge/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/adamtheturtle/sphinx-confluencebuilder-bridge
.. |PyPI| image:: https://badge.fury.io/py/sphinx-confluencebuilder-bridge.svg
   :target: https://badge.fury.io/py/sphinx-confluencebuilder-bridge
