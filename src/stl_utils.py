import numpy as np
from stl import mesh
import os


def get_save_path(file_name):
    # Get the current working directory
    current_directory = os.getcwd()
    print("Current working directory:", current_directory)

    # Navigate to the parent directory
    parent_directory = os.path.abspath("..")
    print("Parent directory:", parent_directory)

    # Define the path for the temporary directory
    stl_dir = os.path.join(parent_directory, "stl")
    # Check if the temporary directory exists
    if not os.path.exists(stl_dir):
        # Create the temporary directory if it doesn't exist
        os.makedirs(stl_dir)
        print("STL directory created at:", stl_dir)

    else:
        print("STL directory already exists at:", stl_dir)

    return os.path.join(stl_dir, file_name)


def generate_bezel(contour, pixel_to_mm, thickness=1, height=4, filename="bezel.stl"):
    # Reshape contour for mesh generation
    contour = contour.squeeze()

    # Extrude the contour to create the bezel
    points = []
    for point in contour:
        points.append([point[0] * pixel_to_mm, point[1] * pixel_to_mm, 0])  # Bottom points
        points.append([point[0] * pixel_to_mm, point[1] * pixel_to_mm, height])  # Top points

    # Extend the contour outward for thickness
    num_points = len(contour)
    for i in range(num_points):
        # Outer bottom point
        points.append([(contour[i][0] + thickness) * pixel_to_mm, (contour[i][1] + thickness) * pixel_to_mm, 0])

        # Outer top point
        points.append([(contour[i][0] + thickness) * pixel_to_mm, (contour[i][1] + thickness) * pixel_to_mm, height])

    # Create the side faces of the bezel
    faces = []
    for i in range(num_points - 1):
        # Side face indices
        bottom_left = i * 2
        bottom_right = bottom_left + 1
        top_left = (i + 1) * 2
        top_right = top_left + 1

        # Side face
        faces.append([bottom_left, bottom_right, top_right])
        faces.append([bottom_left, top_right, top_left])

        # Thickness extension face
        next_bottom_right = bottom_right + 2
        next_top_right = top_right + 2

        faces.append([bottom_right, next_bottom_right, next_top_right])
        faces.append([bottom_right, next_top_right, top_right])

    # Connect the last and first points to close the bezel
    bottom_left = (num_points - 1) * 2
    bottom_right = bottom_left + 1
    top_left = 0
    top_right = 1

    # Side face
    faces.append([bottom_left, bottom_right, top_right])
    faces.append([bottom_left, top_right, top_left])

    # Thickness extension face
    next_bottom_right = bottom_right + 2
    next_top_right = top_right + 2

    faces.append([bottom_right, next_bottom_right, next_top_right])
    faces.append([bottom_right, next_top_right, top_right])

    # Convert points and faces to numpy arrays
    points = np.array(points)
    faces = np.array(faces)

    # Create the mesh
    bezel_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            bezel_mesh.vectors[i][j] = points[f[j]]

    f = get_save_path(file_name=filename)
    # Write the mesh to an STL file
    bezel_mesh.save(f)
    return f


# Example usage:
# pixel_to_mm = vertical_line_length_mm / vertical_line_length_px
# contours = get_contours(your_image)
# for contour in contours:
#     generate_bezel(contour, pixel_to_mm, thickness=1, height=4)
