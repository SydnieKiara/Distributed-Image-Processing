import os
import json

IMAGE_DIR = "images"
TASK_FILE = "sample_task.json"

def validate_task_file():
    """
    Validate the sample task file.
    """
    if not os.path.exists(TASK_FILE):
        print(f"Task file '{TASK_FILE}' not found.")
        return

    with open(TASK_FILE, "r") as file:
        task_data = json.load(file)

    tasks = task_data.get("tasks", [])
    for task in tasks:
        image_name = task.get("image_name")
        if not image_name:
            print("Task missing 'image_name'.")
            continue

        image_path = os.path.join(IMAGE_DIR, image_name)
        if not os.path.exists(image_path):
            print(f"Image file '{image_name}' not found in '{IMAGE_DIR}'.")
        else:
            print(f"Validated task for image: {image_name}")

if __name__ == "__main__":
    validate_task_file()
