import cv2
import numpy as np

# Load the image
image_path = '1.jpg'
img = cv2.imread(image_path)
cv2.imshow("Window", img)
cv2.waitKey(5)

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("Window", gray)


# Convert the grayscale image to 8-bit
gray = cv2.convertScaleAbs(gray)
cv2.imshow("Window", gray)
cv2.waitKey(5)


# Apply median filter with a 5-pixel radius
median_blur = cv2.medianBlur(gray, 5)
cv2.imshow("Window", median_blur)
cv2.waitKey(5)


# Calculate histogram
hist = cv2.calcHist([median_blur], [0], None, [256], [0, 256])

# Find the threshold value by analyzing the histogram
total_pixels = median_blur.shape[0] * median_blur.shape[1]
bright_area_threshold = 0.2  # Adjust this value as needed
bright_area_threshold_pixel = int(total_pixels * bright_area_threshold)

cumulative_sum = 0
threshold_value = 0
for i in range(256):
    cumulative_sum += hist[i]
    if cumulative_sum > bright_area_threshold_pixel:
        threshold_value = i
        break

# Apply thresholding
_, threshold = cv2.threshold(median_blur,240, 255, cv2.THRESH_BINARY)

cv2.imshow("Window", threshold)
cv2.waitKey(0)


# Find edges
edges = cv2.Canny(threshold, 255, 240)

cv2.imshow("Window", edges)
cv2.waitKey(5)
inverted_img = cv2.bitwise_not(edges)
cv2.imshow("Window", inverted_img)


# Define the weights for each image
alpha = 0.5  # Weight for the first image
beta = 0.5   # Weight for the second image
gamma = 0    # Scalar added to each sum

# Superimpose the images
superimposed_img = cv2.addWeighted(gray, alpha, inverted_img, beta, gamma)
cv2.imshow("Window", superimposed_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
