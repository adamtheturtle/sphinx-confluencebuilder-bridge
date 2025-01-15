Samples for Confluence directives
=================================

Configuration
-------------

.. literalinclude:: conf.py
   :language: python

Supported roles and directives
------------------------------

``confluence_toc``
~~~~~~~~~~~~~~~~~~

`confluence_toc <https://sphinxcontrib-confluencebuilder.readthedocs.io/en/stable/directives/#directive-confluence_toc>`_.

With no options
~~~~~~~~~~~~~~~

Source
^^^^^^

.. code-block:: rst

   .. confluence_toc::

Output
^^^^^^

.. confluence_toc::

With ``max-level`` option
~~~~~~~~~~~~~~~~~~~~~~~~~

The only supported option is `max-level <https://sphinxcontrib-confluencebuilder.readthedocs.io/en/stable/directives/#directive-option-confluence_toc-max-level>`_.

Source
^^^^^^

.. code-block:: rst

   .. confluence_toc::
      :max-level: 1

Output
^^^^^^

.. confluence_toc::
   :max-level: 1

``confluence_link``
~~~~~~~~~~~~~~~~~~~

`confluence_link <https://sphinxcontrib-confluencebuilder.readthedocs.io/en/stable/directives/#directive-confluence_link>`_.

.. rest-example::

   :confluence_link:`https://www.bbc.co.uk`
