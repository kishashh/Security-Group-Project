import os
from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import base64

app = Flask(__name__)
email = "chris"
def sig_checker(template, target, match_threshold=110, similarity_threshold=0.75):
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

    # # Check if the number of matches exceeds the threshold
    # if len(matches) >= 130:  # Adjust the threshold as needed
    #     return {"match": True, "num_matches": len(matches)}
    # else:
    #     return {"match": False, "num_matches": len(matches)}

    # Check if the number of matches exceeds the threshold
    if len(matches) >= match_threshold:
        # Calculate the similarity as the ratio of good matches to total matches
        good_matches = [m for m in matches if m.distance < match_threshold]
        similarity = len(good_matches) / len(matches)

        # Check if the similarity exceeds the similarity threshold
        if similarity >= similarity_threshold:
            return {"match": True, "num_matches": len(matches), "similarity": similarity}
        else:
            return {"match": False, "num_matches": len(matches), "similarity": similarity}
    else:
        return {"match": False, "num_matches": len(matches), "similarity": 0.0}

@app.route('/')
def index():
    return render_template('signature.html')

@app.route('/upload_signature', methods=['POST'])
def upload_signature():
    try:
        data = request.get_json()
        signature_data = data.get('signatureImage')

        # Decode the base64 encoded image data
        signature_np = np.frombuffer(
            np.frombuffer(base64.b64decode(signature_data.split(',')[1]), np.uint8),
            np.uint8
        )

        # Reshape the flattened array to an image
        signature_img = cv2.imdecode(signature_np, cv2.IMREAD_GRAYSCALE)

        # Example template path (replace with the actual path)
        # template_path = "path/to/your/template_image.png"
        template_path = "sigref"
        os.path.join(template_path, email)

        # Perform signature comparison
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        result = sig_checker(template, signature_img)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
