"""
Sample ``conf.py``.
"""

extensions = [
    "sphinxcontrib.confluencebuilder",
    "sphinx_confluencebuilder_bridge",
    "sphinx_toolbox.rest_example",
]

# We do Furo specific work, so we use the Furo theme.
html_theme = "furo"
