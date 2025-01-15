Samples for combining blocks
============================

Configuration
-------------

.. literalinclude:: conf.py
   :language: python

``combined-code-block``
-----------------------

.. combined-code-block:: python

    .. literalinclude:: conf.py
       :language: python

    .. code-block:: python

       """First code block."""

    |

    .. code-block:: python

       """Second code block, after a blank line."""

    .. code-block:: python

       """Third code block, with no blank line."""
