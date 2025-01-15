"""
Tests for Sphinx extensions.
"""

from collections.abc import Callable
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING

import pytest
from bs4 import BeautifulSoup
from sphinx.testing.util import SphinxTestApp

if TYPE_CHECKING:
    from bs4.element import ResultSet, Tag


@pytest.mark.sphinx("html")
@pytest.mark.parametrize(
    argnames=("language_arguments", "parent_classes"),
    argvalues=[
        (("python",), ["highlight-python", "notranslate"]),
        ((), ["highlight-default", "notranslate"]),
    ],
)
def test_combine_code_blocks(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
    language_arguments: tuple[str, ...],
    parent_classes: list[str],
) -> None:
    """
    Test that 'combined-code-block' directive merges multiple code blocks into
    one single code block.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()

    conf_py = source_directory / "conf.py"
    conf_py_content = dedent(
        text="""\
        extensions = ['sphinx_combine']
        """,
    )
    conf_py.write_text(data=conf_py_content)

    source_file = source_directory / "index.rst"
    joined_language_arguments = " ".join(language_arguments)
    index_rst_content = dedent(
        text=f"""\
        Testing Combined Code Blocks
        ============================

        .. combined-code-block:: {joined_language_arguments}

           .. code-block::

               print("Hello from snippet one")

           .. code-block::

               print("Hello from snippet two")
        """
    )
    source_file.write_text(data=index_rst_content)

    app = make_app(srcdir=source_directory)
    app.build()
    assert not app.warning.getvalue()

    html_output = source_directory / "_build" / "html" / "index.html"
    html_content = html_output.read_text(encoding="utf-8")

    soup = BeautifulSoup(markup=html_content, features="html.parser")

    code_divs: ResultSet[Tag] = soup.find_all(name="div", class_="highlight")

    (code_div,) = code_divs
    code_block_text = code_div.get_text()
    assert "Hello from snippet one" in code_block_text
    assert "Hello from snippet two" in code_block_text

    # The given language influences the highlighting.
    parent_div = code_div.parent
    assert parent_div is not None
    assert parent_div["class"] == parent_classes


@pytest.mark.sphinx("html")
def test_combine_code_blocks_multiple_arguments(
    tmp_path: Path,
    make_app: Callable[..., SphinxTestApp],
) -> None:
    """
    Test that 'combined-code-block' directive raises an error if multiple
    language arguments are supplied.
    """
    source_directory = tmp_path / "source"
    source_directory.mkdir()

    conf_py = source_directory / "conf.py"
    conf_py_content = dedent(
        text="""\
        extensions = ['sphinx_combine']
        """,
    )
    conf_py.write_text(data=conf_py_content)

    source_file = source_directory / "index.rst"
    index_rst_content = dedent(
        text="""\
        Testing Combined Code Blocks
        ============================

        .. combined-code-block:: python css

            .. code-block::

                print("Hello from snippet one")

            .. code-block::

                print("Hello from snippet two")
        """
    )
    source_file.write_text(data=index_rst_content)

    app = make_app(srcdir=source_directory)
    app.build()
    expected_error = dedent(
        text="""\
        ERROR: Error in "combined-code-block" directive:
        maximum 1 argument(s) allowed, 2 supplied.
        """,
    )
    assert expected_error in app.warning.getvalue()
