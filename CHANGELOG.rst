Changelog
=========

.. contents::

.. towncrier release notes start

2026.08.16
----------

- Register the ``.. confluence_viewpdf::`` directive for all HTML output builders (e.g. ``dirhtml`` and ``singlehtml``), not only the ``html`` builder.

2026.01.12
----------


* Give version in extension metadata.
* Fix ``:confluence_mention:`` URLs when ``confluence_server_url`` has a custom context path.
  Users who previously omitted ``/wiki/`` from their ``confluence_server_url`` must now include it
  (e.g., ``https://example.com/wiki/`` instead of ``https://example.com/``).

2025.07.12.1
------------

2025.07.12
----------

2025.07.11.1
------------

2025.07.11
----------

2025.01.28
----------
