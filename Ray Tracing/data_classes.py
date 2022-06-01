from dataclasses import dataclass
from typing import Any

import numpy as np
from color import Color
from vector import Vector

NDArray = Any


@dataclass
class Camera:
    position: NDArray
    look_at: Vector
    up_vector: Vector
    sc_dist: float
    sc_width: float

    @classmethod
    def from_line(cls, px, py, pz, lx, ly, lz, ux, uy, uz, sc_dist, sc_width):
        return cls(
            position=np.array([px, py, pz]),
            look_at=Vector(np.array([lx, ly, lz])),
            up_vector=Vector(np.array([ux, uy, uz])),
            sc_dist=sc_dist,
            sc_width=sc_width
        )


@dataclass
class Settings:
    background: Color
    shadow_rays: float
    recursion_max: float

    @classmethod
    def from_line(cls, bgr, bgg, bgb, sh_rays, rec_max):
        return cls(
            background=Color(np.array([bgr, bgg, bgb])),
            shadow_rays=sh_rays,
            recursion_max=rec_max
        )


@dataclass
class Material:
    diffuse: Color
    specular: Color
    reflection: Color
    phong: float
    transparency: float

    @classmethod
    def from_line(cls, dr, dg, db, sr, sg, sb, rr, rg, rb, phong, trans):
        return cls(
            diffuse=Color(np.array([dr, dg, db])),
            specular=Color(np.array([sr, sg, sb])),
            reflection=Color(np.array([rr, rg, rb])),
            phong=phong,
            transparency=trans
        )


@dataclass
class Sphere:
    center: NDArray
    radius: float
    index: float

    @classmethod
    def from_line(cls, cx, cy, cz, radius, mat_idx):
        return cls(
            center=np.array([cx, cy, cz]),
            radius=radius,
            index=mat_idx
        )


@dataclass
class Plane:
    normal: NDArray
    offset: float
    index: float

    @classmethod
    def from_line(cls, nx, ny, nz, offset, mat_idx):
        return cls(
            normal=np.array([nx, ny, nz]),
            offset=offset,
            index=mat_idx
        )


@dataclass
class Box:
    center: NDArray
    scale: float
    index: float

    @classmethod
    def from_line(cls, cx, cy, cz, scale, mat_idx):
        return cls(
            center=np.array([cx, cy, cz]),
            scale=scale,
            index=mat_idx
        )


@dataclass
class Light:
    position: NDArray
    color: Color
    specular: float
    shadow: float
    width: float

    @classmethod
    def from_line(cls, px, py, pz, r, g, b, spec, shadow, width):
        return cls(
            position=np.array([px, py, pz]),
            color=Color(np.array([r, g, b])),
            specular=spec,
            shadow=shadow,
            width=width
        )
