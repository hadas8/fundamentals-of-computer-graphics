import random
from intersections import intersected_objects
from scene import Scene
from vector import Vector, Ray
import numpy as np
from data_classes import Light


def get_plane_data(light: Light, inter_point):
    # A helper method to create the light plane needed for the soft shadows
    light_direction = Vector(inter_point - light.position).normalize().v
    vec_on_pln = np.random.rand(3)
    vec_on_pln = vec_on_pln - vec_on_pln.dot(light_direction) * light_direction
    vec_on_pln = Vector(vec_on_pln).normalize().v
    cross_prod = np.cross(vec_on_pln, light_direction)
    return vec_on_pln, cross_prod


def calc_shadows_ratio(light: Light, scene: Scene, inter_point, vec_on_pln, cross_prod, sph, pln, bx, masked_inter):
    # Calculate the ratio of light rays that hit/don't hit the surface at the intersection point with the camera ray
    N = int(scene.settings.shadow_rays)
    start_point = calc_light_start_point(light, cross_prod, vec_on_pln)
    hit_cnt = 0
    u_vec = cross_prod * light.width / N
    v_vec = vec_on_pln * light.width / N
    for i in range(N):
        # start from the corner of the plan's grid
        start_copy = start_point.copy()
        for j in range(N):
            origin_light = start_copy + v_vec * random.uniform(0, 1) + u_vec * random.uniform(0, 1)
            light_to_inter_dir = Vector(inter_point - origin_light)
            ray = Ray(origin_light, light_to_inter_dir)
            light_inters = intersected_objects(sph, pln, bx, ray)
            if len(light_inters) > 1:
                # check if there is another surface between the current surface and the light
                if light_inters[0].surface is not masked_inter.surface:
                    if any(masked_inter.surface is inter.surface for inter in light_inters):
                        hit_cnt += 1
            start_copy += v_vec
        start_point += u_vec
    hit_ratio = hit_cnt / (N ** 2)
    return hit_ratio


def calc_light_intensity(light: Light, hit_ratio):
    # A helper method calculate the light intensity
    ret = (1 - light.shadow) + light.shadow * hit_ratio
    return 1 - ret


def calc_light_start_point(light: Light, u_vec, v_vec):
    # A helper method to calculate the corner fo the grid
    corner = (light.position - 0.5 * u_vec * light.width - 0.5 * v_vec * light.width)
    return corner


def soft_shadows(light: Light, inter_point, scene: Scene, sph, pln, bx, inter):
    # A wrapper method to all methods in the class to help call them via only 1 call and return the light intensity parameter
    vec_on_pln, cross_prod = get_plane_data(light, inter_point)
    hit_ratio = calc_shadows_ratio(light, scene, inter_point, vec_on_pln, cross_prod, sph, pln, bx, inter)
    light_intensity = calc_light_intensity(light, hit_ratio)
    return light_intensity
