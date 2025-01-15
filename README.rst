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

Supported directives
--------------------

Only some of the `directives supported by Atlassian® Confluence® Builder for Sphinx <https://sphinxcontrib-confluencebuilder.readthedocs.io/directives>`_ are supported.
The following directives are supported:

* `confluence_toc <https://sphinxcontrib-confluencebuilder.readthedocs.io/en/stable/directives/#directive-confluence_toc>`_.
   * The only supported option is `max-level <https://sphinxcontrib-confluencebuilder.readthedocs.io/en/stable/directives/#directive-option-confluence_toc-max-level>`_.
* `confluence_link <https://sphinxcontrib-confluencebuilder.readthedocs.io/en/stable/directives/#directive-confluence_link>`_.
   * No options are supported.
   * This renders as a normal hyperlink, unlike in Confluence where the page title is shown.

Contributing
------------

See `CONTRIBUTING.rst <./CONTRIBUTING.rst>`_.

.. |Build Status| image:: https://github.com/adamtheturtle/sphinx-confluencebuilder-bridge/actions/workflows/ci.yml/badge.svg?branch=main
   :target: https://github.com/adamtheturtle/sphinx-confluencebuilder-bridge/actions
.. |codecov| image:: https://codecov.io/gh/adamtheturtle/sphinx-confluencebuilder-bridge/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/adamtheturtle/sphinx-confluencebuilder-bridge
.. |PyPI| image:: https://badge.fury.io/py/sphinx-confluencebuilder-bridge.svg
   :target: https://badge.fury.io/py/sphinx-confluencebuilder-bridge
