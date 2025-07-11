"""Tests for the ``..confluence_viewpdf::`` directive."""

import shutil
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
    build_directory = tmp_path / "build"
    source_directory.mkdir()
    (source_directory / "conf.py").touch()
    pdf_path = Path(__file__).parent / "data" / "example.pdf"
    shutil.copyfile(
        src=pdf_path,
        dst=source_directory / "example.pdf",
    )
    (source_directory / "example.png").touch()

    source_file = source_directory / "index.rst"
    index_rst_template = dedent(
        text="""\
            {pdf}
            """,
    )

    confluencebuilder_directive_source = dedent(
        text="""\
            .. confluence_viewpdf:: example.pdf
            """,
    )

    docutils_directive_source = dedent(
        text="""\
            .. figure:: example.png
            """,
    )

    source_file.write_text(
        data=index_rst_template.format(
            pdf=confluencebuilder_directive_source,
        ),
    )

    app = make_app(
        srcdir=source_directory,
        builddir=build_directory,
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
    # Check that we do not pollute the source directory with generated files.
    assert set(source_directory.iterdir()) == {
        source_directory / "index.rst",
        source_directory / "conf.py",
        source_directory / "example.pdf",
        source_directory / "example.png",
    }

    confluencebuilder_directive_html = (app.outdir / "index.html").read_text()
    app.cleanup()

    source_file.write_text(
        data=index_rst_template.format(pdf=docutils_directive_source),
    )
    app = make_app(srcdir=source_directory)
    app.build()
    assert app.statuscode == 0
    assert not app.warning.getvalue()

    docutils_directive_html = (app.outdir / "index.html").read_text()

    assert confluencebuilder_directive_html == docutils_directive_html
