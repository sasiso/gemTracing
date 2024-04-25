import cv2
import numpy as np
import os

# Load the image
image_path = './test/opal.jpeg'
assert os.path.exists(image_path)

img = cv2.imread(image_path)
assert img is not None
cv2.imshow("Window", img)
cv2.waitKey(1000)

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("Window", gray)


# Convert the grayscale image to 8-bit
gray = cv2.convertScaleAbs(gray)
cv2.imshow("Window", gray)
cv2.waitKey(1000)


# Apply median filter with a 5-pixel radius
median_blur = cv2.medianBlur(gray, 5)
cv2.imshow("Window", median_blur)
cv2.waitKey(1000)


# Find edges
edges = cv2.Canny(median_blur, 100, 200)

cv2.imshow("Window", edges)
cv2.waitKey(5)




inverted_img = cv2.bitwise_not(edges)
cv2.imshow("Window", inverted_img)

# Step 2: Find contours of the detected edges
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Assuming there's only one contour
contour = contours[0]

# Step 3: Draw a horizontal and a vertical line inside the contour
# Calculate the midpoint of the contour (center of the object)
M = cv2.moments(contour)
cx = int(M['m10'] / M['m00'])
cy = int(M['m01'] / M['m00'])

# Draw a horizontal line
cv2.line(edges, (cx - 50, cy), (cx + 50, cy), (255, 0, 0), 2)

# Draw a vertical line
cv2.line(edges, (cx, cy - 50), (cx, cy + 50), (255, 0, 0), 2)

# Display the image with lines
cv2.imshow('Image with lines', edges)
cv2.waitKey(0)


# Define the weights for each image
alpha = 0.5  # Weight for the first image
beta = 0.5   # Weight for the second image
gamma = 0    # Scalar added to each sum

# Superimpose the images
superimposed_img = cv2.addWeighted(gray, alpha, inverted_img, beta, gamma)
cv2.imshow("Window", superimposed_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
