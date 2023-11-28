import threading
import cv2
from deepface import DeepFace

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) #define capture device

cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

count = 0 #this counter is so we dont check that every frame is a match to the face, but only once in a while

match = False #check if the face matches

reference_img = cv2.imread("Computer Security\Group Project\img.jpg") #define reference image
reference_img2 = cv2.imread("C:\Users\crisc\OneDrive\Pictures\Camera Roll\WIN_20231127_14_46_34_Pro.jpg")

def check_face(frame): #checks for a match
    global match
    try: #true if valid face and correct face
        if DeepFace.verify(frame, reference_img.copy())['verified']:
            match = True
        else: #false if valid face but wrong face
            match = False 
    except ValueError: #false if no face
        match = False


while True:
    ret, frame = cam.read() #ret = if it returned somehting; frame = get the frame if something was returned

    if ret:
        if count % 30 == 0:
            try:
                threading.Thread(target=check_face, args=(frame.copy(),)).start()
            except ValueError: #if there is no face recognized, pass
                cv2.putText(frame, "NO FACE!", (20,450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 3)
        count += 1

        if match: #display if the face matches
            cv2.putText(frame, "MATCH!", (20,450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        else: #display if the face doesnt match
            cv2.putText(frame, "NO MATCH!", (20,450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        cv2.imshow("Face ID Scanner", frame)

    key = cv2.waitKey(1) #process user input
    if key == ord("q"): #if 'q' is pressed break out of loop
        break

cv2.destroyAllWindows()