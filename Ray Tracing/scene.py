import typing
from typing import Any
from data_classes import Camera, Material, Settings
from vector import Vector

import numpy as np
NDArray = Any


class Scene:
    # the object of a scene, depicting all the calculations of the camera and the screen
    def __init__(self, cam: Camera, materials: typing.List[Material], settings: Settings, width: int, height: int):
        self.camera = cam
        self.materials = materials
        self.settings = settings
        self.width = width
        self.height = height
        self.aspect_ratio = self.width / self.height
        self.sc_width = self.camera.sc_width
        self.sc_height = self.sc_width / self.aspect_ratio

        # towards is the vector of the camera's look-at direction towards the scene
        self.towards = Vector(self.camera.look_at.v - self.camera.position).normalize()

        # screen center is a point at the center of the screen, by the vector towards
        self.screen_center = self.camera.position + (self.camera.sc_dist * self.towards.v)

        # The Vx vector of the screen, points to the right of the camera
        self.vx = Vector(np.cross(self.vy.v, -self.towards.v))

        # p0 is a point in the lower left corner of the screen, we begin rendering rays from this point
        self.p0 = self.screen_center - (self.sc_width / 2 * self.vx.v) - (self.sc_height / 2 * self.vy.v)

    @property
    def vy(self) -> Vector:
        # up direction is the vector that points up from the camera in the direction of the up vector.
        # It is also perpendicular to the vector towards, and is used to align the screen with the camera
        up_vector = self.camera.up_vector
        towards = self.towards
        proj = up_vector.projection(towards)
        if proj.any():
            return Vector(-1 * (up_vector.v - proj)).normalize()
        else:
            return up_vector.normalize()
