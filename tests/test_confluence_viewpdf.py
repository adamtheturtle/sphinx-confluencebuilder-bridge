"""Tests for the ``..confluence_viewpdf::`` directive."""

import shutil
from collections.abc import Callable
from pathlib import Path
from textwrap import dedent

import pytest
from sphinx.testing.util import SphinxTestApp


def test_confluence_viewpdf(
    *,
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``..confluence_viewpdf::`` directive renders like a normal PDF
    link.
    """
    source_directory = tmp_path / "source"
    source_data_directory = source_directory / "data"
    source_data_directory.mkdir(parents=True)
    (source_directory / "conf.py").touch()
    pdf_path = Path(__file__).parent / "data" / "example.pdf"
    shutil.copyfile(
        src=pdf_path,
        dst=source_data_directory / "example.pdf",
    )

    source_file = source_directory / "index.rst"
    index_rst_template = dedent(
        text="""\
            {pdf}
            """,
    )

    confluencebuilder_directive_source = dedent(
        text="""\
            .. confluence_viewpdf:: data/example.pdf
            """,
    )

    docutils_directive_source = dedent(
        text="""\
            .. pdf-include:: data/example.pdf
            """,
    )

    source_file.write_text(
        data=index_rst_template.format(
            pdf=confluencebuilder_directive_source,
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
        data=index_rst_template.format(pdf=docutils_directive_source),
    )
    app = make_app(
        srcdir=source_directory,
        confoverrides={
            "extensions": [
                "sphinx_simplepdf",
            ],
        },
    )
    app.build()
    assert app.statuscode == 0
    assert not app.warning.getvalue()

    docutils_directive_html = (app.outdir / "index.html").read_text()

    assert confluencebuilder_directive_html == docutils_directive_html


@pytest.mark.parametrize(
    argnames="buildername",
    argvalues=["dirhtml", "singlehtml"],
)
def test_confluence_viewpdf_html_family_builders(
    *,
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
    buildername: str,
) -> None:
    """
    The ``..confluence_viewpdf::`` directive is available for HTML-
    family
    builders other than ``html`` (e.g. ``dirhtml`` and ``singlehtml``),
    which also produce HTML output and support ``iframe``.
    """
    source_directory = tmp_path / "source"
    source_data_directory = source_directory / "data"
    source_data_directory.mkdir(parents=True)
    (source_directory / "conf.py").touch()
    pdf_path = Path(__file__).parent / "data" / "example.pdf"
    shutil.copyfile(
        src=pdf_path,
        dst=source_data_directory / "example.pdf",
    )

    source_file = source_directory / "index.rst"
    source_file.write_text(
        data=dedent(
            text="""\
                .. confluence_viewpdf:: data/example.pdf
                """,
        ),
    )

    app = make_app(
        srcdir=source_directory,
        buildername=buildername,
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
