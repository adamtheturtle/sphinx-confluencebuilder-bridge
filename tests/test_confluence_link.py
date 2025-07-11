"""
Tests for the ``:confluence_link:`` role.
"""

import json
from collections.abc import Callable
from pathlib import Path
from textwrap import dedent

from sphinx.testing.util import SphinxTestApp


def test_confluence_link(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``:confluence_link:`` role renders like a normal link.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    (source_directory / "conf.py").touch()

    source_file = source_directory / "index.rst"
    index_rst_template = dedent(
        text="""\
            {link}
            """,
    )

    confluencebuilder_role_source = dedent(
        text="""\
            :confluence_link:`https://www.bbc.co.uk`
            """,
    )

    docutils_role_source = dedent(
        text="""\
            `https://www.bbc.co.uk <https://www.bbc.co.uk>`_
            """,
    )

    source_file.write_text(
        data=index_rst_template.format(
            link=confluencebuilder_role_source,
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


def test_linkcheck(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    Links are checked by the ``linkcheck`` builder.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()
    (source_directory / "conf.py").touch()

    source_file = source_directory / "index.rst"
    index_rst_content = dedent(
        text="""\
            :confluence_link:`https://badlink.example.com`

            `https://badlink2.example.com <https://badlink2.example.com>`_
            """,
    )

    source_file.write_text(data=index_rst_content)

    app = make_app(
        srcdir=source_directory,
        buildername="linkcheck",
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
    assert not app.warning.getvalue()
    assert app.statuscode != 0
    output_json_lines = (app.outdir / "output.json").read_text().splitlines()
    expected_num_errors = 2
    assert len(output_json_lines) == expected_num_errors
    for line in output_json_lines:
        output_data = json.loads(s=line)
        assert output_data["status"] == "broken"
