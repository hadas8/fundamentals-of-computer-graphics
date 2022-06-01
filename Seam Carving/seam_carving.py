from typing import Dict, Any

import numpy as np
import utils

NDArray = Any


def index_matrix(height, width):
    # defining a helper 2D index matrix in the dimensions of the image
    dim = height * width
    i_matrix = np.arange(dim, dtype=int)
    i_matrix.shape = (height, width)

    return i_matrix


def find_index(place: int, width: int):
    # translating value in the index matrix to actual image index
    dim1 = place // width
    dim2 = place % width

    return int(dim1), int(dim2)


def calc_new_edge(gray_image, direction, i, j):
    # helper method that calculates the edges that will be created after removing a seam,
    # according to the direction choice
    # take cares of special case when j == 0 and j-1 is out ouf bound
    edge = 0
    if j == 0 or j == gray_image.shape[1] - 1:
        special_case_value = 255.0
    else:
        special_case_value = abs((gray_image[i][j + 1] - gray_image[i][j - 1]))

    if direction == 'L':  # will not be called in cases where j == 0
        edge = special_case_value + abs((gray_image[i - 1][j] - gray_image[i][j - 1]))
    elif direction == 'U':
        edge = special_case_value
    elif direction == 'R':  # will not be called in cases where j == cols-1
        edge = special_case_value + abs((gray_image[i - 1][j] - gray_image[i][j + 1]))
    return edge


def calc_forward_cost_matrix(grad_mat, grey_image, rows, cols):
    # returning the cost matrix for the forward-looking method
    cost_mat = np.zeros([rows, cols])
    for i in range(rows):
        for j in range(cols):
            if i == 0:
                cost_mat[i][j] = grad_mat[i][j]
            else:
                if j == 0:
                    cost_mat[i][j] = grad_mat[i][j] + min(cost_mat[i - 1][j] + calc_new_edge(grey_image, 'U', i, j),
                                                          cost_mat[i - 1][j + 1] + calc_new_edge(grey_image, 'R', i, j))

                elif j == cols - 1:
                    cost_mat[i][j] = grad_mat[i][j] + min(cost_mat[i - 1][j - 1] + calc_new_edge(grey_image, 'L', i, j),
                                                          cost_mat[i - 1][j] + calc_new_edge(grey_image, 'U', i, j))

                else:
                    cost_mat[i][j] = grad_mat[i][j] + min(cost_mat[i - 1][j - 1] + calc_new_edge(grey_image, 'L', i, j),
                                                          cost_mat[i - 1][j] + calc_new_edge(grey_image, 'U', i, j),
                                                          cost_mat[i - 1][j + 1] + calc_new_edge(grey_image, 'R', i, j))

    return cost_mat


def find_forward_seam(cost_mat, grad_mat, grey_image, indices, rows):
    seam = np.zeros([rows])
    i = rows - 1
    j = np.argmin(cost_mat[i])
    seam[0] = indices[i][j]

    for t in range(rows - 1):
        if round(cost_mat[i][j], 10) == \
                round(grad_mat[i][j] + cost_mat[i-1][j] + calc_new_edge(grey_image, 'U', i, j), 10):
            min_col_index = j
        elif round(cost_mat[i][j], 10) == \
                round(grad_mat[i][j] + cost_mat[i-1][j-1] + calc_new_edge(grey_image, 'L', i, j), 10):
            min_col_index = j - 1
        else:
            min_col_index = j + 1

        i = i - 1
        j = min_col_index

        seam[t + 1] = indices[i][min_col_index]

    return seam


def calc_basic_cost_matrix(grad_mat, rows, cols):
    # returning the cost matrix for teh basic method
    cost_mat = np.zeros([rows, cols])
    for i in range(rows):
        for j in range(cols):
            if i == 0:
                cost_mat[i][j] = grad_mat[i][j]
            else:
                if j == 0:
                    cost_mat[i][j] = grad_mat[i][j] + min(cost_mat[i - 1][j], cost_mat[i - 1][j + 1])
                elif j == cols - 1:
                    cost_mat[i][j] = grad_mat[i][j] + min(cost_mat[i - 1][j - 1], cost_mat[i - 1][j])
                else:
                    cost_mat[i][j] = grad_mat[i][j] + min(cost_mat[i - 1][j - 1], cost_mat[i - 1][j],
                                                          cost_mat[i - 1][j + 1])
    return cost_mat


