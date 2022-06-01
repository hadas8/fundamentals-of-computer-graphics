from typing import Any

import numpy as np
NDArray = Any


class Vector:
    # a vector represented by 3D numpy array v,
    # to simulate a directed ray that begins at (0,0,0) in the direction of v
    def __init__(self, v: NDArray):
        self.v = v

    def magnitude(self):
        return np.linalg.norm(self.v)

    def normalize(self):
        return Vector(self.v / self.magnitude())

    def projection(self, v2: "Vector"):
        return (np.dot(self.v, v2.v) / np.dot(v2.v, v2.v)) * v2.v


class Ray:
    # a ray object is a direction vector that begins at an origin point
    def __init__(self, origin: NDArray, direction: Vector):
        self.origin = origin
        self.direction = direction.normalize()

    @classmethod
    def cast_ray(cls, point: NDArray, direction: Vector):
        epsilon = 0.00000000001
        return cls(
            origin=point + direction.v * epsilon,
            direction=direction
        )
