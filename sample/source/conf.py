"""Sample ``conf.py``."""

# Sphinx requires lowercase names for its configuration settings.
# pylint: disable=invalid-name

extensions = [
    "sphinxcontrib.confluencebuilder",
    "sphinx_confluencebuilder_bridge",
    "sphinx_toolbox.rest_example",
]

# We do Furo specific work, so we use the Furo theme.
html_theme = "furo"
html_theme_options = {
    "source_repository": "https://github.com/adamtheturtle/sphinx-confluencebuilder-bridge/",
    "source_branch": "main",
    "source_directory": "sample/source/",
}

html_static_path = ["_static"]

confluence_mentions = {
    "eloise.red": "1234a",
}

confluence_server_url = "https://example.com/wiki/"
