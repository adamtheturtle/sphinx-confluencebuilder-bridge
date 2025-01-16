"""
Tests for the ``:confluence_doc:`` role.
"""

from collections.abc import Callable
from pathlib import Path
from textwrap import dedent

import pytest
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("html")
def test_confluence_doc(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``confluence_doc`` role renders like a normal link to another document.
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
        """,
    )
    conf_py.write_text(data=conf_py_content)

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

    confluencebuilder_directive_source = dedent(
        text="""\
        :confluence_doc:`other`
        """,
    )

    docutils_directive_source = dedent(
        text="""\
        :doc:`other`
        """,
    )

    source_file.write_text(
        data=index_rst_template.format(
            link=confluencebuilder_directive_source,
        ),
    )

    app = make_app(srcdir=source_directory)
    app.build()
    assert app.statuscode == 0
    assert not app.warning.getvalue()

    confluencebuilder_directive_html = (app.outdir / "index.html").read_text()
    app.cleanup()

    source_file.write_text(
        data=index_rst_template.format(link=docutils_directive_source),
    )
    app = make_app(srcdir=source_directory)
    app.build()
    assert app.statuscode == 0
    assert not app.warning.getvalue()

    docutils_directive_html = (app.outdir / "index.html").read_text()

    assert confluencebuilder_directive_html == docutils_directive_html
