import os

def setup_directories():
    """
    Create necessary directories for the project.
    """
    directories = [
        "images",
        os.path.join("results", "grayscale"),
        os.path.join("results", "resize"),
        os.path.join("results", "edge"),
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Directory created or already exists: {directory}")

if __name__ == "__main__":
    setup_directories()
