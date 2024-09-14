from ursina import *


class RadioButton(Button):
    def __init__(self, start_state=False, **kwargs):
        super().__init__(start_state=start_state, state=start_state, radius=.5, scale=(.25, .25), color=color.black33, origin_z=0)
        self.default_model = None

        for key, value in kwargs.items():
            setattr(self, key, value)

        if 'color' in kwargs:
            setattr(self, 'color', kwargs['color'])

        if RadioButton.default_model is None:
            if not 'model' in kwargs:
                self.model = Quad(radius=.5)
        else:
            self.model = RadioButton.default_model

        def _active():
            self.state = not self.state
            if self.state is True:
                self.active.color = self.color.tint(-.2)
                self.active.highlight_color = self.color.tint(-.2)
            elif self.state is False:
                self.active.highlight_color = color.blue

        self.active = Button(radius=.5, scale=(self.scale[0] - .035, self.scale[1] - .035), z=-1, color=color.blue)

        self.active.on_click = _active

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        print(value)
        self.active.color = color.blue

    def on_click(self):
        self.state = not self.state

    def on_mouse_enter(self):
        if hasattr(self, 'tooltip'):
            self.tooltip.enabled = True

        self.highlight_color = color.black33

    def on_mouse_exit(self):
        if hasattr(self, 'tooltip'):
            self.tooltip.enabled = False


if __name__ == "__main__":
    app = Ursina()

    RadioButton(scale=.2, color=color.black33)

    app.run()