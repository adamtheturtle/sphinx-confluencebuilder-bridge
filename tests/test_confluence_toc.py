"""
Tests for the ``..confluence_toc::`` directive.
"""

from collections.abc import Callable
from pathlib import Path
from textwrap import dedent

import pytest
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("html")
def test_confluence_toc(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The table of contents directive renders like a normal table of contents.
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
    index_rst_template = dedent(
        text="""\
            Heading A
            =========

            Heading A.A
            -----------

            Some text

            Heading A.B
            -----------

            Some text

            {toc}

            Heading A.B.A
            ~~~~~~~~~~~~~

            Text

            Heading B
            =========

            Other
            """,
    )

    confluencebuilder_directive_source = dedent(
        text="""\
            .. confluence_toc::
            """,
    )

    docutils_directive_source = dedent(
        text="""\
            .. contents::
            :class: this-will-duplicate-information-and-it-is-still-useful-here
            """,
    )

    source_file.write_text(
        data=index_rst_template.format(
            toc=confluencebuilder_directive_source,
        ),
    )

    app = make_app(srcdir=source_directory)
    app.build()
    assert not app.warning.getvalue()

    confluencebuilder_directive_html = (app.outdir / "index.html").read_text()
    app.cleanup()

    source_file.write_text(
        data=index_rst_template.format(toc=docutils_directive_source),
    )
    app = make_app(srcdir=source_directory)
    app.build()
    assert not app.warning.getvalue()

    docutils_directive_html = (app.outdir / "index.html").read_text()

    assert confluencebuilder_directive_html == docutils_directive_html


@pytest.mark.sphinx("html")
def test_max_level(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The table of contents directive renders like a normal table of contents,
    even with a ``max-level``.
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
    index_rst_template = dedent(
        text="""\
            Heading A
            =========

            Heading A.A
            -----------

            Some text

            Heading A.B
            -----------

            Some text

            {toc}

            Heading A.B.A
            ~~~~~~~~~~~~~

            Text

            Heading B
            =========

            Other
            """,
    )

    confluencebuilder_directive_source = dedent(
        text="""\
            .. confluence_toc::
            :max-level: 1
            """,
    )

    docutils_directive_source = dedent(
        text="""\
            .. contents::
            :class: this-will-duplicate-information-and-it-is-still-useful-here
            :depth: 2
            """,
    )

    source_file.write_text(
        data=index_rst_template.format(
            toc=confluencebuilder_directive_source,
        ),
    )

    app = make_app(srcdir=source_directory)
    app.build()
    assert not app.warning.getvalue()

    confluencebuilder_directive_html = (app.outdir / "index.html").read_text()
    app.cleanup()

    source_file.write_text(
        data=index_rst_template.format(toc=docutils_directive_source),
    )
    app = make_app(srcdir=source_directory)
    app.build()
    assert not app.warning.getvalue()

    docutils_directive_html = (app.outdir / "index.html").read_text()

    assert confluencebuilder_directive_html == docutils_directive_html