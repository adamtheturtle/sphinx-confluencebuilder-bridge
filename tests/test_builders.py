"""
Tests for using various builders.
"""

from collections.abc import Callable
from pathlib import Path
from textwrap import dedent

from sphinx.testing.util import SphinxTestApp


def test_not_html(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The roles and directives workfor non-HTML builders.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()

    conf_py = source_directory / "conf.py"
    conf_py_content = dedent(
        text="""\
        extensions = [
            "sphinxcontrib.confluencebuilder",
            "sphinx_confluencebuilder_bridge",
        ]

        confluence_bridge_users = {
            "eloise.red": "1234a",
        }

        confluence_server_url = "https://example.com/wiki"
        """,
    )
    conf_py.write_text(data=conf_py_content)

    source_file = source_directory / "index.rst"
    index_rst_template = dedent(
        text="""\
            {mention}
            """,
    )

    confluencebuilder_directive_source = dedent(
        text="""\
            :confluence_mention:`eloise.red`

            :confluence_link:`https://www.bbc.co.uk`
            """,
    )

    docutils_directive_source = dedent(
        text="""\
            `@eloise.red <https://example.com/wiki/people/1234a>`_

            `https://www.bbc.co.uk <https://www.bbc.co.uk>`_
            """,
    )

    source_file.write_text(
        data=index_rst_template.format(
            mention=confluencebuilder_directive_source,
        ),
    )

    app = make_app(srcdir=source_directory, buildername="text")
    app.build()
    assert not app.warning.getvalue()

    confluencebuilder_directive_html = (
        app.outdir.parent / "text" / "index.txt"
    ).read_text()
    app.cleanup()

    source_file.write_text(
        data=index_rst_template.format(mention=docutils_directive_source),
    )
    app = make_app(srcdir=source_directory)
    app.build()
    assert not app.warning.getvalue()

    docutils_directive_html = (
        app.outdir.parent / "text" / "index.txt"
    ).read_text()

    assert confluencebuilder_directive_html == docutils_directive_html
