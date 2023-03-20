import socket
from sys import argv


class Client:
    def __init__(self, ip, port, debug=False):
        self.ip = ip
        self.port = port
        self.debug = debug
        self.connected = None

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)
        try:
            self.socket.connect((self.ip, self.port))
            self.connected = True
            if self.debug:
                print(f"CLIENT connected to {(ip, port)}")
        except ConnectionRefusedError:
            print(f"CLIENT could not connect")

        if self.connected:
            self.send(input("Sending: "))

            self.data = True
            while self.data:

                self.data = self.recv()
                print(f"Received: {self.data}")

                self.send(input("Sending: "))

            if self.debug:
                print("CLIENT disconnected")

        self.socket.close()

        self.connected = False

    def send(self, data):
        try:
            self.socket.send(data.encode("utf-8"))
        except Exception as e:
            if self.debug:
                print(f"CLIENT {e}")

    def recv(self):
        try:
            return self.socket.recv(1024).decode("utf-8")
        except Exception as e:
            if self.debug:
                print(f"CLIENT {e}")
        return None


if __name__ == "__main__":
    try:
        ip = argv[1]
        port = int(argv[2])
    except:
        print("Usage: python -m network.Client <ip> <port> [debug]")
        exit(1)
    debug = len(argv) > 2

    client = Client(ip, port, debug)
