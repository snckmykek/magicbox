from kivy.clock import Clock
from kivy.factory import Factory
from kivy.properties import ObjectProperty


class LongpressButton(Factory.Button):
    """This object helps to use long and short clicks. Just use it with multiple inheritance
    on_short_press for short press, on_long_press - for long, long_press_time - seconds to long press"""

    _clockev = ObjectProperty
    __events__ = ('on_long_press', 'on_short_press')
    is_short_press = False

    long_press_time = Factory.NumericProperty(.3)

    def on_state(self, instance, value):
        if value == 'down':
            self.is_short_press = True
            lpt = self.long_press_time
            self._clockev = Clock.schedule_once(self._do_long_press, lpt)
        else:
            self._clockev.cancel()
            if self.is_short_press:
                self._do_short_press()

    def _do_long_press(self, dt):
        self.is_short_press = False
        self.dispatch('on_long_press')

    def on_long_press(self, *largs):
        pass

    def _do_short_press(self):
        self.dispatch('on_short_press')

    def on_short_press(self, *largs):
        pass
