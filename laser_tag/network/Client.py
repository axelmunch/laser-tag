import socket
from threading import Lock, Thread

from ..configuration import CLIENT_TIMEOUT, NETWORK_BUFFER_SIZE, VARIABLES, VERSION
from .safe_eval import safe_eval


class Client:
    def __init__(self, ip: str, port: int, debug=False):
        self.ip = ip
        self.port = port
        self.debug = VARIABLES.debug or debug

        self.connected = None
        self.thread = None

        self.data_to_send = []
        self.data_received = []
        self.mutex = Lock()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(CLIENT_TIMEOUT)
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
        self.send(f'"{VERSION}"')
        server_version = str(self.recv())
        if VERSION != server_version:
            if self.debug:
                print(
                    f"CLIENT bad version (Client: {VERSION} Server: {server_version})"
                )
            self.disconnect()

        while self.connected:
            self.send(self.get_data_to_send())

            data = self.recv()
            if data is None:
                self.disconnect()
                continue

        self.disconnect()

    def send(self, data):
        try:
            self.socket.send(str(data).encode("utf-8"))
        except Exception as e:
            if self.debug:
                print(f"CLIENT send {e}")

    def recv(self):
        try:
            data = self.socket.recv(NETWORK_BUFFER_SIZE).decode("utf-8")
            data = safe_eval(data, self.debug)
            self.add_received_data(data)
            return data
        except Exception as e:
            if self.debug:
                print(f"CLIENT recv {e}")
        return None

    def add_data_to_send(self, data):
        self.mutex.acquire()
        self.data_to_send.append(data)
        self.mutex.release()

    def get_data_to_send(self):
        self.mutex.acquire()
        data = self.data_to_send.copy()
        self.data_to_send.clear()
        self.mutex.release()
        return data

    def add_received_data(self, data):
        self.mutex.acquire()
        self.data_received.append(data)
        self.mutex.release()

    def get_received_data(self):
        self.mutex.acquire()
        data = self.data_received.copy()
        self.data_received.clear()
        self.mutex.release()
        return data

    def disconnect(self):
        if self.connected or self.connected is None:
            self.socket.close()
            self.connected = False
            if self.debug:
                print("CLIENT disconnected")
