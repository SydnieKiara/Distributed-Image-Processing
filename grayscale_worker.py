from PIL import Image
import os
import socket
import pickle

def process_grayscale(image_path, output_path):
    """
    Convert an image to grayscale and save it to the output path.
    """
    try:
        image = Image.open(image_path)
        grayscale_image = image.convert("L")  # Convert to grayscale (L mode)
        grayscale_image.save(output_path)
        print(f"[Grayscale Worker] Grayscale image saved to {output_path}")
    except Exception as e:
        print(f"[Grayscale Worker] Error processing grayscale image: {e}")

def handle_grayscale_task(task):
    """
    Handle grayscale task by calling the process_grayscale function.
    """
    image_name = task["image_name"]
    client_id = task["client_id"]
    input_image_path = os.path.join("images", image_name)  # Input image folder
    output_image_path = os.path.join("client_results", f"{client_id}_grayscale.jpg")

    # Process the image
    process_grayscale(input_image_path, output_image_path)
    return {"client_id": client_id, "status": "grayscale processed", "output": output_image_path}

def start_grayscale_worker(host="127.0.0.1", port=5001):
    """
    Start a socket server for the grayscale worker.
    """
    print(f"[Grayscale Worker] Listening on {host}:{port}...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"[Grayscale Worker] Connection established with {addr}")
                data = b""
                while True:
                    packet = conn.recv(4096)
                    if not packet:
                        break
                    data += packet

                try:
                    task = pickle.loads(data)
                    result = handle_grayscale_task(task)
                    conn.sendall(pickle.dumps(result))
                    print(f"[Grayscale Worker] Task complete for client {result['client_id']}")
                except Exception as e:
                    print(f"[Grayscale Worker] Error handling task: {e}")

if __name__ == "__main__":
    start_grayscale_worker()
