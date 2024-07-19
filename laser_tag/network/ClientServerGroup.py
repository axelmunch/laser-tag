from .Client import Client
from .Server import Server


class ClientServerGroup:
    """Client and server manager"""

    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)

            cls.__instance.client = None
            cls.__instance.server = None

        return cls.__instance

    def connect_client(self, ip: str, port: int, debug=False):
        self.client = Client(ip, port, debug)

    def is_client_connected(self) -> bool:
        if self.client is None:
            return False
        return self.client.is_connected()

    def disconnect_client(self):
        self.client.disconnect()

    def get_client(self):
        return self.client

    def start_server(self, port: int, debug=False) -> int:
        self.server = Server(port, debug)
        self.server.start()
        return self.server.get_port()

    def is_server_running(self) -> bool:
        if self.server is None:
            return False
        return self.server.running

    def stop_server(self):
        if self.server is not None:
            self.server.stop()

    def get_server(self):
        return self.server
