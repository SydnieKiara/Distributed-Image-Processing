from PIL import Image, ImageFilter
import os
import socket
import pickle
from concurrent.futures import ThreadPoolExecutor
from config import WORKERS   


def process_edge_detection(image_path, output_path):
    """
    Apply edge detection to an image and save it to the output path.
    """
    try:
        image = Image.open(image_path)
        edge_image = image.filter(ImageFilter.FIND_EDGES)
        edge_image.save(output_path)
        print(f"[Edge Worker] Edge-detected image saved to {output_path}")
    except Exception as e:
        print(f"[Edge Worker] Error processing edge detection: {e}")


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
    return {
        "client_id": client_id,
        "status": "edge processed",
        "output": output_image_path
    }


def handle_connection(conn, addr):
    """
    Handle a single client connection.
    This function runs in a worker thread.
    """
    with conn:
        print(f"[Edge Worker] Connection established with {addr}")
        data = b""

        # Receive full pickled task object
        while True:
            packet = conn.recv(4096)
            if not packet:
                break
            data += packet

        try:
            task = pickle.loads(data)
            result = handle_edge_detection_task(task)

            # Send back result to controller
            conn.sendall(pickle.dumps(result))
            print(f"[Edge Worker] Task complete for client {result['client_id']}")
        except Exception as e:
            print(f"[Edge Worker] Error handling task: {e}")


def start_edge_worker(max_workers=4):
    """
    Start a socket server for the edge worker using config.WORKERS['edge'].

    Uses a ThreadPoolExecutor so multiple tasks can be processed
    concurrently (multithreading).
    """
    worker_cfg = WORKERS["edge"]
    host = worker_cfg["host"]
    port = worker_cfg["port"]

    print(f"[Edge Worker] Listening on {host}:{port} with up to {max_workers} threads...")

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
    start_edge_worker()
