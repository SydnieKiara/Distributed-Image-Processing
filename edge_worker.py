from PIL import Image, ImageFilter
import os

def process_edge_detection(image_path, output_path):
    """
    Apply edge detection to an image and save it to the output path.
    """
    try:
        image = Image.open(image_path)
        edge_image = image.filter(ImageFilter.FIND_EDGES)
        edge_image.save(output_path)
        print(f"Edge-detected image saved to {output_path}")
    except Exception as e:
        print(f"Error processing edge detection: {e}")

def handle_edge_detection_task(task):
    """
    Handle edge detection task by calling the process_edge_detection function.
    """
    image_name = task["image_name"]
    client_id = task["client_id"]
    input_image_path = os.path.join("images", image_name)
    output_image_path = os.path.join("client_results", f"{client_id}_edge.jpg")

    # Process the image
    process_edge_detection(input_image_path, output_image_path)
    return {"client_id": client_id, "status": "edge processed", "output": output_image_path}
