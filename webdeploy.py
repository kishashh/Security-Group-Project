import cv2, numpy, os,time
from flask import Flask, render_template, request, redirect, url_for, Response, session

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/facerec', methods=['GET', 'POST'])
def facerec():
    global email
    email = request.form.get('email') # Get the email from the form
    session['email'] = email # Store email in session
    print("Email received:", session['email']) #Print for test
    # ,redirect(url_for('test'))
    return render_template('facerec.html', email=email)

size = 1 # change this to 4 to speed up processing trade off is the accuracy
classifier = 'haarcascade_frontalface_default.xml'
image_dir = 'imgref'
print("Face Recognition Starting ...")
# Create a list of images,labels,dictionary of corresponding names
(images, labels, names, id) = ([], [], {}, 0)
# Get the folders containing the training data
for (subdirs, dirs, files) in os.walk(image_dir):
    # Loop through each folder named after the subject in the photos
    for subdir in dirs:
        names[id] = subdir
        
        subjectpath = os.path.join(image_dir, subdir)
        # Loop through each photo in the folder
        for filename in os.listdir(subjectpath):
            # Skip non-image formats
            f_name, f_extension = os.path.splitext(filename)
            if(f_extension.lower() not in
                    ['.png','.jpg','.jpeg','.gif','.pgm']):
                print("Skipping "+filename+", wrong file type")
                continue
            path = subjectpath + '/' + filename
            label = id
            # Add to training data
            images.append(cv2.imread(path, 0))
            labels.append(int(label))
        id += 1
(im_width, im_height) = (120, 120)
# Create a Numpy array from the two lists above
(images, labels) = [numpy.array(lis) for lis in [images, labels]]
model = cv2.face.LBPHFaceRecognizer_create()
model.train(images, labels)
haar_cascade = cv2.CascadeClassifier(classifier)
webcam = cv2.VideoCapture(0) #  0 to use webcam
def process():
    while True:
        # Loop until the camera is working
        rval = False
        while(not rval):
            # Put the image from the webcam into 'frame'
            (rval, frame) = webcam.read()
            if(not rval):
                print("Failed to open webcam. Trying again...")
        startTime = time.time()
        # Flip the image (optional)
        frame=cv2.flip(frame,1) # 0 = horizontal ,1 = vertical , -1 = both
        # Convert to grayscalel
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Resize to speed up detection (optinal, change size above)
        mini = cv2.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))
        # Detect faces and loop through each one
        faces = haar_cascade.detectMultiScale(mini)
        for i in range(len(faces)):
            face_i = faces[i]
            # Coordinates of face after scaling back by size
            (x, y, w, h) = [v * size for v in face_i]
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (im_width, im_height))
            start =(x, y)
            end =(x + w, y + h)
            # Try to recognize the face
            prediction = model.predict(face_resize)
            #print(names, prediction)
            cv2.rectangle(frame,start , end, (255, 255, 255), 3) # creating a bounding box for detected face
            cv2.rectangle(frame, (start[0],start[1]-20), (start[0]+120,start[1]), (255, 255, 255), -3) # creating  rectangle on the upper part of bounding box
            #for i in prediction[1]
            # TODO: Fix formatting of unknown
            # TODO: Fix formatting of frame so it looks nice
            # TODO: Change colors for unknown scanning and match to red yellow green
            if prediction[1]<60 and email.lower() == names[prediction[0]].lower(): # Matches if lowercase version of email and predicted name are the same
                cv2.rectangle(frame,start , end, (0, 255, 0), 3) # green box when its a match
                cv2.rectangle(frame, (start[0],start[1]-20), (start[0]+120,start[1]), (0, 255, 0), -3) # green box when its a match
                cv2.putText(frame, 'MATCH!',(x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX,0.6,(0, 0, 0),thickness=2)
                print('%s - %.0f' % (names[prediction[0]],prediction[1]) + " MATCH!")
            elif prediction[1]<90 :  # NOTE: 0 is the perfect match  the higher the value the lower the accuracy
                cv2.rectangle(frame,start , end, (0, 255, 255), 3) # yellow box when its Scanning
                cv2.rectangle(frame, (start[0],start[1]-20), (start[0]+120,start[1]), (0, 255, 255), -3) # yellow box when its Scanning
                cv2.putText(frame,'Scanning',(x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX,0.6,(0, 0, 0),thickness=2)
                print('%s - %.0f' % (names[prediction[0]],prediction[1]))
            else: #If face isnt seen its unknown
                cv2.rectangle(frame,start , end, (0, 0, 255), 3) # red box when its unknown
                cv2.rectangle(frame, (start[0],start[1]-20), (start[0]+120,start[1]), (0, 0, 255), -3) # red box when its unknown
                cv2.putText(frame,("Unknown {} ".format(str(int(prediction[1])))),(x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0, 0, 0),thickness=2)
                print("Unknown -",prediction[1])
        endTime = time.time()
        fps = 1/(endTime-startTime)   
        cv2.rectangle(frame,(30,48),(130,70),(0,0,0),-1)
        cv2.putText(frame,"Fps : {} ".format(str(int(fps))),(34,65),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,255),2)
        # Show the image and check for "q" being pressed
        #cv2.imshow('Recognition System', frame)
        ret, buffer = cv2.imencode('.jpg', frame) #compress and store image to memory buffer
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') #concat frame one by one and return frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    webcam.release()
    cv2.destroyAllWindows()

@app.route('/video_feed')
def video_feed():
    #Video streaming route
    return Response(process(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='192.168.56.1',port='5000', debug=False,threaded = True)
# Matts Laptop  : 10.204.154.133
# Matts PC      : 192.168.56.1