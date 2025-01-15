|Build Status| |codecov| |PyPI|

Sphinx Combine
==============

Extension for Sphinx which enables combining code blocks.

.. contents::

Installation
------------

``sphinx-combine`` is compatible with Sphinx 7.2.0+ using Python 3.10+.

.. code-block:: console

   $ pip install sphinx-combine

Setup
-----

Add the following to ``conf.py`` to enable the extension:

.. code-block:: python

   """Configuration for Sphinx."""

   extensions = ["sphinxcontrib.spelling"]  # Example existing extensions

   extensions += ["sphinx_combine"]

Using ``combined-code-block``
-----------------------------

The extension provides a new directive, ``combined-code-block``, which allows
you to combine multiple code blocks into a single code block.

The directive takes a language argument which is used to determine the syntax, as well as all options that the `code-block directive <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code-block>`_ supports.

Languages and options of code blocks within the directive are ignored.

.. code-block:: restructuredtext

   .. combined-code-block:: python

      .. literalinclude:: my_code.js
         :language: javascript

      .. code-block:: python

         """First code block."""

      .. code-block:: cpp

         // Second code block.

By default, there are no blank lines between the code blocks.
To add a blank line, use ``|``.

Contributing
------------

See `CONTRIBUTING.rst <./CONTRIBUTING.rst>`_.

.. |Build Status| image:: https://github.com/adamtheturtle/sphinx-combine/actions/workflows/ci.yml/badge.svg?branch=main
   :target: https://github.com/adamtheturtle/sphinx-combine/actions
.. _code-block: http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code-block
.. |codecov| image:: https://codecov.io/gh/adamtheturtle/sphinx-combine/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/adamtheturtle/sphinx-combine
.. |PyPI| image:: https://badge.fury.io/py/sphinx-combine.svg
   :target: https://badge.fury.io/py/sphinx-combine
