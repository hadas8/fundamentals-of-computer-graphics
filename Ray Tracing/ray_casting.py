import typing
from typing import Any
from scene import Scene
from vector import Vector, Ray
from color import Color
from data_classes import Light, Material, Sphere, Plane, Box
from intersections import Intersection, intersected_objects
from shadows import soft_shadows

import numpy as np

NDArray = Any


def render(scene: Scene, lgt: typing.List[Light],
           sph: typing.List[Sphere], pln: typing.List[Plane], box: typing.List[Box]):
    # The method of the main loop. Rendering a scene with the ray tracing algorithm
    width = scene.width
    height = scene.height
    origin = scene.camera.position

    cnt = 0
    image = np.zeros((height, width, 3))
    for i, y in enumerate(np.linspace(0, scene.sc_height, height)):
        for j, x in enumerate(np.linspace(0, scene.sc_width, width)):
            cnt = cnt + 1

            # p is the current pixel in the screen
            p = scene.p0 + (scene.vx.v * x) + (scene.vy.v * y)

            # ray is the vector cast from the camera through p in the look-at direction
            ray = Ray(origin, Vector(p - origin))

            # inters is a list of surfaces that intersect with ray sorted by the distance from the camera
            inters = intersected_objects(sph, pln, box, ray)

            image[i][j] = colors_rec(lgt, inters, ray, scene, sph, pln, box, int(scene.settings.recursion_max)).c

    return image


def get_color(light: Light, inter: Intersection, ray: Ray, material: Material, light_intensity: float):
    # Add the diffuse and the specular color to the surface according to a specific light source
    light_dir = Vector(light.position - inter.point).normalize()
    light_reflection_dir = Vector(
        light_dir.v + 2 * (light_dir.projection(Vector(inter.normal)) - light_dir.v)).normalize()
    diffuse_color = Color.diffuse(material.diffuse, light.color, Vector(inter.normal), light_dir, light_intensity)
    specular_color = Color.specular(material.specular, light.color, light.specular,
                                    light_reflection_dir, ray.direction, material.phong, light_intensity)
    return Color(diffuse_color.c + specular_color.c)


def colors_rec(lgt: typing.List[Light], inters: typing.List[Intersection], view_ray: Ray, scene: Scene,
               sph: typing.List[Sphere], pln: typing.List[Plane], box: typing.List[Box], rec_depth: int):
    # for each pixel, calculate the output color of the screen, according to surfaces intersected by the ray,
    # taking into account all light sources, and materials
    background = scene.settings.background
    if len(inters) == 0:
        return background
    mat = scene.materials
    inter = inters[0]
    index = inter.surface.index - 1
    material = mat[int(index)]
    transparency = material.transparency

    # Calculating the color and shadows of the first object intersected by the ray
    color_by_light = color_by_light_calc(inter, material, lgt, scene, view_ray, sph, pln, box)

    # Calculate background color for transparent and semi-transparent surfaces
    if transparency > 0 and len(inters) > 1:
        background = colors_rec(lgt, inters[1:], view_ray, scene, sph, pln, box, rec_depth)

    # Calculate reflections of the surface
    reflection_color = Color([0, 0, 0])
    if rec_depth > 0:
        view_reflection_dir = Vector(-view_ray.direction.v)
        view_reflection_vector = Vector(
            view_reflection_dir.v + 2 * (
                        view_reflection_dir.projection(Vector(inter.normal)) - view_reflection_dir.v)).normalize()
        reflection_ray = Ray.cast_ray(inter.point, view_reflection_vector)
        ref_inters = intersected_objects(sph, pln, box, reflection_ray)
        reflection_color = colors_rec(lgt, ref_inters, reflection_ray, scene, sph, pln, box, rec_depth - 1)

    return Color.output_color(background, transparency, color_by_light, reflection_color, material.reflection)


def color_by_light_calc(inter: Intersection, material: Material, lgt: typing.List[Light], scene: Scene, pixel_ray: Ray,
                        sph: typing.List[Sphere], pln: typing.List[Plane], box: typing.List[Box]):
    # for each light source, calculating shadows and color of a surface
    color_by_light = Color([0, 0, 0])
    for light in lgt:
        light_intensity = soft_shadows(light, inter.point, scene, sph, pln, box, inter)
        color_by_light.c += get_color(light, inter, pixel_ray, material, light_intensity).c
    return color_by_light
