# from flask import Flask, render_template, request
# import cv2
# import numpy as np
# import base64

# app = Flask(__name__)

# def compare_signatures(template_path, target_data, match_threshold=130):

#     target_data_parts = target_data.split(',')
    
#     if len(target_data_parts) < 2:
#         print("Invalid target data format.")
#         return  # or handle the error in another way
    
#     # target_bytes = base64.b64decode(target_data_parts[1])
#     target_bytes = base64.b64decode(target_data)

#     target_np = np.frombuffer(target_bytes, np.uint8)
#     target = cv2.imdecode(target_np, cv2.IMREAD_GRAYSCALE)

#     # # Convert base64 image data to NumPy array
#     # target_bytes = base64.b64decode(target_data.split(',')[1])
#     # target_np = np.frombuffer(target_bytes, np.uint8)
#     # target = cv2.imdecode(target_np, cv2.IMREAD_GRAYSCALE)

#     # ... (rest of the code remains unchanged)
#     template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
#     target = cv2.imread(target_path, cv2.IMREAD_GRAYSCALE)

#     # Initialize the ORB detector
#     orb = cv2.ORB_create()

#     # Find the key points and descriptors with ORB
#     kp1, des1 = orb.detectAndCompute(template, None)
#     kp2, des2 = orb.detectAndCompute(target, None)

#     # Create a BFMatcher (Brute Force Matcher) object
#     bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

#     # Match descriptors
#     matches = bf.match(des1, des2)

#     # Sort them in ascending order of distance
#     matches = sorted(matches, key=lambda x: x.distance)

#     # Check if the number of matches exceeds the threshold
#     if len(matches) >= match_threshold:
#         print(f"Signatures are a potential match! (Matches: {len(matches)})")
#     else:
#         print(f"Signatures do not match. (Matches: {len(matches)})")

#     # Draw the first 10 matches
#     img_matches = cv2.drawMatches(template, kp1, target, kp2, matches[:130], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

#     # Display the matches
#     cv2.imshow('ORB Feature Matches', img_matches)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#     # Check if the number of matches exceeds the threshold
#     if len(matches) >= match_threshold:
#         return f"Signatures are a potential match! (Matches: {len(matches)})"
#     else:
#         return f"Signatures do not match. (Matches: {len(matches)})"
    
#     # If the number of matches is less than 130, display a message
#     if len(matches) < 130:
#         print("Insufficient matches for meaningful comparison. Increase match_threshold or check the input images.")
#     else:
#         # Draw the first 10 matches
#         img_matches = cv2.drawMatches(template, kp1, target, kp2, matches[:130], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

#         # Display the matches
#         cv2.imshow('ORB Feature Matches', img_matches)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/compare', methods=['POST'])
# def compare():
#     # template_path = "path/to/your/template/image.png"  # Set the path to your template image
#     template_path = "C:\\Users\\crisc\\Downloads\\signature (4).png" # Test Signature

#     target_data = request.form['signatureData']
#     result = compare_signatures(template_path, target_data, match_threshold=130)
#     return render_template('index.html', result=result)

# if __name__ == '__main__':
#     app.run(debug=True)

########################################################################################################## 1:14a

# from flask import Flask, render_template, request
# import cv2
# import numpy as np
# import base64

# app = Flask(__name__)

# def compare_signatures(template_path, target_data, match_threshold=130):

#     target_data_parts = target_data.split(',')
    
#     if len(target_data_parts) < 2:
#         print("Invalid target data format.")
#         return  # or handle the error in another way
    
#     target_bytes = base64.b64decode(target_data_parts[1])

#     target_np = np.frombuffer(target_bytes, np.uint8)
#     target = cv2.imdecode(target_np, cv2.IMREAD_GRAYSCALE)

#     # Read the template image
#     template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

#     # Initialize the ORB detector
#     orb = cv2.ORB_create()

#     # Find the key points and descriptors with ORB
#     kp1, des1 = orb.detectAndCompute(template, None)
#     kp2, des2 = orb.detectAndCompute(target, None)

#     # Create a BFMatcher (Brute Force Matcher) object
#     bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

#     # Match descriptors
#     matches = bf.match(des1, des2)

#     # Sort them in ascending order of distance
#     matches = sorted(matches, key=lambda x: x.distance)

#     # Check if the number of matches exceeds the threshold
#     if len(matches) >= match_threshold:
#         print(f"Signatures are a potential match! (Matches: {len(matches)})")
#     else:
#         print(f"Signatures do not match. (Matches: {len(matches)})")

#     # Draw the first 10 matches
#     img_matches = cv2.drawMatches(template, kp1, target, kp2, matches[:130], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

#     # Display the matches
#     cv2.imshow('ORB Feature Matches', img_matches)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#     # Check if the number of matches exceeds the threshold
#     if len(matches) >= match_threshold:
#         return f"Signatures are a potential match! (Matches: {len(matches)})"
#     else:
#         return f"Signatures do not match. (Matches: {len(matches)})"

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/compare', methods=['POST'])
# def compare():
#     # template_path = "path/to/your/template/image.png"  # Set the path to your template image
#     template_path = "C:\\Users\\crisc\\Downloads\\signature (4).png" # Test Signature

#     target_data = request.form['signatureData']
#     print("Received target_data:", target_data)


# # Ensure that the target data is a valid base64 string
#     try:
#         target_data_parts = target_data.split(',')
#         if len(target_data_parts) < 2:
#             raise ValueError("Invalid target data format.")
        
#         target_bytes = base64.b64decode(target_data_parts[1])
#     except Exception as e:
#         print(f"Error decoding target data: {e}")
#         result = "Error decoding target data"
#         return render_template('index.html', result=result)



#     result = compare_signatures(template_path, target_data, match_threshold=130)
#     return render_template('index.html', result=result)

# if __name__ == '__main__':
#     app.run(debug=True)




from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np

app = Flask(__name__)

def compare_signatures(template, target):
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
    if len(matches) >= 130:  # Adjust the threshold as needed
        return {"match": True, "num_matches": len(matches)}
    else:
        return {"match": False, "num_matches": len(matches)}

@app.route('/')
def index():
    return render_template('index.html')

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
        template_path = "C:\\Users\\crisc\\Downloads\\signature (4).png"

        # Perform signature comparison
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        result = compare_signatures(template, signature_img)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
