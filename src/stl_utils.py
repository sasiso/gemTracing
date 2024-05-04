import numpy as np
import cv2
from stl import mesh

def generate_bezel(contour, pixel_to_mm, thickness=1, height=4):
    # Reshape contour for mesh generation
    contour = contour.squeeze()

    # Extrude the contour to create the bezel
    points = []
    for point in contour:
        points.append([point[0] * pixel_to_mm, point[1] * pixel_to_mm, 0])  # Bottom points
        points.append([point[0] * pixel_to_mm, point[1] * pixel_to_mm, height])  # Top points

    # Extend the contour inward for thickness
    for point in contour[::-1]:
        points.append([point[0] * pixel_to_mm - thickness, point[1] * pixel_to_mm - thickness, 0])  # Bottom points
        points.append([point[0] * pixel_to_mm - thickness, point[1] * pixel_to_mm - thickness, height])  # Top points

    # Create the side faces of the bezel
    faces = []
    num_points = len(contour)
    for i in range(num_points - 1):
        # Side face indices
        bottom_left = i * 2
        bottom_right = bottom_left + 1
        top_left = (i + 1) * 2
        top_right = top_left + 1

        # Side face
        faces.append([bottom_left, bottom_right, top_right])
        faces.append([bottom_left, top_right, top_left])

    # Connect the last and first points to close the bezel
    faces.append([num_points * 2 - 2, num_points * 2 - 1, 1])
    faces.append([num_points * 2 - 2, 1, 0])

    # Add faces for the thickness extension
    for i in range(num_points - 1):
        bottom_left = (num_points + i) * 2
        bottom_right = bottom_left + 1
        top_left = (num_points + i + 1) * 2
        top_right = top_left + 1

        faces.append([bottom_left, bottom_right, top_right])
        faces.append([bottom_left, top_right, top_left])

    # Connect the last and first points of the thickness extension
    faces.append([(num_points * 2 - 2) + num_points * 2, num_points * 2, num_points * 2 + 1])
    faces.append([(num_points * 2 - 2) + num_points * 2, num_points * 2 + 1, (num_points * 2 - 2) + 1])

    # Convert points and faces to numpy arrays
    points = np.array(points)
    faces = np.array(faces)

    # Create the mesh
    bezel_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            bezel_mesh.vectors[i][j] = points[f[j]]

    # Write the mesh to an STL file
    bezel_mesh.save('bezel.stl')

# Example usage:
# pixel_to_mm = vertical_line_length_mm / vertical_line_length_px
# contours = get_contours(your_image)
# for contour in contours:
#     generate_bezel(contour, pixel_to_mm, thickness=1, height=4)
