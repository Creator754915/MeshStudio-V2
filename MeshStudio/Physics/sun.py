from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import Vec4, DirectionalLight, AmbientLight


class Sun:
    def __init__(self, target):
        super().__init__()

        self.sun = DirectionalLight('sun')

        self.sun.getLens().setNearFar(-120, 300)
        self.sun.getLens().setFilmSize((150, 150))

        self.pivot = render.attachNewNode(self.sun)
        self.pivot.lookAt((1, -1, -1))
        render.setLight(self.pivot)

        self.lighting = AmbientLight('lighting')
        self.lighting.setColor(Vec4(0.4, 0.5, 0.6, 0) * 1.3)
        self.parent = render.attachNewNode(self.lighting)
        render.setLight(self.parent)

        self.target = target

        taskMgr.add(self.update, 'update')

    def update(self, task):
        self.sun.setShadowCaster(True, 4096, 4096)
        self.pivot.setPos(self.target.world_position)

        return task.cont