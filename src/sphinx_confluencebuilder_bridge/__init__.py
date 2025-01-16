"""
Sphinx extension to enable using directives and roles from Atlassian
Confluence® Builder for Sphinx in other Sphinx builders such as HTML.
"""

from urllib.parse import urljoin

from docutils import nodes
from docutils.nodes import Node
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.parts import Contents
from docutils.parsers.rst.states import Inliner
from docutils.utils import SystemMessage
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.errors import ExtensionError
from sphinx.util.docfields import Field
from sphinx.util.typing import ExtensionMetadata


class _Contents(Contents):
    """A directive to put a table of contents in the page.

    Use this in place for the ``.. confluence_toc::`` directive, but they are
    not exactly the same. For example, the ``.. confluence_toc::`` directive
    does not render the page title.

    Using the ``:local:`` option with the ``.. confluence_toc::`` directive
    only renders the subsections of the current section, so we do not just use
    that.
    """

    option_spec = Contents.option_spec or {}
    option_spec["max-level"] = directives.nonnegative_int

    def run(self) -> list[Node]:
        """
        Run the directive.
        """
        # The ``depth`` option is used by the ``.. contents::`` directive,
        # while we use ``max-level`` for ``.. confluence_toc``..
        # Here we translate the ``max-level`` option to ``depth``.
        # We add 1 to the ``max-level`` option, as it includes the page title
        # in the HTML builder.
        #
        # The ``depth`` option has a default of "unlimited". See:
        # https://docutils.sourceforge.io/docs/ref/rst/directives.html#table-of-contents.
        default_depth = 1000
        depth = self.options.pop("max-level", default_depth) + 1
        self.options["depth"] = depth
        # In Confluence this directive shows and inline table of contents.
        # In the Furo HTML theme, the table of contents is shown in the
        # sidebar.
        # The Furo theme has a warning by default for the ``.. contents::``
        # directive.
        # We disable that warning for the ``.. confluence_toc::`` directive.
        self.options["class"] = [
            "this-will-duplicate-information-and-it-is-still-useful-here"
        ]
        return list(super().run())


def _link_role(
    # We allow multiple unused function arguments, to match the Sphinx API.
    role: str,
    rawtext: str,
    text: str,
    lineno: str,
    inliner: Inliner,
) -> tuple[list[Node], list[SystemMessage]]:
    """A role to create a link.

    Use this when the source uses ``confluence_link``, and we put in nodes
    which can be link checked.
    """
    del role
    del lineno
    del inliner
    link_text = text
    link_url = text
    node = nodes.reference(rawsource=rawtext, text=link_text, refuri=link_url)
    return [node], []


def _mention_role(
    # We allow multiple unused function arguments, to match the Sphinx API.
    role: str,
    rawtext: str,
    text: str,
    lineno: str,
    inliner: Inliner,
) -> tuple[list[Node], list[SystemMessage]]:
    """A role to create a mention link.

    On Confluence, mention links are rendered nicely with the user's
    full name, linking to their profile. For the HTML builder, we render
    a link with the user's user ID, linking to their profile.
    """
    del role
    del lineno
    link_text = f"@{text}"
    env: BuildEnvironment = inliner.document.settings.env  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    assert isinstance(env, BuildEnvironment)
    users: dict[str, str] = env.config.confluence_bridge_users
    server_url: str | None = env.config.confluence_server_url

    if server_url is None:
        message = (
            "The 'confluence_server_url' configuration value is required "
            "for the 'confluence_mention' role."
        )
        raise ExtensionError(message=message)

    if text not in users:
        message = (
            f"The user '{text}' is not in the 'confluence_bridge_users' "
            "configuration value."
        )
        raise ExtensionError(message=message)
    mention_id: str = users[text]
    link_url = urljoin(base=server_url, url=f"/wiki/people/{mention_id}")
    node = nodes.reference(rawsource=rawtext, text=link_text, refuri=link_url)
    return [node], []


def _doc_role(
    # We allow multiple unused function arguments, to match the Sphinx API.
    role: str,
    rawtext: str,
    text: str,
    lineno: str,
    inliner: Inliner,
) -> tuple[list[Node], list[SystemMessage]]:
    """
    This role acts just like the ``:doc:`` role, linking to other documents in
    this project.
    """
    del role
    del rawtext
    del lineno
    env: BuildEnvironment = inliner.document.settings.env  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    assert isinstance(env, BuildEnvironment)
    field = Field(name="")
    node = field.make_xref(rolename="doc", domain="std", target=text, env=env)
    return [node], []


def _connect_confluence_to_html_builder(app: Sphinx) -> None:
    """
    Allow ``sphinx-confluencebuilder`` directives and roles to be used with the
    HTML builder.
    """
    app.add_directive(name="confluence_toc", cls=_Contents)
    app.add_role(name="confluence_link", role=_link_role)
    app.add_role(name="confluence_doc", role=_doc_role)
    app.add_role(name="confluence_mention", role=_mention_role)
    app.add_config_value(
        name="confluence_bridge_users",
        default={},
        rebuild="",
        types=dict[str, str],
    )


def setup(app: Sphinx) -> ExtensionMetadata:
    """
    Allow ``sphinx-confluencebuilder`` directives and roles to be used with the
    HTML builder.
    """
    app.connect(
        event="builder-inited",
        callback=_connect_confluence_to_html_builder,
    )
    return {"parallel_read_safe": True, "parallel_write_safe": True}
