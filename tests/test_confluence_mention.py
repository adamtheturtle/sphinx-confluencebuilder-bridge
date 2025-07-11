"""
Tests for the ``:confluence_mention:`` role.
"""

from collections.abc import Callable
from pathlib import Path
from textwrap import dedent

import pytest
from sphinx.errors import ExtensionError
from sphinx.testing.util import SphinxTestApp


def test_confluence_mention_with_user_id(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``:confluence_mention:`` role renders like a link to a user ID when
    using an identifier not set in ``confluence_mentions``.
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
            :confluence_mention:`1234a`
            """,
    )

    docutils_role_source = dedent(
        text="""\
            `@1234a <https://example.com/wiki/people/1234a>`_
            """,
    )

    source_file.write_text(
        data=index_rst_template.format(
            mention=confluencebuilder_role_source,
        ),
    )

    app = make_app(
        srcdir=source_directory,
        confoverrides={
            "extensions": [
                "sphinxcontrib.confluencebuilder",
                "sphinx_confluencebuilder_bridge",
            ],
            "confluence_server_url": "https://example.com/wiki/",
        },
    )
    app.build()
    assert app.statuscode == 0
    assert not app.warning.getvalue()

    confluencebuilder_role_html = (app.outdir / "index.html").read_text()
    app.cleanup()

    source_file.write_text(
        data=index_rst_template.format(mention=docutils_role_source),
    )
    app = make_app(srcdir=source_directory)
    app.build()
    assert app.statuscode == 0
    assert not app.warning.getvalue()

    docutils_role_html = (app.outdir / "index.html").read_text()

    assert confluencebuilder_role_html == docutils_role_html


def test_confluence_mention_with_user_identifier(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``:confluence_mention:`` role renders like a link to a user profile
    when using an identifier set in ``confluence_mentions``.
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

    docutils_role_source = dedent(
        text="""\
            `@eloise.red <https://example.com/wiki/people/1234a>`_
            """,
    )

    source_file.write_text(
        data=index_rst_template.format(
            mention=confluencebuilder_role_source,
        ),
    )

    app = make_app(
        srcdir=source_directory,
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

    confluencebuilder_role_html = (app.outdir / "index.html").read_text()
    app.cleanup()

    source_file.write_text(
        data=index_rst_template.format(mention=docutils_role_source),
    )
    app = make_app(srcdir=source_directory)
    app.build()
    assert app.statuscode == 0
    assert not app.warning.getvalue()

    docutils_role_html = (app.outdir / "index.html").read_text()

    assert confluencebuilder_role_html == docutils_role_html


def test_confluence_mention_with_user_identifier_not_in_mentions(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``:confluence_mention:`` role assumes that if a user identifier is not
    in the me when using an identifier set in ``confluence_mentions``.
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

    docutils_role_source = dedent(
        text="""\
            `@eloise.red <https://example.com/wiki/people/eloise.red>`_
            """,
    )

    source_file.write_text(
        data=index_rst_template.format(
            mention=confluencebuilder_role_source,
        ),
    )

    app = make_app(
        srcdir=source_directory,
        confoverrides={
            "extensions": [
                "sphinxcontrib.confluencebuilder",
                "sphinx_confluencebuilder_bridge",
            ],
            "confluence_mentions": {},
            "confluence_server_url": "https://example.com/wiki/",
        },
    )
    app.build()
    assert app.statuscode == 0
    assert not app.warning.getvalue()

    confluencebuilder_role_html = (app.outdir / "index.html").read_text()
    app.cleanup()

    source_file.write_text(
        data=index_rst_template.format(mention=docutils_role_source),
    )
    app = make_app(srcdir=source_directory)
    app.build()
    assert app.statuscode == 0
    assert not app.warning.getvalue()

    docutils_role_html = (app.outdir / "index.html").read_text()

    assert confluencebuilder_role_html == docutils_role_html


def test_server_url_not_given(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``:confluence_mention:`` role renders like a link to a user profile.
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
        confoverrides={
            "extensions": [
                "sphinxcontrib.confluencebuilder",
                "sphinx_confluencebuilder_bridge",
            ],
            "confluence_mentions": {
                "eloise.red": "1234a",
            },
        },
    )
    expected_regex = (
        "The 'confluence_server_url' configuration value is required for the "
        "'confluence_mention' role."
    )
    with pytest.raises(
        expected_exception=ExtensionError,
        match=expected_regex,
    ):
        app.build()
