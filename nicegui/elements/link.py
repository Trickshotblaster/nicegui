from typing import Callable, Union

from .. import globals
from ..dependencies import register_component
from ..element import Element
from .mixins.text_element import TextElement

register_component('link', __file__, 'link.js')


class Link(TextElement):

    def __init__(self, text: str = '', target: Union[Callable, str] = '#', new_tab: bool = False) -> None:
        """Link

        Create a hyperlink.

        To jump to a specific location within a page you can place linkable anchors with `ui.link_target("name")`
        and link to it with `ui.link(target="#name")`.

        :param text: display text
        :param target: page function or string that is a an absolute URL or relative path from base URL
        :param new_tab: open link in new tab (default: False)
        """
        super().__init__(tag='link', text=text)
        self._props['href'] = target if isinstance(target, str) else globals.page_routes[target]
        self._props['target'] = '_blank' if new_tab else '_self'
        self._classes = ['nicegui-link']
        self._props['key'] = self.id  # HACK: workaround for #600


class LinkTarget(Element):

    def __init__(self, name: str) -> None:
        """Link target

        Create an anchor tag that can be used as inner-page target for links.

        :param name: target name
        """
        super().__init__('a')
        self._props['name'] = name
