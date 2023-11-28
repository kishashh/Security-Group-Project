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
