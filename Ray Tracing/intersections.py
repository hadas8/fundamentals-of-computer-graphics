from data_classes import Sphere, Plane, Box
import typing
from typing import Any
import numpy as np
from vector import Vector, Ray

NDArray = Any


def sphere_intersect(sphere, ray: Ray):
    # returns an Intersection object of a certain sphere and ray
    center = sphere.center
    radius = sphere.radius
    b = 2 * np.dot(ray.direction.v, ray.origin - center)
    c = np.linalg.norm(ray.origin - center) ** 2 - radius ** 2
    delta = b ** 2 - 4 * c
    if delta > 0:
        t1 = (-b + np.sqrt(delta)) / 2
        t2 = (-b - np.sqrt(delta)) / 2
        if t1 > 0 and t2 > 0:
            t = min(t1, t2)
            intersection_point = ray.origin + ray.direction.v * t
            normal = Vector(intersection_point - center).normalize().v
            return Intersection(sphere, intersection_point, normal, t)
    return None


def plane_intersect(plane, ray: Ray):
    # returns an Intersection object of a certain plane and ray
    normal = plane.normal
    offset = plane.offset
    # normal * (o + t * d) = offset
    denom = normal.dot(ray.direction.v)
    t = (offset - normal.dot(ray.origin)) / denom
    # if t is positive there's  an intersection
    if t > 0:
        intersection_point = ray.origin + ray.direction.v * t
        return Intersection(plane, intersection_point, normal, t)
    return None


def box_intersect(box, ray: Ray):
    # returns an Intersection object of a certain box and ray
    # returns intersection_point, distance
    center = box.center
    scale = box.scale
    o, d = ray.origin, ray.direction.v  # normalized direction
    x_min, x_max = center[0] - scale / 2, center[0] + scale / 2
    y_min, y_max = center[1] - scale / 2, center[1] + scale / 2
    z_min, z_max = center[2] - scale / 2, center[2] + scale / 2
    t_min, t_max = (x_min - o[0]) / d[0], (x_max - o[0]) / d[0]
    t_y_min, t_y_max = (y_min - o[1]) / d[1], (y_max - o[1]) / d[1]
    t_z_min, t_z_max = (z_min - o[2]) / d[2], (z_max - o[2]) / d[2]

    if t_max < t_min:
        t_min, t_max = swap(t_min, t_max)

    if t_y_max < t_y_min:
        t_y_min, t_y_max = swap(t_y_min, t_y_max)

    if t_z_max < t_z_min:
        t_z_min, t_z_max = swap(t_z_min, t_z_max)

    if (t_min > t_y_max) or (t_y_min > t_max):
        return None

    if t_y_min > t_min:
        t_min = t_y_min

    if t_y_max < t_max:
        t_max = t_y_max

    if (t_min > t_z_max) or (t_z_min > t_max):
        return None

    intersection_point = ray.origin + ray.direction.v * t_min
    normal = normal_box_intersect(intersection_point, center, scale)

    return Intersection(box, intersection_point, normal, t_min)


def intersected_objects(sphere_objects: typing.List[Sphere], plane_objects: typing.List[Plane],
                        box_objects: typing.List[Box], ray: Ray):
    # A method to calculate for each ray, the list of all surfaces it interacts with ordered in descending order by distance
    # this method is assuming no 2 distances are the same
    objects_inters = []
    if len(sphere_objects) != 0:
        for sphere_obj in sphere_objects:
            sphere_inter = sphere_intersect(sphere_obj, ray)
            if sphere_inter is not None:
                objects_inters.append(sphere_inter)

    if len(plane_objects) != 0:
        for plane_obj in plane_objects:
            plane_inter = plane_intersect(plane_obj, ray)
            if plane_inter is not None:
                objects_inters.append(plane_inter)

    if len(box_objects) != 0:
        for box_obj in box_objects:
            box_inter = box_intersect(box_obj, ray)
            if box_inter is not None:
                objects_inters.append(box_inter)

    objects_inters.sort(key=lambda x: x.distance)
    return objects_inters


def nearest_intersection(spheres: typing.List[Sphere], planes: typing.List[Plane], boxes: typing.List[Box],
                         ray: Ray):
    # Helper method to find the nearest object in the intersections list
    nearest_object = intersected_objects(spheres, planes, boxes, ray)[0][0]
    return nearest_object


def swap(min_val, max_val):
    # helper method to swap min, max values
    temp = min_val
    min_val = max_val
    max_val = temp
    return min_val, max_val


def normal_box_intersect(inter_point, center, scale):
    # A method to calculate the normal of an intersection with a box, according to which face of the box the intersection is on
    EPS = 0.000001
    normal = np.empty(3, )
    near_point = np.array([center[0] - scale / 2, center[1] - scale / 2, center[2] - scale / 2])
    far_point = np.array([center[0] + scale / 2, center[1] + scale / 2, center[2] + scale / 2])
    if abs(inter_point[0] - near_point[0]) <= EPS:
        normal = np.array([-1, 0, 0], dtype=float)
    elif abs(inter_point[0] - far_point[0]) <= EPS:
        normal = np.array([1, 0, 0], dtype=float)
    elif abs(inter_point[1] - near_point[1]) <= EPS:
        normal = np.array([0, -1, 0], dtype=float)
    elif abs(inter_point[1] - far_point[1]) <= EPS:
        normal = np.array([0, 1, 0], dtype=float)
    elif abs(inter_point[2] - near_point[2]) <= EPS:
        normal = np.array([0, 0, -1], dtype=float)
    elif abs(inter_point[2] - far_point[2]) <= EPS:
        normal = np.array([0, 0, 1], dtype=float)

    return normal


class Intersection:
    # A class to create type intersection to contain all its data,
    # which surface type it is, the intersection point, the normal at the intersection point and the distance from the camera
    def __init__(self, surface, point, normal, distance):
        self.surface = surface
        self.point = point
        self.normal = normal
        self.distance = distance
