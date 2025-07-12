|Build Status| |codecov| |PyPI|

Sphinx Confluence Builder Bridge
================================

Extension for Sphinx which enables using directives and roles from `Atlassian® Confluence® Builder for Sphinx <https://sphinxcontrib-confluencebuilder.readthedocs.io>`_ in other Sphinx builders such as HTML.
This enables you to use HTML builds for easy iteration while developing documentation which is primarily meant for Confluence.

.. contents::

Installation
------------

``sphinx-confluencebuilder-bridge`` is compatible with Python |minimum-python-version|\+.

.. code-block:: console

   $ pip install sphinx-confluencebuilder-bridge

Setup
-----

Add the following to ``conf.py`` to enable the extension:

.. code-block:: python

   """Configuration for Sphinx."""

   extensions = ["sphinxcontrib.confluencebuilder"]  # Example existing extensions

   extensions += [
       # This must come after ``"sphinxcontrib.confluencebuilder"``
       "sphinx_confluencebuilder_bridge"
   ]

Supported directives
--------------------

Only some of the `directives supported by Atlassian® Confluence® Builder for Sphinx <https://sphinxcontrib-confluencebuilder.readthedocs.io/directives>`_ are supported.
The following directives are supported:

* `confluence_toc <https://sphinxcontrib-confluencebuilder.readthedocs.io/en/stable/directives/#directive-confluence_toc>`_
   * The only supported option is `max-level <https://sphinxcontrib-confluencebuilder.readthedocs.io/en/stable/directives/#directive-option-confluence_toc-max-level>`_.

* ``confluence_viewpdf``
   * HTML builder only.
   * Requires the PDF to be in a directory specified in `html_static_path <https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_static_path>`_.

Supported roles
---------------

Only some of the `roles supported by Atlassian® Confluence® Builder for Sphinx <https://sphinxcontrib-confluencebuilder.readthedocs.io/roles>`_ are supported.
The following roles are supported:

* `confluence_link <https://sphinxcontrib-confluencebuilder.readthedocs.io/en/stable/roles/#role-confluence_link>`_
   * This renders as a normal hyperlink, unlike in Confluence where the page title is shown.
* `confluence_doc <https://sphinxcontrib-confluencebuilder.readthedocs.io/en/stable/roles/#role-confluence_doc>`_
   * This renders as a normal documentation link, unlike in Confluence where the page title is shown.
* `confluence_mention <https://sphinxcontrib-confluencebuilder.readthedocs.io/en/stable/roles/#role-confluence_mention>`_
   * This renders as a link with the text being the user's account identifier, user key or username.
   * For this to show a clear account identifier, set `confluence_mentions <https://sphinxcontrib-confluencebuilder.readthedocs.io/en/stable/configuration/#confval-confluence_mentions>`_ in ``conf.py``.

Contributing
------------

See `CONTRIBUTING.rst <./CONTRIBUTING.rst>`_.

.. |Build Status| image:: https://github.com/adamtheturtle/sphinx-confluencebuilder-bridge/actions/workflows/ci.yml/badge.svg?branch=main
   :target: https://github.com/adamtheturtle/sphinx-confluencebuilder-bridge/actions
.. |codecov| image:: https://codecov.io/gh/adamtheturtle/sphinx-confluencebuilder-bridge/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/adamtheturtle/sphinx-confluencebuilder-bridge
.. |PyPI| image:: https://badge.fury.io/py/sphinx-confluencebuilder-bridge.svg
   :target: https://badge.fury.io/py/sphinx-confluencebuilder-bridge
.. |minimum-python-version| replace:: 3.11
