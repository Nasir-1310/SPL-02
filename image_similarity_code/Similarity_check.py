import os
import cv2
from skimage.metrics import structural_similarity as ssim

# Function to compute structural similarity index between two images
def compute_ssim(image1_path, image2_path):
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    return ssim(img1_gray, img2_gray)

# Path to the folder containing screenshots
screenshots_folder = "Screenshots"

# Path to the folder where similar pictures will be moved
similar_picture_folder = "similarPictures"

# Create the similar picture folder if it doesn't exist
if not os.path.exists(similar_picture_folder):
    os.makedirs(similar_picture_folder)

# Iterate through each screenshot in the folder
for filename1 in os.listdir(screenshots_folder):
    image1_path = os.path.join(screenshots_folder, filename1)
    # Skip if the file is not an image
    if not image1_path.endswith(('.png', '.jpg', '.jpeg')):
        continue
    # Compare with other screenshots
    for filename2 in os.listdir(screenshots_folder):
        image2_path = os.path.join(screenshots_folder, filename2)
        # Skip if comparing with itself or if the file is not an image
        if filename1 == filename2 or not image2_path.endswith(('.png', '.jpg', '.jpeg')):
            continue
        # Compute SSIM between the current pair of images
        similarity = compute_ssim(image1_path, image2_path)
        # Define a threshold for similarity
        similarity_threshold = 0.9
        # If similarity is above the threshold, move one of the similar images to the similar picture folder
        if similarity > similarity_threshold:
            # Determine which image to keep in the Screenshots folder and which to move
            # For example, keep the image with the higher filename
            if filename1 > filename2:
                os.rename(image2_path, os.path.join(similar_picture_folder, filename2))
            else:
                os.rename(image1_path, os.path.join(similar_picture_folder, filename1))
            break  # Stop comparing with other screenshots for this image

print("Similar pictures have been moved to the 'similarPictures' folder.")
