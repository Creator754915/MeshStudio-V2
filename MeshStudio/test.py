from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
from ursina.shaders import basic_lighting_shader

app = Ursina()
app.title = "Mon Premier FPS"
window.borderless = False
window.fullscreen = False
window.exit_button.enabled = False
window.fps_counter.enabled = False

boxes = []


def pause():
    def resume():
        application.resume()
        player.enabled = True
        resume_btn.enabled = False
        quit_btn.enabled = False

    def quit_game():
        application.quit()

    resume_btn = Button(text='Resume', color=color.gray, highlight_color=color.light_gray, scale=(.2, .075),
                        radius=0.08,
                        position=(0, 0))

    quit_btn = Button(text='Quit', color=color.gray, highlight_color=color.light_gray, scale=(.2, .075),
                      radius=0.08,
                      position=(0, -.12))

    resume_btn.enabled = True
    quit_btn.enabled = True

    resume_btn.on_click = resume
    quit_btn.on_click = quit_game


sky = Sky()

ground = Entity(model="plane", texture="grass", scale=(50, 1, 50), position=(0, 0), collider="mesh")
boxes.append(ground)

wall = Entity(model="cube", texture="brick", scale=(50, 10, 1), position=(25, 0, 0), rotation=(0, 90, 0),
              collider="cube")

wall2 = Entity(model="cube", texture="brick", scale=(50, 10, 1), position=(-25, 0, 0), rotation=(0, 90, 0),
               collider="cube")

wall3 = Entity(model="cube", texture="brick", scale=(50, 10, 1), position=(0, 0, -25), rotation=(0, 0, 0),
               collider="cube")

wall4 = Entity(model="cube", texture="brick", scale=(50, 10, 1), position=(0, 0, 25), rotation=(0, 0, 0),
               collider="cube")

player = FirstPersonController(speed=8, gravity=0.5)

healthbar = HealthBar(bar_color=color.red.tint(-.25),
                      roundness=0.2,
                      scale=(.6, .04),
                      position=(-.82, -.43))

hookshot_target = Button(parent=scene, model='cube', color=color.brown, position=(4, 5, 5))
hookshot_target.on_click = Func(player.animate_position, hookshot_target.position, duration=.5, curve=curve.linear)


def input(key):
    if key == 'escape':
        if not application.paused:
            player.enabled = False
            application.pause()
            pause()
        else:
            application.resume()
            player.enabled = True


def update():
    if held_keys["shift"]:
        camera.fov = lerp(camera.fov, 30, .5)
    else:
        camera.fov = lerp(camera.fov, 90, .5)


app.run()
