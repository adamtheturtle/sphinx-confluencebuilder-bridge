"""
Tests for the ``:confluence_mention:`` role.
"""

from collections.abc import Callable
from pathlib import Path
from textwrap import dedent

import pytest
from sphinx.errors import ExtensionError
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("html")
def test_confluence_mention(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``:confluence_mention:`` role renders like a link to a user profile.
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

        confluence_bridge_users = {
            "eloise.red": "1234a",
        }

        confluence_server_url = "https://example.com/wiki/"
        """,
    )
    conf_py.write_text(data=conf_py_content)

    source_file = source_directory / "index.rst"
    index_rst_template = dedent(
        text="""\
            {mention}
            """,
    )

    confluencebuilder_directive_source = dedent(
        text="""\
            :confluence_mention:`eloise.red`
            """,
    )

    docutils_directive_source = dedent(
        text="""\
            `@eloise.red <https://example.com/wiki/people/1234a>`_
            """,
    )

    source_file.write_text(
        data=index_rst_template.format(
            mention=confluencebuilder_directive_source,
        ),
    )

    app = make_app(srcdir=source_directory)
    app.build()
    assert app.statuscode == 0
    assert not app.warning.getvalue()

    confluencebuilder_directive_html = (app.outdir / "index.html").read_text()
    app.cleanup()

    source_file.write_text(
        data=index_rst_template.format(mention=docutils_directive_source),
    )
    app = make_app(srcdir=source_directory)
    app.build()
    assert app.statuscode == 0
    assert not app.warning.getvalue()

    docutils_directive_html = (app.outdir / "index.html").read_text()

    assert confluencebuilder_directive_html == docutils_directive_html


@pytest.mark.sphinx("html")
def test_mentioned_does_not_exist(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    An error is raised if the ``confluence_bridge_users`` configuration value
    does not contain the given user.
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

        confluence_bridge_users = {
        }

        confluence_server_url = "https://example.com/wiki/"
        """,
    )
    conf_py.write_text(data=conf_py_content)

    source_file = source_directory / "index.rst"
    index_rst_template = dedent(
        text="""\
            {mention}
            """,
    )

    confluencebuilder_directive_source = dedent(
        text="""\
            :confluence_mention:`eloise.red`
            """,
    )

    source_file.write_text(
        data=index_rst_template.format(
            mention=confluencebuilder_directive_source,
        ),
    )

    app = make_app(srcdir=source_directory)
    expected_regex = (
        "The user 'eloise.red' is not in the "
        "'confluence_bridge_users' configuration value."
    )
    with pytest.raises(
        expected_exception=ExtensionError,
        match=expected_regex,
    ):
        app.build()


@pytest.mark.sphinx("html")
def test_users_not_given(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    An error is raised if the ``confluence_bridge_users`` configuration value
    is not given.
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

        confluence_server_url = "https://example.com/wiki/"
        """,
    )
    conf_py.write_text(data=conf_py_content)

    source_file = source_directory / "index.rst"
    index_rst_template = dedent(
        text="""\
            {mention}
            """,
    )

    confluencebuilder_directive_source = dedent(
        text="""\
            :confluence_mention:`eloise.red`
            """,
    )

    source_file.write_text(
        data=index_rst_template.format(
            mention=confluencebuilder_directive_source,
        ),
    )

    app = make_app(srcdir=source_directory)
    expected_regex = (
        "The user 'eloise.red' is not in the "
        "'confluence_bridge_users' configuration value."
    )
    with pytest.raises(
        expected_exception=ExtensionError,
        match=expected_regex,
    ):
        app.build()


@pytest.mark.sphinx("html")
def test_server_url_not_given(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    The ``:confluence_mention:`` role renders like a link to a user profile.
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

        confluence_bridge_users = {
            "eloise.red": "1234a",
        }
        """,
    )
    conf_py.write_text(data=conf_py_content)

    source_file = source_directory / "index.rst"
    index_rst_template = dedent(
        text="""\
            {mention}
            """,
    )

    confluencebuilder_directive_source = dedent(
        text="""\
            :confluence_mention:`eloise.red`
            """,
    )

    source_file.write_text(
        data=index_rst_template.format(
            mention=confluencebuilder_directive_source,
        ),
    )

    app = make_app(srcdir=source_directory)
    expected_regex = (
        "The 'confluence_server_url' configuration value is required for the "
        "'confluence_mention' role."
    )
    with pytest.raises(
        expected_exception=ExtensionError,
        match=expected_regex,
    ):
        app.build()
