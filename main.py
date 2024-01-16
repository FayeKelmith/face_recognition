import cv2 as cv
import face_recognition as fr 

font = cv.FONT_HERSHEY_SIMPLEX

width = 640
height = 360
cam = cv.VideoCapture(0)
cam.set(cv.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv.CAP_PROP_FPS, 15)
cam.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))


kelmith = fr.load_image_file("./images/known/Faye Kelmith.jpg")
#detect face location
faceLocation = fr.face_locations(kelmith)[0]
#encode face
donFaceEncoding = fr.face_encodings(kelmith)[0]

# Nancy Pelosi

nancy = fr.load_image_file("./images/known/Nancy Pelosi.jpg")
nancyFaceLocation = fr.face_locations(nancy)[0]
nancyFaceEncoding = fr.face_encodings(nancy)[0]

#bookkeeping
knownEncodings = [donFaceEncoding, nancyFaceEncoding]
names = ["Faye Kelmith", "Nancy Pelosi"]

#unknown image

while True:
    ignore, unknown = cam.read()
    
    unknownFace = cv.cvtColor(unknown, cv.COLOR_RGB2BGR)
    
    faceLocations = fr.face_locations(unknown)
    unknownFaceEncodings = fr.face_encodings(unknown, faceLocations)


    for face_location,unknownEncoding in zip(faceLocations,unknownFaceEncodings):
        top,right,bottom,left = face_location
        #print(f"Face Locations : {face_location}")
        cv.rectangle(unknownFace,(left,top),(right,bottom),(255,0,0),3)
        name = "Unknown Person"
        matches = fr.compare_faces(knownEncodings,unknownEncoding)
        print(matches)
        
        if True in matches:
            matchIndex = matches.index(True)
            print(matchIndex)
            name = names[matchIndex]
        cv.putText(unknownFace,name,(left,top),font, 0.75,(0,0,255),2)
    cv.imshow("Faces",unknownFace)
    
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv.destroyAllWindows()