from ursina import *


class ListBox(Button):
    def __init__(self, text="Select    >", ObjectList=[], scale=(.15, 0.05), **kwargs):
        super().__init__(text=text, scale=scale, **kwargs)
        self.parent = camera.ui
        self.L
        for i in range(len(ObjectList)):
            print(self.ObjectList[i])

    def SetUpList(self):
        for i in range(len(self.ObjectList)):
            Button(parent=self, text=f"{self.ObjectList[i - 1]}", y=self.postion - self.scale_x)


if __name__ == "__main__":
    app = Ursina()

    listbox = ListBox(List=["Test", "Test2", "Test2"])

    listbox.SetUpList()

    app.run()
