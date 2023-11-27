import threading
import cv2
from deepface import DeepFace

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) #define capture device

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

count = 0 #this counter is so we dont check that every frame is a match to the face, but only once in a while

facenum = 0

reference_img = cv2.imread("img.jpg") #define reference image

def check_face(frame): #checks for a match
    global facenum
    try: #true if valid face and correct face
        if DeepFace.verify(frame, reference_img.copy())['verified']:
            facenum = 2
        else: #false if valid face but wrong face
            facenum = 1
    except ValueError: #false if no face
        facenum = 0

while True:
    ret, frame = cam.read() #ret = if it returned somehting; frame = get the frame if something was returned

    if ret:
        if count % 30 == 0:
            try:
                threading.Thread(target=check_face, args=(frame.copy(),)).start()
            except ValueError: #if there is no face recognized, pass
                pass
        count += 1

        if facenum == 2: #display if the face matches
                cv2.putText(frame, "MATCH!", (20,450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        elif facenum == 1: #display if face is detected but doesnt match
            cv2.putText(frame, "NO MATCH.", (20,450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 3)
        else: #display if no face is detected
            cv2.putText(frame, "NO FACE.", (20,450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        cv2.imshow("Face ID Scanner", frame)

    key = cv2.waitKey(1) #process user input
    if key == ord("q"): #if 'q' is pressed break out of loop
        break

cv2.destroyAllWindows()