import socket
import json
import threading
import pickle

from config import CONTROLLER_HOST, CONTROLLER_PORT, WORKERS

def send_task_to_worker(task_type, task):
    """
    Send a single task to the appropriate remote worker node
    and return the result.

    task_type: 'resize', 'grayscale', or 'edge_detect'
    task: dict with fields like 'image_name', 'client_id', etc.
    """
    # Map task_type from JSON to WORKERS key
    if task_type == "resize":
        worker_key = "resize"
    elif task_type == "grayscale":
        worker_key = "grayscale"
    elif task_type == "edge_detect":
        worker_key = "edge"
    else:
        # Unknown type - just return a failure status
        return {
            "client_id": task.get("client_id", "unknown"),
            "status": f"unknown task type: {task_type}"
        }

    worker_cfg = WORKERS[worker_key]
    host = worker_cfg["host"]
    port = worker_cfg["port"]

    print(f"[Controller] Sending {task_type} task to worker {worker_key} at {host}:{port}...")

    # Open a TCP connection to the worker and send the task via pickle
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(pickle.dumps(task))

        # Receive the full pickled result
        data = b""
        while True:
            packet = s.recv(4096)
            if not packet:
                break
            data += packet

    try:
        result = pickle.loads(data)
    except Exception as e:
        print(f"[Controller] Error decoding worker response: {e}")
        result = {
            "client_id": task.get("client_id", "unknown"),
            "status": "worker response error"
        }

    print(f"[Controller] Worker response: {result}")
    return result


def handle_client(client_socket):
    """
    Handle incoming client requests, forward tasks to workers,
    and send results back to the client.
    """
    try:
        data = client_socket.recv(4096)
        if not data:
            return

        # Client sends JSON
        tasks = json.loads(data.decode("utf-8"))
        print("[Controller] Tasks received from client:", tasks)

        results = []
        for task in tasks.get("tasks", []):
            task_type = task.get("task_type")
            # Delegate to remote worker instead of calling local functions
            result = send_task_to_worker(task_type, task)
            results.append(result)

        # Send all results back to the client as JSON
        client_socket.sendall(json.dumps(results).encode("utf-8"))
        print("[Controller] Results sent back to client.")

    except Exception as e:
        print(f"[Controller] Error handling client: {e}")
    finally:
        client_socket.close()


def start_server():
    """
    Start the controller server and listen for incoming client connections.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((CONTROLLER_HOST, CONTROLLER_PORT))
    server_socket.listen(5)
    print(f"[Controller] Listening on {CONTROLLER_HOST}:{CONTROLLER_PORT}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[Controller] Connection from {addr} established.")

        # Handle each client in a separate thread
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()


if __name__ == "__main__":
    start_server()
