import argparse
import typing
from time import perf_counter

import ray_casting
from image import get_image, normalize_image
from scene import Scene
from data_classes import Camera, Settings, Material, Sphere, Plane, Box, Light


def get_args():
    parser = argparse.ArgumentParser(description='Ray tracing application')
    parser.add_argument(dest="scene", type=str, help='The scene file path')
    parser.add_argument(dest="output_dir", type=str, help='The output image')
    parser.add_argument(dest="width", type=int, help="The output image width", default=500)
    parser.add_argument(dest="height", type=int, help="The output image height", default=500)
    args = parser.parse_args()
    return args


def main(args):
    """
    The program main function.
    :param args: the command-line input arguments.
    """
    cam: typing.List[Camera] = []
    sett: typing.List[Settings] = []
    mtl: typing.List[Material] = []
    sph: typing.List[Sphere] = []
    pln: typing.List[Plane] = []
    box: typing.List[Box] = []
    lgt: typing.List[Light] = []

    with open(args.scene, 'r') as f:
        for line in f:
            if line.startswith("#") or (line == "\n"):
                continue
            elif line.startswith("cam"):
                cam.append(Camera.from_line(*map(float, line.split()[1:])))
            elif line.startswith("set"):
                sett.append(Settings.from_line(*map(float, line.split()[1:])))
            elif line.startswith("mtl"):
                mtl.append(Material.from_line(*map(float, line.split()[1:])))
            elif line.startswith("sph"):
                sph.append(Sphere.from_line(*map(float, line.split()[1:])))
            elif line.startswith("pln"):
                pln.append(Plane.from_line(*map(float, line.split()[1:])))
            elif line.startswith("box"):
                box.append(Box.from_line(*map(float, line.split()[1:])))
            elif line.startswith("lgt"):
                lgt.append(Light.from_line(*map(float, line.split()[1:])))

    scene = Scene(cam[0], mtl, sett[0], int(args.width), int(args.height))
    image = ray_casting.render(scene, lgt, sph, pln, box)

    # Normalize image pixels to be between [0., 1.0]
    image = normalize_image(image)

    image.save(args.output_dir)


if __name__ == '__main__':
    args = get_args()
    main(args)
