''''

from skimage import io, metrics
import matplotlib.pyplot as plt

def compare_signatures(image_path1, image_path2):
    # Load images
    signature1 = io.imread(image_path1, as_gray=True)
    signature2 = io.imread(image_path2, as_gray=True)

    # Compare images using Structural Similarity Index (SSI)
    ssi_index = metrics.structural_similarity(signature1, signature2)

    # Display the images and the SSI index
    plt.subplot(1, 3, 1)
    plt.imshow(signature1, cmap='gray')
    plt.title('Signature 1')

    plt.subplot(1, 3, 2)
    plt.imshow(signature2, cmap='gray')
    plt.title('Signature 2')

    plt.subplot(1, 3, 3)
    plt.text(0.5, 0.5, f'SSI Index: {ssi_index:.2f}', ha='center', va='center', fontsize=12)
    plt.axis('off')
    plt.show()

    # Return the SSI index for further analysis or thresholding
    return ssi_index

# Example usage
image_path1 = 'path/to/signature1.png'
image_path2 = 'path/to/signature2.png'

ssi_index = compare_signatures(image_path1, image_path2)
print(f'Structural Similarity Index: {ssi_index:.2f}')

'''

import cv2
import numpy as np

def compare_signatures(template_path, target_path, threshold=0.8):
    # Read the template and target images
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    target = cv2.imread(target_path, cv2.IMREAD_GRAYSCALE)

    # Perform template matching
    result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # If the maximum correlation coefficient is above the threshold, consider it a match
    if max_val > threshold:
        print("Signatures match!")
        # You can also draw a rectangle around the matched region if needed
        h, w = template.shape
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(target, top_left, bottom_right, 255, 2)
        
        # Display the images with the matching region highlighted
        cv2.imshow('Matching Result', target)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Signatures do not match.")

# Example usage
# template_path = 'path/to/signature_template.png'
template_path = 'C:\Users\crisc\Downloads\signature (4).png'

# target_path = 'path/to/target_image.png'
target_path = 'C:\Users\crisc\Downloads\signature (5).png'

compare_signatures(template_path, target_path)
