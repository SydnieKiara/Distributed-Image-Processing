from PIL import Image
import os
import socket
import pickle

def process_resize(image_path, output_path, dimensions):
    """
    Resize an image to the specified dimensions and save it to the output path.
    """
    try:
        image = Image.open(image_path)
        resized_image = image.resize(dimensions)
        resized_image.save(output_path)
        print(f"[Resize Worker] Resized image saved to {output_path}")
    except Exception as e:
        print(f"[Resize Worker] Error processing resize image: {e}")

def handle_resize_task(task):
    """
    Handle resize task by calling the process_resize function.
    """
    image_name = task["image_name"]
    client_id = task["client_id"]
    input_image_path = os.path.join("images", image_name)  # Input image folder
    output_image_path = os.path.join("client_results", f"{client_id}_resized.jpg")
    resize_dimensions = task["resize_dimensions"]

    # Process the image
    process_resize(input_image_path, output_image_path, resize_dimensions)
    return {"client_id": client_id, "status": "resize processed", "output": output_image_path}

def start_resize_worker(host="127.0.0.1", port=5002):
    """
    Start a socket server for the resize worker.
    """
    print(f"[Resize Worker] Listening on {host}:{port}...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"[Resize Worker] Connection established with {addr}")
                data = b""
                while True:
                    packet = conn.recv(4096)
                    if not packet:
                        break
                    data += packet

                try:
                    task = pickle.loads(data)
                    result = handle_resize_task(task)
                    conn.sendall(pickle.dumps(result))
                    print(f"[Resize Worker] Task complete for client {result['client_id']}")
                except Exception as e:
                    print(f"[Resize Worker] Error handling task: {e}")

if __name__ == "__main__":
    start_resize_worker()
