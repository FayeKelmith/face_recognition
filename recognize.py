import face_recognition as fr 
from picamera import PiCamera
import numpy as np
import csv
import logging 
from datetime import datetime
from database import getAttendee, addAttendee

camera = PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8) # 3 is for RGB


#encodings from csv variables
known_face_encodings = []
names = []

# mark attendance
def attendance(name: str):
    
    current_day = datetime.now().strftime("%Y-%m-%d") # format: YYYY:MM:DD
    
    existing_attendee = getAttendee(name, current_day)
    
    if existing_attendee == 0:
        addAttendee(name)
        logging.info(f"Added {name} to the database.")
    else:
        logging.info(f"{name} already marked present.")
    
    
# loading encodings from csv
def get_faces_registered():
    with open("./encodings/features.csv","r") as f:
        reader = csv.reader(f)
        for row in reader:
            known_face_encodings.append(row[1:])
            names.append(row[0])
    
    if len(known_face_encodings):
        logging.info("Loaded encodings successfully.")
        return True
    
    logging.error("Failed to load encodings.")
    return False


    
def main():
    
    get_faces_registered() # load encodings
    
    logging.basicConfig(filename="recognize.log",level=logging.INFO)
    while True:
        
        if get_faces_registered():
            camera.capture(output,format="rgb") #capture image
            
            face_locations = fr.face_locations(output)
            face_encodings = fr.face_encodings(output,face_locations)
            
            for face_encoding in face_encodings:
                result = fr. compare_faces(known_face_encodings,face_encoding) # returns a list of True/False
                if True in result:
                    index = result.index(True)
                    logging.info("Marking {} present.".format(names[index]))
                    
                    attendance(names[index]) # add to database
                
                
        else:
            logging.error("No faces registered.")
            break

if __name__ == "__main__":
    main()