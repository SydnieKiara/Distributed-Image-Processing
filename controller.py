import socket
import json
import threading

from edge_worker import handle_edge_detection_task
from grayscale_worker import handle_grayscale_task
from resize_worker import handle_resize_task

SERVER_HOST = "127.0.0.1"  # Listening on localhost
SERVER_PORT = 65432        # Same port as the client is trying to connect to

def handle_client(client_socket):
    """
    Handle incoming client requests, process tasks, and send results back.
    """
    try:
        # Receive data from the client
        data = client_socket.recv(4096)
        if data:
            tasks = json.loads(data.decode('utf-8'))
            print("Tasks received:", tasks)

            # Process tasks based on task type
            results = []
            for task in tasks["tasks"]:
                task_type = task["task_type"]
                if task_type == "resize":
                    result = handle_resize_task(task)  # Call resize worker
                elif task_type == "grayscale":
                    result = handle_grayscale_task(task)  # Call grayscale worker
                elif task_type == "edge_detect":
                    result = handle_edge_detection_task(task)  # Call edge detection worker
                else:
                    result = {"client_id": task["client_id"], "status": "unknown task type"}
                
                results.append(result)

            # Send back the results as JSON
            client_socket.sendall(json.dumps(results).encode('utf-8'))
            print("Results sent to client.")
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def start_server():
    """
    Start the server and listen for incoming client connections.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} established.")
        
        # Start a new thread to handle the client
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
