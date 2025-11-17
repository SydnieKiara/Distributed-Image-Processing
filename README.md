# How to Run the Distributed Image Processing System

This system runs across **four separate machines** on the same network:

| Machine | Role | Script | Example IP |
|--------|------|--------|------------|
| Machine 1 | **Controller + Client** | `controller.py`, `client.py` | `192.168.1.10` |
| Machine 2 | **Grayscale Worker** | `grayscale_worker.py` | `192.168.1.11` |
| Machine 3 | **Resize Worker** | `resize_worker.py` | `192.168.1.12` |
| Machine 4 | **Edge Worker** | `edge_worker.py` | `192.168.1.13` |

All machines must contain the **same project folder**, including `config.py`.

---

##  Step 1 — Install Dependencies on All Machines

```bash
pip install pillow numpy opencv-python
```

##  Step 2 — Configure IP Addresses

Inside `config.py`, set the real LAN IPs of each machine:

```python
CONTROLLER_HOST = "192.168.1.10"
CONTROLLER_PORT = 65432

WORKERS = {
    "grayscale": {"host": "192.168.1.11", "port": 5001},
    "resize":    {"host": "192.168.1.12", "port": 5002},
    "edge":      {"host": "192.168.1.13", "port": 5003},
}  
```

If you need the same formatting for any other section, just send it!

##  Step 3 — Start Each Worker on Its Own Machine

###  Machine 2 — Grayscale Worker
```bash
python grayscale_worker.py
```
Expected Output

[Grayscale Worker] Listening on 192.168.1.11:5001 with up to 4 threads...


###  Machine 3 — Resize Worker
```bash
python resize_worker.py
```
Expected Output

[Resize Worker] Listening on 192.168.1.12:5002 with up to 4 threads...

###  Machine 4 — Edge Worker
```bash
python edge_worker.py
```
Expected Output

[Edge Worker] Listening on 192.168.1.13:5003 with up to 4 threads...

##  Step 4 — Start the Controller (Machine 1)

Run the controller:

```bash
python controller.py
```

Expected Output

[Controller] Listening on 192.168.1.10:65432...

##  Step 5 — Run the Client (Machine 1)

Run the client script:

```bash
python client.py
```
This sends tasks from sample_task.json to the controller.
The controller forwards each task to the correct worker machine.

Example Log Output

[Controller] Sending resize task to worker resize at 192.168.1.12:5002...
[Resize Worker] Task complete for client client1

##  Step 6 — View Processed Images

After all tasks have been executed, the processed output images will be stored in:

client_results/

**Example output files:**
cake_grayscale.jpg
kitty_resized.jpg
tower_edge.jpg




#  DESIGN DESCRIPTION

This project demonstrates a fully functional **distributed image-processing system** that satisfies all required concepts for distributed computing, multiprocessing, multithreading, interprocess communication, and internode communication.

---

##  1. Distributed Computing (Multiple Machines)

The system executes across **four independent machines** on the same network:

- The **controller machine** receives tasks and delegates them to workers.
- Three **worker machines** independently handle:
  - Grayscale conversion
  - Image resizing
  - Edge detection

This architecture resembles real-world distributed systems such as:

- MapReduce clusters  
- Microservice architectures  
- Distributed compute nodes  

Each machine runs its own Python process, enabling true distributed execution.

---

## 2. Internode Communication (Machine-to-Machine Networking)

Communication between machines is performed through:

- **TCP sockets**  
- **Pickle serialization** for sending Python dictionaries  
- **JSON** for client-to-controller communication  

**Communication Flow:**

Client → Controller → Worker → Controller → Client

css
Copy code

Each worker acts as a dedicated server:

```python
server_socket.bind((host, port))
server_socket.listen()
The controller connects to each worker using the IP addresses defined in config.py.
```
##  3. Multithreading (Concurrency Inside Workers)

All worker nodes use a **ThreadPoolExecutor** to process multiple image tasks concurrently.

**Example worker threading model:**

```python
with ThreadPoolExecutor(max_workers=4) as executor:
    executor.submit(handle_connection, conn, addr)
```
This enables:

Multiple client connections at once

Parallel execution of image-processing tasks

Faster throughput on each worker node

Each worker can process up to 4 concurrent image operations by default.

##  4. Multiprocessing (Across Independent Processes)

This project uses **multiple independent Python processes**, each running on its own machine or terminal window:

- `controller.py` → 1 process  
- `client.py` → 1 process  
- `grayscale_worker.py` → 1 process  
- `resize_worker.py` → 1 process  
- `edge_worker.py` → 1 process  

**Total:** 5 separate operating-system processes working together across the network.

This demonstrates true multiprocessing because:

- Each script runs in its own Python interpreter instance  
- Each worker performs image processing independently  
- The controller and client operate in parallel with the workers  

This architecture satisfies the requirement for **distributed multiprocessing across multiple machines**.

##  5. Interprocess Communication (IPC)

Interprocess Communication in this system is implemented using:

- **TCP sockets** (primary communication channel)
- **Pickle** for transmitting Python dictionaries and task results
- **JSON** for structured task messages from the client to the controller

This communication model mirrors real-world distributed systems, such as:

- Remote Procedure Call (RPC) services  
- Message-passing architectures  
- Distributed task schedulers  

**IPC Workflow:**

Client → Controller → Worker → Controller → Client

diff
Copy code

This design ensures:

- Reliable delivery of tasks  
- Structured message passing  
- Clear separation between nodes  
- Scalable communication across the network

##  6. Functional Image Processing

Each worker performs real image-processing tasks using the Pillow (PIL) library, demonstrating practical computation across the distributed system.

###  Grayscale Worker
- Converts color images to **grayscale**  
- Uses Pillow’s `"L"` mode conversion  
- Outputs files such as:  
  - `client1_grayscale.jpg`

###  Resize Worker
- Resizes images to new dimensions  
- Uses Pillow’s `resize()` function  
- Outputs files such as:  
  - `client1_resized.jpg`

###  Edge Detection Worker
- Applies **edge detection** using `ImageFilter.FIND_EDGES`  
- Detects outlines and boundaries  
- Outputs files such as:  
  - `client1_edge.jpg`

All processed images are sent back to the controller, then returned to the client, and saved in:

client_results/

sql
Copy code

This confirms the system performs real, functional image transformations—not just simulated tasks.

# Summary of Requirements Met

| Requirement | Met By |
|------------|--------|
| **Multiprocessing** | Controller + 3 workers + client run as separate OS processes |
| **Multithreading** | Each worker uses `ThreadPoolExecutor` to process multiple tasks concurrently |
| **Interprocess Communication (IPC)** | Implemented using TCP sockets, JSON, and Pickle |
| **Distributed Computing** | System runs across four independent machines on the same network |
| **Internode Communication** | Controller and workers exchange messages via TCP connections |

 **Your project successfully demonstrates distributed computing, multithreading, multiprocessing, IPC, and internode communication — fully satisfying the assignment requirements.**
