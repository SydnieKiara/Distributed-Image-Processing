import os

IMAGE_DIR = "images"

def list_images():
    """
    List all image files in the images directory.
    """
    if os.path.exists(IMAGE_DIR):
        images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        print("Found images:", images)
    else:
        print(f"Image directory '{IMAGE_DIR}' does not exist!")

if __name__ == "__main__":
    list_images()
