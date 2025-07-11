"""Tests for the ``..confluence_viewpdf::`` directive."""

from collections.abc import Callable
from pathlib import Path
from textwrap import dedent

from sphinx.testing.util import SphinxTestApp


def test_confluence_viewpdf(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``..confluence_viewpdf::`` directive renders like a normal PDF link.
    """
    source_directory = tmp_path / "source"
    pdf_path = source_directory / "example.pdf"
    source_directory.mkdir()
    (source_directory / "conf.py").touch()

    source_file = source_directory / "index.rst"
    index_rst_template = dedent(
        text="""\
            {pdf}
            """,
    )

    confluencebuilder_directive_source = dedent(
        text=f"""\
            .. confluence_viewpdf:: {pdf_path}
            """,
    )

    docutils_directive_source = dedent(
        text=f"""\
            Inline view of :download:`example.pdf <{pdf_path}>`_
            """,
    )

    source_file.write_text(
        data=index_rst_template.format(
            link=confluencebuilder_directive_source,
        ),
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
