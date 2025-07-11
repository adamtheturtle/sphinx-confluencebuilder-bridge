"""
Tests for the ``:confluence_doc:`` role.
"""

from collections.abc import Callable
from pathlib import Path
from textwrap import dedent

from sphinx.testing.util import SphinxTestApp


def test_confluence_doc(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``confluence_doc`` role renders like a normal link to another document.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    (source_directory / "conf.py").touch()

    source_file = source_directory / "index.rst"
    linked_file = source_directory / "other.rst"
    linked_file_content = dedent(
        text="""\
        Other
        =====

        Some text
        """,
    )
    linked_file.write_text(data=linked_file_content)

    index_rst_template = dedent(
        text="""\
        {link}

        .. toctree::

            other
        """,
    )

    confluencebuilder_role_source = dedent(
        text="""\
        :confluence_doc:`other`
        """,
    )

    docutils_role_source = dedent(
        text="""\
        :doc:`other`
        """,
    )

    source_file.write_text(
        data=index_rst_template.format(link=confluencebuilder_role_source),
    )

    app = make_app(
        srcdir=source_directory,
        confoverrides={
            "extensions": [
                "sphinxcontrib.confluencebuilder",
                "sphinx_confluencebuilder_bridge",
            ],
        },
    )
    app.build()
    assert app.statuscode == 0
    assert not app.warning.getvalue()

    confluencebuilder_role_html = (app.outdir / "index.html").read_text()
    app.cleanup()

    source_file.write_text(
        data=index_rst_template.format(link=docutils_role_source),
    )
    app = make_app(srcdir=source_directory)
    app.build()
    assert app.statuscode == 0
    assert not app.warning.getvalue()

    docutils_role_html = (app.outdir / "index.html").read_text()

    assert confluencebuilder_role_html == docutils_role_html
