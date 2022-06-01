from typing import Any

from vector import Vector

import numpy as np
NDArray = Any


class Color:
    # an RGB color represented by a 3D numpy array
    def __init__(self, c: NDArray):
        self.c = c

    @classmethod
    def diffuse(cls, mtl_diffuse: "Color", lgt_color: "Color", normal: Vector, lgt_dir: Vector, intensity: float):
        # a method that calculates the diffuse color of a given material with a given light source
        return cls(
             c=intensity * mtl_diffuse.c * lgt_color.c * max(0.0, np.dot(normal.v, lgt_dir.v))
         )

    @classmethod
    def specular(cls, mtl_specular: "Color", lgt_color: "Color", lgt_specular: float,
                 reflection_dir: Vector, ray_dir: Vector, phong: float, intensity: float):
        # a method that calculates the specular color of a given material with a given light source
        return cls(
            c=intensity * mtl_specular.c * lgt_color.c * lgt_specular * (max(0.0, np.dot(reflection_dir.v, -ray_dir.v)) ** phong)
        )

    @classmethod
    def output_color(cls, background: "Color", transparency: float, color_by_light: "Color",
                     ref: "Color", mtl_ref: "Color"):
        # a method that calculates the output color of a given material with a given light source
        return cls(
            c=(background.c * transparency) + color_by_light.c * (1 - transparency) + (ref.c * mtl_ref.c)
        )
