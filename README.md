#  Distributed Image Processing — Run Instructions

##  Project Overview
This project demonstrates **distributed computing concepts** in Python, where different “worker” nodes handle image-processing tasks such as **grayscale**, **resize**, and **edge detection** through **socket-based communication**.

It showcases:
-  **Multiprocessing**
-  **Multithreading**
-  **Interprocess Communication (IPC)**
-  **Distributed Computing**
-  **Internode Communication**

---

##  Requirements

### 1. Install Python
Make sure you have **Python 3.10 or newer** installed:

```bash
python --version
```

### 2. Install Required Libraries

Install all required dependencies before running the project.  
Open your terminal in the project folder and run the following command:

```bash
pip install pillow numpy opencv-python
```

##  How to Run the Program

###  Step 1: Open the Project in VS Code

Open the folder directly (the one containing **`controller.py`**, not any parent folder).

Open a terminal inside VS Code by pressing **Ctrl + `**.

Your prompt should look something like:
PS C:\Users\YourName\Downloads\Distributed-Image-Processing>


---

###  Step 2: Prepare the Folders

Run the setup scripts (only once or whenever you reset your environment):

```bash
python extra/setup_directories.py
python extra/setup_client_directories.py
```
###  Step 3: Validate the Task File

Run the following command to ensure that your `sample_task.json` file is valid and that all referenced images exist:

```bash
python extra/validate_task_file.py
```
###  Step 4: Start Worker Nodes

Open **three terminals** (or PowerShell windows).  
Each one runs a separate “node” that handles a specific image-processing operation.

---

####  Terminal 1 — Grayscale Worker
Run the following command:

```bash
python grayscale_worker.py
```
####  Terminal 2 — Resize Worker

Run the following command:

```bash
python resize_worker.py
```
####  Terminal 3 — Edge Worker

Run the following command:

```bash
python edge_worker.py
```

###  Start the Controller (Master Node)

In a **fourth terminal**, run the following command:

```bash
python controller.py
```
###  Step 6: Run the Client to Send Tasks

In a **fifth terminal**, run the following command:

```bash
python client.py
```
The client reads **`sample_task.json`**, sends each image operation to the **controller**, and the controller delegates them to the correct **worker node**.

**You’ll see logs like:**
[Controller] Sending resize task to Worker 5002
[Resize Worker] Connection established with ('127.0.0.1', 51245)
[Resize Worker] Resized image saved to client_results/client1_resized.jpg

###  Step 7: Check the Results

When the tasks finish, check your output folder:

client_results/

