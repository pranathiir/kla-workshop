from PIL import Image
import csv
import cv2
import json

f = open('input.json')
data = json.load(f)

x_start = data['care_areas'][0]['top_left']['x']
y_start = data['care_areas'][0]['bottom_right']['y']
x_end = data['care_areas'][0]['bottom_right']['x']
y_end = data['care_areas'][0]['top_left']['y']

color_count = {}
totalDefects = []

for i in range(1, 6):
    img = Image.open("D:\Placement\kla\level1\wafer_image_{0}.png".format(i))
    img = img.convert('RGB')
    pixels = img.load()
    
    for y in range(y_start, y_end):
        for x in range(x_start, x_end):
            color = pixels[x, y]
            if(color in color_count):
                color_count[color] += 1
            else:
                color_count[color] = 1
    
    most = {} 
    maxcol1 = max(color_count.values())
    
    for key in color_count:
        if(color_count[key] == maxcol1):
            most_col1 = key
    
    most[most_col1] = color_count.pop(most_col1)
    maxcol2 = max(color_count.values())
    
    for key in color_count:
        if(color_count[key] == maxcol2):
            most_col2 = key
            
    most[most_col2] = color_count.pop(most_col2)
    defects = []
    defect_coords = []
    
    for y in range(y_start, y_end):
        for x in range(x_start, x_end):
            color = pixels[x, y]
            if(color != most_col1 and color != most_col2):
                defects.append((i, x, y_end-y-1)) #flips the image

    with open("outputs.csv", "a+") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(defects)
