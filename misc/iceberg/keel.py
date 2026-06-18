import cv2 
import os
import numpy as np
from math import *


script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "firer.png")

if not os.path.exists(file_path):
	print(f"Error: Could not find {file_path}")
else:
	img_raw = cv2.imread(file_path)
	wi,hi,thirdthing = img_raw.shape
	print(wi,hi)
	img = cv2.resize(img_raw,(1050, int(1050*(wi/hi))))

measure = True
if measure:
	
	clicks = []
	box_w = 1  

	def click_event(event, x, y, flags, params):
		global img,box_w
		global clicks
		if event == cv2.EVENT_LBUTTONDOWN:
			clicks.append((x, y))
			
			
			cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
			
			if len(clicks) >= 2 and len(clicks) % 2 == 0:
				if len(clicks) > 2:
					p1 = clicks[-2]
					p2 = clicks[-1]
					
					pixdist = dist(p1, p2)
					meas = round(pixdist / (box_w / 10), 2)
					
					cv2.line(img, p1, p2, (255, 0, 0), 2)
					cv2.putText(img, f"{meas} cm", p2, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
				else:
					p1 = clicks[-2]
					p2 = clicks[-1]
					
					pixdist = dist(p1, p2)
					box_w = pixdist
					meas = round(pixdist / (box_w / 10), 2)
					
					cv2.line(img, p1, p2, (255, 0, 0), 2)
					cv2.putText(img, f"{meas} cm", p2, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
			cv2.imshow('image', img)

	
	
		
	cv2.imshow('image', img)
	cv2.setMouseCallback('image', click_event)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	