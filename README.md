# Fundamentals of Computer Graphics

2 Assignments that we submited for The Fundamentals of Computer Graphics, Vision and Image Processing class in Tel Aviv University

## Seam Carving

An implementation of the seam carving algorithm for image resizing. 
This project contains 3 pre-implemented python files:
- A main program that receives an image, size and a resizing method, and excecutes the chosen method to resize the image.
- A utils file with several pre-implemnted methods of opening, saving and normalizing an image, using the PIL packge in Python
- A nearest_neigbor file with a pre-implemented naive method for image resizing using the nearest meighbor approach.

The file seam_carving contains out implementaion of the seam carving algorithm, and depicts two methods: a basic seam carving algorithm and a forward looking seam carving algorithm. In both methods, we calculate the optimal vertical seams which their removal will least affect the energy of the picture. These seams are either removed or duplicated to change the size of the piture. Following this, we turn the picutre sideways and repeat the process with the horizontal seams.
The forward looking seam carving method improves the energy function used to determine the optimal seam, this improvement is being done by calculating the energy of the image, not as it is but is it would be after removing the optimal seam, to detemine the next seam to remove. This improves the cases of seams chosen around the edges of the previuosly removed seams. 

* Also presented are the PDF file of the instructions for this assignment, as well as some image examples.


## Ray Tracing

An implementation of the Ray tracing algorithm for image rendering.
This projects contains 9 Python files of our implementation of the ray tracing algorithm:
- RayTracer is the main program. It accepts a text file that depicts a scene to render, as well as the desired height and width and returns the rendered image of the scene.
- data_classes file contains the data classes parsed from the scene file. This includes Camera, Settings, Materials, Planes, Spheres, Boxes and Lights.
- scene file contains the Scene class. it includes the Vectors the construct the camera as well as the screen through which the scene is depicted in the picture.
- vector file contains two classes, a Vector class and a Ray class. A vector is a 3D numpy array with several implemented calculation methods. A ray is an object that contains an origin point (a 3D numpy array) and a normilized direction vector.
- color file contains the RGB Color class (a 3D numpy array), with several implemnted methods of different color aspects calculations, such as diffuse color and specular color.
- shadows file contains several methods of calculating shadows and soft shadows in the picture, according to the light directions, as well as the surfaces' locations.
- intersections file contains the class Intersection that depicts an occurance of intersection of a ray with a surface in the scene. The class object contains the surface, the intersection point, a vector normal to the surface from the intersection point, and the distance between the point of intersection to the origin point of the ray. The file also contains several methods to calculate diffrent surfaces in the scene, and their intersection occurenece with a given ray, and a method for listing all the intersections of a specific ray, sorted by their distance.
- ray_casting file contains several methods, including the core rendering algorithm and the picture coloring methods:
  - render method: The core loop of a the ray tracing algorithm. For each pixel in the screen, the method casts a ray from the camera, through the pixel, calculates all the surfaces intersected by the ray, and colors the pixel in accordance.
  - colors_rec is the main coloring method, it receives a ray and a list of intersection objects, and recursively follows through the surfaces to calculate the color of the pixel, considering the color of the surface, the colors and directions of the lights, the shadows, the transparancy and reflexivity of the materials.
  - other coloring methods get_color and color_by_light are helper functions that help break some of  these calculations.
- image file saves the given numpy array image into a PIL image, and normalizes the colors

Also presented are the PDF file of the instructions for this assignment, as well as some scene text and .png image examples.