def find_basic_seam(cost_mat, indices, rows, cols):
    seam = np.zeros([rows])
    curr_row_index = rows - 1
    curr_col_index = np.argmin(cost_mat[curr_row_index])

    seam[0] = indices[curr_row_index][curr_col_index]

    for i in range(rows - 1):
        curr_row_index = rows - 2 - i
        if curr_col_index == 0:
            curr_col_index = np.argmin(cost_mat[curr_row_index][0:2])
        elif curr_col_index == cols - 1:
            curr_col_index = np.argmin(cost_mat[curr_row_index][curr_col_index - 2:]) + curr_col_index - 2
        else:
            curr_col_index = np.argmin(cost_mat[curr_row_index][curr_col_index - 1:curr_col_index + 2]) + curr_col_index - 1

        seam[1 + i] = indices[curr_row_index][curr_col_index]

    return seam


def add_seam_to_seams(seams, seam, index):
    seams[index] = seam


def remove_seam(image_to_change: NDArray, indices: NDArray, grad_mat: NDArray, seam: NDArray):
    # receives a seam array, and deletes the seam from the image and from the index matrix
    length = seam.shape[0]
    for i in range(length):
        j = np.searchsorted(indices[i], seam[length - 1 - i])
        indices[i, j:-1] = indices[i, j + 1:]
        image_to_change[i, j:-1, ...] = image_to_change[i, j + 1:, ...]
        grad_mat[i, j:-1] = grad_mat[i, j + 1:]


def add_seam(image_to_change: NDArray, indices: NDArray, seam: NDArray):
    # receives a seam array, and duplicates the seam in the image and the index matrix
    length = seam.shape[0]
    for i in range(length):
        j = np.searchsorted(indices[i], seam[length - 1 - i])
        indices[i, j + 1:] = indices[i, j:-1]
        image_to_change[i, j + 1:, ...] = image_to_change[i, j:-1, ...]


def remove_seams(image_to_change: NDArray, indices: NDArray, seam_matrix: NDArray):
    # receives a seam matrix, and deletes all the seams from the rgb image
    empty = np.zeros_like(indices)
    for seam in seam_matrix:
        remove_seam(image_to_change, indices, empty, seam)
    return image_to_change[:, :-seam_matrix.shape[0]]


def add_seams(image_to_change: NDArray, indices: NDArray, seam_matrix: NDArray):
    # receives a seam matrix, and duplicate all the seams in the rgb image
    zero_image = np.zeros((image_to_change.shape[0], seam_matrix.shape[0], 3), dtype=np.float32)
    zero_indices = np.zeros((indices.shape[0], seam_matrix.shape[0]), dtype=int)
    larger_image = np.concatenate((image_to_change, zero_image), axis=1)
    larger_indices = np.concatenate((indices, zero_indices), axis=1)

    for seam in seam_matrix:
        add_seam(larger_image, larger_indices, seam)
    return larger_image


def color_seams(image_to_change: NDArray, seam_matrix: NDArray, rot: int, width: int):
    # receives a seam matrix, color all the pixels in the seams to either red or black
    color = (255, 0, 0) if rot == 0 else (0, 0, 0)
    for seam in seam_matrix:
        for place in seam:
            image_to_change[find_index(place, width)] = color


def return_images(image_to_change: NDArray, seams: NDArray, indices: NDArray, rot: int, enlarge: bool):
    # resizing the image according to the found seams, returning a resized image and an image with colored seams
    resized_image = np.copy(image_to_change)
    colors = np.copy(image_to_change)

    color_seams(colors, seams, rot, indices.shape[1])
    if enlarge:
        resized_image = add_seams(resized_image, indices, seams)
    else:
        resized_image = remove_seams(resized_image, indices, seams)

    return colors, resized_image


