import os

RESULTS_DIR = "client_results"

def setup_client_directories():
    """
    Create necessary directories for storing client results.
    """
    os.makedirs(RESULTS_DIR, exist_ok=True)
    print(f"Directory created or already exists: {RESULTS_DIR}")

if __name__ == "__main__":
    setup_client_directories()
