from typing import Any, Callable, Dict, Optional

from ..dependencies import register_component
from ..element import Element
from ..events import JoystickEventArguments, handle_event

register_component('joystick', __file__, 'joystick.vue', ['lib/nipplejs.min.js'])


class Joystick(Element):

    def __init__(self, *,
                 on_start: Optional[Callable[..., Any]] = None,
                 on_move: Optional[Callable[..., Any]] = None,
                 on_end: Optional[Callable[..., Any]] = None,
                 throttle: float = 0.05,
                 ** options: Any) -> None:
        """Joystick

        Create a joystick based on `nipple.js <https://yoannmoi.net/nipplejs/>`_.

        :param on_start: callback for when the user touches the joystick
        :param on_move: callback for when the user moves the joystick
        :param on_end: callback for when the user releases the joystick
        :param throttle: throttle interval in seconds for the move event (default: 0.05)
        :param options: arguments like `color` which should be passed to the `underlying nipple.js library <https://github.com/yoannmoinet/nipplejs#options>`_
        """
        super().__init__('joystick')
        self._props['options'] = options
        self.active = False

        def handle_start() -> None:
            self.active = True
            handle_event(on_start, JoystickEventArguments(sender=self,
                                                          client=self.client,
                                                          action='start'))

        def handle_move(msg: Dict) -> None:
            if self.active:
                handle_event(on_move, JoystickEventArguments(sender=self,
                                                             client=self.client,
                                                             action='move',
                                                             x=float(msg['args']['data']['vector']['x']),
                                                             y=float(msg['args']['data']['vector']['y'])))

        def handle_end() -> None:
            self.active = False
            handle_event(on_end, JoystickEventArguments(sender=self,
                                                        client=self.client,
                                                        action='end'))

        self.on('start', handle_start)
        self.on('move', handle_move, args=['data'], throttle=throttle),
        self.on('end', handle_end)
