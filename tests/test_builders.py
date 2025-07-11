"""
Tests for using various builders.
"""

from collections.abc import Callable
from pathlib import Path
from textwrap import dedent

import pytest
from sphinx.testing.util import SphinxTestApp


def test_not_html(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The roles and directives work for non-HTML builders.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    (source_directory / "conf.py").touch()

    source_file = source_directory / "index.rst"
    index_rst_template = dedent(
        text="""\
            {mention}
            """,
    )

    confluencebuilder_role_source = dedent(
        text="""\
            :confluence_mention:`eloise.red`

            :confluence_link:`https://www.bbc.co.uk`
            """,
    )

    docutils_role_source = dedent(
        text="""\
            `@eloise.red <https://example.com/wiki/people/1234a>`_

            `https://www.bbc.co.uk <https://www.bbc.co.uk>`_
            """,
    )

    source_file.write_text(
        data=index_rst_template.format(
            mention=confluencebuilder_role_source,
        ),
    )

    app = make_app(
        srcdir=source_directory,
        buildername="text",
        confoverrides={
            "extensions": [
                "sphinxcontrib.confluencebuilder",
                "sphinx_confluencebuilder_bridge",
            ],
            "confluence_mentions": {
                "eloise.red": "1234a",
            },
            "confluence_server_url": "https://example.com/wiki/",
        },
    )
    app.build()
    assert app.statuscode == 0
    assert not app.warning.getvalue()

    confluencebuilder_directive_html = (
        app.outdir.parent / "text" / "index.txt"
    ).read_text()
    app.cleanup()

    source_file.write_text(
        data=index_rst_template.format(mention=docutils_role_source),
    )
    app = make_app(srcdir=source_directory)
    app.build()
    assert app.statuscode == 0
    assert not app.warning.getvalue()

    docutils_directive_html = (
        app.outdir.parent / "text" / "index.txt"
    ).read_text()

    assert confluencebuilder_directive_html == docutils_directive_html


@pytest.mark.parametrize(
    argnames="buildername",
    argvalues=["spelling", "confluence", "linkcheck"],
)
def test_translatable_builders(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
    buildername: str,
) -> None:
    """
    The roles and directives do not break the builders with "translator"s.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    (source_directory / "conf.py").touch()

    source_file = source_directory / "index.rst"
    index_rst_template = dedent(
        text="""\
            {mention}
            """,
    )

    confluencebuilder_role_source = dedent(
        text="""\
            :confluence_mention:`eloise.red`
            """,
    )

    source_file.write_text(
        data=index_rst_template.format(
            mention=confluencebuilder_role_source,
        ),
    )

    app = make_app(
        srcdir=source_directory,
        buildername=buildername,
        confoverrides={
            "extensions": [
                "sphinxcontrib.spelling",
                "sphinxcontrib.confluencebuilder",
                "sphinx_confluencebuilder_bridge",
            ],
            "confluence_mentions": {
                "eloise.red": "1234a",
            },
            "confluence_server_url": "https://example.com/wiki/",
        },
    )
    app.build()
    assert app.statuscode == 0
    assert not app.warning.getvalue()
    app.cleanup()
