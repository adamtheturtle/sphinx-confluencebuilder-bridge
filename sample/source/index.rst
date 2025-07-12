Samples for Confluence directives
=================================

.. toctree::
   :hidden:

   other

Configuration
-------------

.. literalinclude:: conf.py
   :language: python

Supported directives
--------------------

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

``confluence_viewpdf``
~~~~~~~~~~~~~~~~~~~~~~

.. confluence_viewpdf:: _static/meta.pdf

Supported roles
---------------

``confluence_link``
~~~~~~~~~~~~~~~~~~~

`confluence_link <https://sphinxcontrib-confluencebuilder.readthedocs.io/en/stable/roles/#role-confluence_link>`_.

.. rest-example::

   :confluence_link:`https://www.bbc.co.uk`

``confluence_doc``
~~~~~~~~~~~~~~~~~~

`confluence_doc <https://sphinxcontrib-confluencebuilder.readthedocs.io/en/stable/roles/#role-confluence_doc>`_.

.. rest-example::

   .. This link works!

   :confluence_doc:`other`

``confluence_mention``
~~~~~~~~~~~~~~~~~~~~~~

.. rest-example::

   :confluence_mention:`eloise.red`
