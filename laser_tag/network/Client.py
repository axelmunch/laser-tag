import socket
from sys import argv
from sys import exit as sys_exit
from threading import Thread

from ..configuration import VERSION


class Client:
    def __init__(self, ip: str, port: int, debug=False):
        self.ip = ip
        self.port = port
        self.debug = debug

        self.connected = None
        self.thread = None

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)
        try:
            self.socket.connect((self.ip, self.port))
            self.connected = True
            if self.debug:
                print(f"CLIENT connected to {(ip, port)}")
        except ConnectionRefusedError:
            if self.debug:
                print(f"CLIENT connection refused by {ip}")
        except socket.gaierror:
            if self.debug:
                print(f"CLIENT cannot resolve host {ip}")
        except TimeoutError:
            if self.debug:
                print(f"CLIENT connection timed out")

        if self.connected:
            self.thread = Thread(target=self.client)
            self.thread.start()
        else:
            self.disconnect()

    def client(self):
        # Version check
        self.send(VERSION)
        server_version = str(self.recv())
        if VERSION != server_version:
            if self.debug:
                print(
                    f"CLIENT bad version (Client: {VERSION} Server: {server_version})"
                )
            self.disconnect()

        self.data = True
        while self.data and self.connected:

            self.data = self.recv()
            print(f"Received: {self.data}")

            self.send(input("Sending: "))

        self.disconnect()

    def send(self, data):
        try:
            self.socket.send(str(data).encode("utf-8"))
        except Exception as e:
            if self.debug:
                print(f"CLIENT send {e}")

    def recv(self):
        try:
            return self.socket.recv(1024).decode("utf-8")
        except Exception as e:
            if self.debug:
                print(f"CLIENT recv {e}")
        return None

    def disconnect(self):
        if self.connected or self.connected is None:
            self.socket.close()
            self.connected = False
            if self.debug:
                print("CLIENT disconnected")


if __name__ == "__main__":
    try:
        ip = argv[1]
        port = int(argv[2])
        debug = len(argv) > 3
    except:
        print("Usage: python -m laser_tag.network.Client <ip> <port> [debug]")
        sys_exit(1)

    client = Client(ip, port, debug)
