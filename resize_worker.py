from PIL import Image
import os
import socket
import pickle
from concurrent.futures import ThreadPoolExecutor
from config import WORKERS   # shared config for host/port


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
    return {
        "client_id": client_id,
        "status": "resize processed",
        "output": output_image_path
    }


def handle_connection(conn, addr):
    """
    Handle a single client connection.
    This function runs in a worker thread.
    """
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


def start_resize_worker(max_workers=4):
    """
    Start a socket server for the resize worker using the
    host and port defined in config.WORKERS['resize'].

    Uses a ThreadPoolExecutor so multiple tasks can be processed
    concurrently (multithreading).
    """
    worker_cfg = WORKERS["resize"]
    host = worker_cfg["host"]
    port = worker_cfg["port"]

    print(f"[Resize Worker] Listening on {host}:{port} with up to {max_workers} threads...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()

        # Thread pool for handling multiple client connections concurrently
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            while True:
                conn, addr = server_socket.accept()
                # Each connection is processed in a separate thread
                executor.submit(handle_connection, conn, addr)


if __name__ == "__main__":
    start_resize_worker()
