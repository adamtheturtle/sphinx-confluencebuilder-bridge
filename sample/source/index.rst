Samples for Confluence directives
=================================

Configuration
-------------

.. literalinclude:: conf.py
   :language: python

Supported roles
---------------

`confluence_toc <https://sphinxcontrib-confluencebuilder.readthedocs.io/en/stable/directives/#directive-confluence_toc>`_.

The only supported option is `max-level <https://sphinxcontrib-confluencebuilder.readthedocs.io/en/stable/directives/#directive-option-confluence_toc-max-level>`_.

Source
~~~~~~

.. code-block::

   .. confluence_toc::
      :max-level: 0

Output
~~~~~~

.. confluence_toc::
   :max-level: 0
