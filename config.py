

CONTROLLER_HOST = "172.20.208.110"   # controller machine IP
CONTROLLER_PORT = 65432

WORKERS = {
    "grayscale": {
        "host": "172.20.208.138",    # grayscale machine IP
        "port": 5001
    },
    "resize": {
        "host": "172.20.210.183",    # resize machine IP
        "port": 5002
    },
    "edge": {
        "host": "172.20.208.157",    # edge machine IP
        "port": 5003
    }
}
