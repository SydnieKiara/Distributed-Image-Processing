from PIL import Image, ImageFilter
import os
import socket
import pickle

def process_edge(image_path, output_path):
    """Apply edge detection and save the image."""
    try:
        image = Image.open(image_path)
        edge_image = image.filter(ImageFilter.FIND_EDGES)
        edge_image.save(output_path)
        print(f"[Edge Worker] Edge image saved to {output_path}")
    except Exception as e:
        print(f"[Edge Worker] Error: {e}")

def handle_edge_task(task):
    """Handle edge detection task."""
    image_name = task["image_name"]
    client_id = task["client_id"]
    input_image_path = os.path.join("images", image_name)
    output_image_path = os.path.join("client_results", f"{client_id}_edge.jpg")

    process_edge(input_image_path, output_image_path)
    return {"client_id": client_id, "status": "edge processed", "output": output_image_path}

def start_edge_worker(host="127.0.0.1", port=5003):
    """Start the edge detection worker socket server."""
    print(f"[Edge Worker] Listening on {host}:{port}...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"[Edge Worker] Connection established with {addr}")
                data = b""
                while True:
                    packet = conn.recv(4096)
                    if not packet:
                        break
                    data += packet

                try:
                    task = pickle.loads(data)
                    result = handle_edge_task(task)
                    conn.sendall(pickle.dumps(result))
                    print(f"[Edge Worker] Task complete for client {result['client_id']}")
                except Exception as e:
                    print(f"[Edge Worker] Error handling task: {e}")

if __name__ == "__main__":
    start_edge_worker()
