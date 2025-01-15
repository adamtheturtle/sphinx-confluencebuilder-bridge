"""
Tests for Sphinx extensions.
"""

from collections.abc import Callable
from pathlib import Path
from textwrap import dedent

import pytest
from sphinx.testing.util import SphinxTestApp


class TestConfluenceTOC:
    """Tests for the ``..

    confluence_toc::`` directive.
    """

    @pytest.mark.sphinx("html")
    def test_confluence_toc(
        self, tmp_path: Path, make_app: Callable[..., SphinxTestApp]
    ) -> None:
        """
        The table of contents directive renders like a normal table of
        contents.
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
             {toc}

             A
             =

             B
             -

             Some text

             C
             -

             Some text

             A2
             ==

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
             """,  # noqa: E501
        )

        source_file.write_text(
            data=index_rst_template.format(
                toc=confluencebuilder_directive_source,
            ),
        )

        app = make_app(srcdir=source_directory)
        app.build()
        assert not app.warning.getvalue()

        confluencebuilder_directive_html = (
            app.outdir / "index.html"
        ).read_text()
        app.cleanup()

        source_file.write_text(
            data=index_rst_template.format(toc=docutils_directive_source),
        )
        app = make_app(srcdir=source_directory)
        app.build()
        assert not app.warning.getvalue()

        docutils_directive_html = (app.outdir / "index.html").read_text()

        assert confluencebuilder_directive_html == docutils_directive_html
