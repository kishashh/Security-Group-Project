# Integrating my python code into my html code (index.html)

from flask import Flask, render_template, request
import cv2
import numpy as np
import os

app = Flask(__name__)

def compare_signatures(template_path, target_path, match_threshold=130):
    # Your existing compare_signatures function here

    # Read the template and target images
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    target = cv2.imread(target_path, cv2.IMREAD_GRAYSCALE)

    # Initialize the ORB detector
    orb = cv2.ORB_create()

    # Find the key points and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(template, None)
    kp2, des2 = orb.detectAndCompute(target, None)

    # Create a BFMatcher (Brute Force Matcher) object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors
    matches = bf.match(des1, des2)

    # Sort them in ascending order of distance
    matches = sorted(matches, key=lambda x: x.distance)

    # Check if the number of matches exceeds the threshold
    if len(matches) >= match_threshold:
        print(f"Signatures are a potential match! (Matches: {len(matches)})")
    else:
        print(f"Signatures do not match. (Matches: {len(matches)})")

    # Draw the first 10 matches
    img_matches = cv2.drawMatches(template, kp1, target, kp2, matches[:130], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # Display the matches
    cv2.imshow('ORB Feature Matches', img_matches)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', error='No selected file')

    # Save the uploaded file to a temporary location
    temp_path = 'temp_uploaded_image.png'
    file.save(temp_path)

    # Define the paths for the template and target images
    template_path = "C:\\Users\\crisc\\Downloads\\signature (4).png"
    target_path = temp_path

    # Call the compare_signatures function
    compare_signatures(template_path, target_path, match_threshold=130)

    # Remove the temporary uploaded file
    os.remove(temp_path)

    return render_template('index.html', success='Comparison completed successfully')

if __name__ == '__main__':
    app.run(debug=True)
