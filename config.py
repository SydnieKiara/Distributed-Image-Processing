

CONTROLLER_HOST = "192.168.1.10"   # controller machine IP
CONTROLLER_PORT = 65432

WORKERS = {
    "grayscale": {
        "host": "192.168.1.11",    # grayscale machine IP
        "port": 5001
    },
    "resize": {
        "host": "192.168.1.12",    # resize machine IP
        "port": 5002
    },
    "edge": {
        "host": "192.168.1.13",    # edge machine IP
        "port": 5003
    }
}
