"""
detect faces and draw a box around them
"""
import os
import sys
import pickle
import cv2
import face_recognition
import functions

CAMINDEX = 0
SAVE_FILE = "encodings.pickle"
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONTSCALE = 1
TEXTCOLOUR = (255, 0, 0)
TOLERANCE = 0.4
if not os.path.exists(SAVE_FILE):
    data = {"encodings":[],"names":[]}
    print("No encoding file exists running face detection only")
else:
    with open(SAVE_FILE, "rb") as f:
        data = pickle.load(f)
Knownencodings = data["encodings"]
names = data["names"]

cap = functions.camera_connection(CAMINDEX)

while True:
    q , frame = cap.read()
    boxes = face_recognition.face_locations(frame)
    encodings = face_recognition.face_encodings(frame, boxes)
    matches = []
    foundnames = []
    for x,encoding in enumerate(encodings):
        matches = face_recognition.compare_faces(Knownencodings,encoding, tolerance = TOLERANCE)
        print(matches)
        if not matches:
            for i in boxes:
                matches.append(False)
        for e,i in enumerate(matches):
            print("BOXES:",boxes)
            top,right,bottom,left = boxes[x]
            cv2.rectangle(frame, (left,top), (right,bottom) , (0,255,0), 4)

            if i:
                foundnames.append(names[e])
                image = cv2.putText(frame, names[e], (left-20,top-20), FONT, FONTSCALE,
                TEXTCOLOUR, 1, cv2.LINE_AA, False)
            elif True not in matches:
                image = cv2.putText(frame, "Unknown", (left-20,top-20), FONT, FONTSCALE,
                TEXTCOLOUR, 1, cv2.LINE_AA, False)


    print("Found:",foundnames)
    cv2.imshow("window",frame)
    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()
sys.exit()
