import face_recognition as fr 
from picamera import PiCamera
import numpy as np
import csv

camera = PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8) # 3 is for RGB


#load encodings
known_face_encodings = []
names = []

with open("./encodings/features.csv","r") as f:
    reader = csv.reader(f)
    for row in reader:
        known_face_encodings.append(row[1:])
        names.append(row[0])

while True:
    camera.capture(output,format="rgb")
    
    face_locations = fr.face_locations(output)
    face_encodings = fr.face_encodings(output,face_locations)
    
    for face_encoding in face_encodings:
        pass