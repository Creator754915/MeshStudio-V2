from ursina import *
from ursina import color as clr


class ClickPanel(Button):
    def __init__(self, scale=(0.3, 0.5), radius=0.01, color=color.black66, visible=False, position=(999, 999),
                 key_control=True,
                 key_bind="right mouse",
                 button_text="Button1",
                 button2_text="Button2",
                 button3_text="Button3",
                 button4_text="Button4",
                 button5_text="Button5",
                 button6_text="Button6",
                 **kwargs):
        super().__init__(paren=camera.ui, model=Quad(radius=radius), scale=scale, color=color, visible=visible,
                         key_control=key_control,
                         key_bind=key_bind,
                         position=position, z=0,
                         button_text=button_text,
                         button2_text=button2_text,
                         button3_text=button3_text,
                         button4_text=button4_text,
                         button5_text=button5_text,
                         button6_text=button6_text)

        if 'color' in kwargs:
            setattr(self, 'color', kwargs['color'])
        self.highlight_color = self.color.tint(.01)
        self.pressed_color = self.color.tint(-.2)
        self.highlight_scale = 1
        self.pressed_scale = 1

        scale_btn = (1, 0.12)

        # for i in range(5):
        # c += .14
        # duplicate(self.button, origin=(0, -11.5), text=f"Button{i}", y=-c, z=-1)
        self.button = Button(parent=self, text=self.button_text, radius=radius, scale=scale_btn, y=0.4, origin=(0, 0),
                             z=-1,
                             highlight_color=clr.azure,
                             command=None)
        self.button2 = Button(parent=self, text=self.button2_text, radius=radius, scale=scale_btn, y=0.26, z=-1,
                              highlight_color=clr.azure,
                              command=None)
        self.button3 = Button(parent=self, text=self.button3_text, radius=radius, scale=scale_btn, y=0.12, z=-1,
                              highlight_color=clr.azure,
                              command=None)
        self.button4 = Button(parent=self, text=self.button4_text, radius=radius, scale=scale_btn, y=-0.02, z=-1,
                              highlight_color=clr.azure,
                              command=None)
        self.button5 = Button(parent=self, text=self.button5_text, radius=radius, scale=scale_btn, y=-0.16, z=-1,
                              highlight_color=clr.azure,
                              command=None)
        self.button6 = Button(parent=self, text=self.button6_text, radius=radius, scale=scale_btn, y=-0.3, z=-1,
                              highlight_color=clr.azure,
                              command=None)

    def update(self):
        if self.button6.text == "Exit" or self.button6.text == "exit":
            self.button6.color = color.rgb(75, 0, 0)
            self.button6.highlight_color = color.rgb(50, 0, 0)
            self.button6.on_click = application.quit
            print("True")
        else:
            print("False")

    def input(self, key):
        if self.key_control is True:
            if held_keys['control'] and held_keys[self.key_bind]:
                if self.visible is False:
                    self.visible = True
                    self.position = mouse.x, mouse.y
                else:
                    self.visible = False
                    self.position = 999, 999
        else:
            if held_keys[self.key_bind]:
                if self.visible is False:
                    self.visible = True
                    self.position = mouse.x, mouse.y
                else:
                    self.visible = False
                    self.position = 999, 999

        # print_warning(f"Key not found: {self.key_bind}")


if __name__ == "__main__":
    app = Ursina()

    ClickPanel(key_control=False, key_bind="right mouse")

    app.run()