def resize(image: NDArray, out_height: int, out_width: int, forward_implementation: bool) -> Dict[str, NDArray]:
    """

    :param image: ِnp.array which represents an image.
    :param out_height: the resized image height
    :param out_width: the resized image width
    :param forward_implementation: a boolean flag that indicates whether forward or basic implementation is used.
                                    if forward_implementation is true then the forward-looking energy is used otherwise
                                    the basic implementation is used.
    :return: A dictionary with three elements, {'resized' : img1, 'vertical_seams' : img2 ,'horizontal_seams' : img3},
            where img1 is the resized image and img2/img3 are the visualization images
            (where the chosen seams are colored red and black for vertical and horizontal seams, respecitvely).
    """

    # initial values of given image
    gray_image = utils.to_grayscale(image)
    energy_matrix = utils.get_gradients(gray_image)

    # calculating the grey scale image dimensions
    height = gray_image.shape[0]
    width = gray_image.shape[1]

    # helper index matrix
    indices = index_matrix(height, width)

    # calculating the number of seams needed to be found
    vertical_seams_number = abs(width - out_width)
    horizontal_seams_number = abs(height - out_height)

    # flags to mark if we need to enlarge the image
    enlarge_width = width < out_width
    enlarge_height = height < out_height

    # structures to keep the seams of each direction
    # seam_counter = 0
    vertical_seams = np.empty([vertical_seams_number, height], dtype=int)
    horizontal_difference = width + vertical_seams_number if enlarge_width else width - vertical_seams_number
    horizontal_seams = np.empty([horizontal_seams_number, horizontal_difference], dtype=int)
    'width - vertical_seams_number = the size of a seam we will remove after (1) removal of vertical seams (2) rotation'
    'seam_counter in order to know which index to add the seam in the seam structure,'
    'add 1 when adding a seam to it at main loop using add_seam method below'

    if forward_implementation:
        for i in range(vertical_seams_number):
            cost_mat = calc_forward_cost_matrix(energy_matrix, gray_image, height, width - i)
            seam = find_forward_seam(cost_mat, energy_matrix, gray_image, indices, height)
            add_seam_to_seams(vertical_seams, seam, i)
            remove_seam(gray_image, indices, energy_matrix, seam)

    else:
        for i in range(vertical_seams_number):
            cost_mat = calc_basic_cost_matrix(energy_matrix, height, width - i)
            seam = find_basic_seam(cost_mat, indices, height, width - i)
            add_seam_to_seams(vertical_seams, seam, i)
            remove_seam(gray_image, indices, energy_matrix, seam)

    # creates the image with vertical seams colored in red, as well as a partially resized image
    indices = index_matrix(height, width)
    red_image, partially_resized_image = return_images(image, vertical_seams, indices, 0, enlarge_width)

    # rotating image and reassigning initial values
    rotated_image = np.rot90(partially_resized_image)
    gray_image = utils.to_grayscale(rotated_image)
    energy_matrix = utils.get_gradients(gray_image)
    height = gray_image.shape[0]
    width = gray_image.shape[1]
    indices = index_matrix(height, width)

    if forward_implementation:
        for i in range(horizontal_seams_number):
            cost_mat = calc_forward_cost_matrix(energy_matrix, gray_image, height, width - i)
            seam = find_forward_seam(cost_mat, energy_matrix, gray_image, indices, height)
            add_seam_to_seams(horizontal_seams, seam, i)
            remove_seam(gray_image, indices, energy_matrix, seam)

    else:
        for i in range(horizontal_seams_number):
            cost_mat = calc_basic_cost_matrix(energy_matrix, height, width - i)
            seam = find_basic_seam(cost_mat, indices, height, width - i)
            add_seam_to_seams(horizontal_seams, seam, i)
            remove_seam(gray_image, indices, energy_matrix, seam)

    indices = index_matrix(height, width)
    black_image, resized_image = return_images(rotated_image, horizontal_seams, indices, 1, enlarge_height)

    return {'resized': np.rot90(resized_image, -1),
            'vertical_seams': red_image,
            'horizontal_seams': np.rot90(black_image, -1)}
