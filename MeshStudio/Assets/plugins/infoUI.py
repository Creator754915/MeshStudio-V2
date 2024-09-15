from ursina import *


def aspect_ratio():
    print_info(window.size)


if __name__ == "__main__":
    app = Ursina()

    aspect_ratio()

    app.run()