import cv2

def get_contours(img):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.convertScaleAbs(gray)
    median_blur = cv2.medianBlur(gray, 5)

    edges = cv2.Canny(median_blur, 100, 200)

    ret, thresh = cv2.threshold(edges, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours
