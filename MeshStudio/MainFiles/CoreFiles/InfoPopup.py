from ursina import *


class InfoPopup(WindowPanel):
    def __init__(self, title="Information", Message="Enter Your Message", Type="ERROR"):
        super().__init__(title=title, Message=Message, Type=Type)
        self.y = self.panel.scale_y / 2 * self.scale_y
        self.popup = True
        self.InfoText = Text('Are you sure to unsave your project ?')
        self.YesButton = Button(text='Yes', color=color.azure)
        self.NoButton = Button(text='No', color=color.red, on_click=lambda: destroy(self))
        self.content = (
            self.InfoText,
            self.YesButton,
            self.NoButton
        )

        if Type == "ERROR":
            self.YesButton.color = color.green
            self.NoButton.color = color.red
        elif Type == "INFO":
            self.YesButton.color = color.azure
            self.NoButton.color = color.red
            self.NoButton.text = "Close"


if __name__ == "__main__":
    app = Ursina()

    InfoPopup()

    app.run()
