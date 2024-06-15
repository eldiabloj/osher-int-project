import os
import cv2
import numpy as np

class Img:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image_data = self.load_image()

    def load_image(self):
        try:
            image = cv2.imread(self.image_path)
            if image is not None:
                return image
            else:
                raise FileNotFoundError("Unable to load image.")
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def save_image(self, image_data, suffix='_filtered'):
        try:
            directory = 'images'
            if not os.path.exists(directory):
                os.makedirs(directory)

            file_path = os.path.join(directory, f"{os.path.basename(self.image_path).split('.')[0]}{suffix}.jpg")
            cv2.imwrite(file_path, image_data)
            print(f"Image saved successfully: {file_path}")
            return file_path
        except Exception as e:
            print(f"Error saving image: {e}")
            return None

    def blur(self, blur_level=16):
        try:
            if self.image_data is None:
                raise ValueError("No image data available.")
            blur_level = max(1, blur_level)
            blur_level = blur_level + 1 if blur_level % 2 == 0 else blur_level
            blurred_image = cv2.GaussianBlur(self.image_data, (blur_level, blur_level), 0)
            return blurred_image
        except Exception as e:
            print(f"Error applying blur: {e}")
            return None

    def rotate(self):
        try:
            img = cv2.imread(self.image_path)
            if img is None:
                raise FileNotFoundError("Unable to load image.")
            rotated_img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            return rotated_img
        except Exception as e:
            print(f"Error rotating image: {e}")
            return None

    def salt_n_pepper(self, amount=0.1):
        try:
            if self.image_data is None:
                raise ValueError("No image data available.")
            noisy_image = self.image_data.copy()
            mask = np.random.choice([0, 1, 2], size=noisy_image.shape[:2], p=[amount / 2, amount / 2, 1 - amount])
            noisy_image[mask == 0] = 0
            noisy_image[mask == 1] = 255
            return noisy_image
        except Exception as e:
            print(f"Error adding salt and pepper noise: {e}")
            return None

    def concat(self, other_image_data, direction='horizontal'):
        try:
            if self.image_data is None or other_image_data is None:
                raise ValueError("Image data is missing.")

            if direction not in ['horizontal', 'vertical']:
                raise ValueError("Invalid direction. Please use 'horizontal' or 'vertical'.")

            if direction == 'horizontal':
                concatenated_img = np.concatenate((self.image_data, other_image_data), axis=1)
            else:
                concatenated_img = np.concatenate((self.image_data, other_image_data), axis=0)

            return concatenated_img
        except Exception as e:
            print(f"Error concatenating images: {e}")
            return None

    def segment(self, num_clusters=100):
        try:
            if self.image_data is None:
                raise ValueError("No image data available.")

            # Convert image to RGB color space
            image_rgb = cv2.cvtColor(self.image_data, cv2.COLOR_BGR2RGB)

            # Reshape image data to 2D array of pixels
            pixels = image_rgb.reshape((-1, 3)).astype(np.float32)

            # Define criteria for k-means clustering
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

            # Perform k-means clustering
            _, labels, centers = cv2.kmeans(pixels, num_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

            # Convert centers to 8-bit unsigned integer format
            centers = np.uint8(centers)

            # Map each pixel to its corresponding cluster center
            segmented_image = centers[labels.flatten()]

            # Reshape segmented image back to original shape
            segmented_image = segmented_image.reshape(image_rgb.shape)

            # Convert segmented image back to BGR color space
            segmented_image_bgr = cv2.cvtColor(segmented_image, cv2.COLOR_RGB2BGR)

            # Darken the segmented image
            segmented_image_bgr = segmented_image_bgr * 0.5  # Reduce brightness by 50%

            return segmented_image_bgr
        except Exception as e:
            print(f"Error segmenting image: {e}")
            return None

    def convert_to_grayscale(self):
        try:
            if self.image_data is None:
                raise ValueError("No image data available.")

            gray_image = cv2.cvtColor(self.image_data, cv2.COLOR_BGR2GRAY)
            return gray_image  # Return the grayscale image directly
        except Exception as e:
            print(f"Error converting image to grayscale: {e}")
            return None

    def adjust_brightness(self, alpha=1.5, beta=0):
        try:
            if self.image_data is None:
                raise ValueError("No image data available.")

            # Perform brightness adjustment
            adjusted_image = cv2.convertScaleAbs(self.image_data, alpha=alpha, beta=beta)

            return adjusted_image
        except Exception as e:
            print(f"Error adjusting brightness: {e}")
            return None

    # def blend_images(self, other_image_data, alpha=0.5):
    #     try:
    #         if self.image_data is None or other_image_data is None:
    #             raise ValueError("Image data is missing.")
    #
    #         # Resize other_image_data to match self.image_data if needed
    #         resized_other_image = cv2.resize(other_image_data, (self.image_data.shape[1], self.image_data.shape[0]))
    #
    #         # Blend images using alpha blending
    #         blended_image = cv2.addWeighted(self.image_data, alpha, resized_other_image, 1 - alpha, 0)
    #
    #         return blended_image
    #     except Exception as e:
    #         print(f"Error blending images: {e}")
    #         return None


