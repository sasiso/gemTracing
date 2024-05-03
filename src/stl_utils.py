import cv2
import numpy as np
from stl import mesh

# Function to convert contour points from pixels to millimeters
def convert_contour_to_mm(contour, factor):
    return contour * factor

def save_stl(largest_contour, pixel_to_mm):
    # Define conversion factor from pixels to millimeters
    pixel_to_mm = 0.1  # You need to replace this with your actual conversion factor

    # Convert contour points to millimeters
    largest_contour_mm = convert_contour_to_mm(largest_contour, pixel_to_mm)

    # Create a 3D mesh from the contour
    vertices = np.array([largest_contour_mm[:, 0, :]], dtype=mesh.Mesh.dtype)
    stl_mesh = mesh.Mesh(np.zeros(len(vertices), dtype=mesh.Mesh.dtype))
    for i, vertex in enumerate(vertices):
        for j in range(3):
            stl_mesh.vectors[i][j] = vertex[j]

    # Save the mesh to an STL file
    stl_mesh.save('output_mesh.stl')
