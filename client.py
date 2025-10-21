import socket
import json
import os

TASK_FILE = "sample_task.json"
RESULTS_DIR = "client_results"
SERVER_HOST = "127.0.0.1"  # Replace with controller's IP
SERVER_PORT = 65432        # Port to connect to controller

def load_tasks(task_file):
    """
    Load tasks from a JSON file.
    """
    if not os.path.exists(task_file):
        print(f"Task file '{task_file}' not found.")
        return None

    with open(task_file, "r") as file:
        tasks = json.load(file)
    return tasks

def save_result(client_id, result_data):
    """
    Save result data to the client_results directory.
    """
    file_name = os.path.join(RESULTS_DIR, f"{client_id}_result.json")
    with open(file_name, "w") as file:
        json.dump(result_data, file, indent=4)
    print(f"Results saved for client {client_id}: {file_name}")

def main():
    """
    Main client function to send tasks to the controller and receive results.
    """
    # Load tasks
    tasks = load_tasks(TASK_FILE)
    if not tasks:
        return

    # Connect to the controller
    try:
        print(f"Connecting to server at {SERVER_HOST}:{SERVER_PORT}...")
        with socket.create_connection((SERVER_HOST, SERVER_PORT)) as client_socket:
            print("Connected to the server.")

            # Send tasks to the controller
            task_data = json.dumps(tasks).encode('utf-8')
            client_socket.sendall(task_data)
            print("Tasks sent to the controller.")

            # Receive results from the controller
            received_data = client_socket.recv(4096)  # Adjust buffer size as needed
            results = json.loads(received_data.decode('utf-8'))
            print("Results received from the controller.")

            # Save results
            for result in results:
                save_result(result["client_id"], result)

    except ConnectionError as e:
        print(f"Error connecting to the server: {e}")

if __name__ == "__main__":
    main()
