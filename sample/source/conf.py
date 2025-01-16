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

confluence_bridge_users = {
    "eloise.red": "1234a",
}

confluence_server_url = "https://example.com/wiki/"
