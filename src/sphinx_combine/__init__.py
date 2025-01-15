"""
Sphinx extension to combine multiple nested code-blocks into a single one.
"""

from docutils import nodes
from docutils.nodes import Node
from docutils.statemachine import StringList
from sphinx.application import Sphinx
from sphinx.directives.code import CodeBlock
from sphinx.util.typing import ExtensionMetadata


class CombinedCodeBlock(CodeBlock):
    """
    A Sphinx directive that merges multiple nested code blocks into a single
    literal block.
    """

    def run(self) -> list[Node]:
        """
        Parse the directive content (which may contain multiple code-blocks)
        and return a single merged code-block node.
        """
        container = nodes.container()
        self.state.nested_parse(  # pyright: ignore[reportUnknownMemberType]
            block=self.content,
            input_offset=self.content_offset,
            node=container,
        )

        new_content = StringList()
        for literal in container:
            code_snippet = literal.astext()
            new_item_string_list = StringList(initlist=[code_snippet])
            new_content.extend(other=new_item_string_list)

        self.content = new_content
        return super().run()


def setup(app: Sphinx) -> ExtensionMetadata:
    """
    Register the 'combined-code-block' directive with Sphinx.
    """
    app.add_directive(name="combined-code-block", cls=CombinedCodeBlock)
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
