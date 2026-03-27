import cv2
import numpy as np
import os

# Define your constant
img = cv2.imread(os.path.join(os.path.dirname(__file__), "test.png"))

w = np.array([191, 155, 77], dtype=np.uint8)

if img is not None:
    img = np.clip(img.astype(np.int16) * 2 - w, 0, 255).astype(np.uint8)

    cv2.imshow("gloop", img)
    cv2.waitKey(0)
