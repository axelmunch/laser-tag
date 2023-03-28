import socket
from sys import argv
from sys import exit as sys_exit
from threading import Thread

from laser_tag.configuration import (
    NETWORK_BUFFER_SIZE,
    SERVER_SOCKET_TIMEOUT,
    SERVER_TIMEOUT,
    VERSION,
)
from laser_tag.network.safe_eval import safe_eval


class ClientInstance:
    def __init__(self, info, conn):
        self.info = info
        self.conn = conn

        self.thread = None

        self.data = None


class Server:
    def __init__(self, port: str, debug=False):
        self.port = port
        self.debug = debug

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(SERVER_SOCKET_TIMEOUT)
        try:
            self.socket.bind(("", self.port))
        except OSError:
            if self.debug:
                print(f"SERVER port {self.port} is already in use")
            self.socket.close()
            sys_exit(1)
        self.socket.listen()

        if self.debug:
            print(f"SERVER started on {self.socket.getsockname()}")
            print(f"SERVER IP: {socket.gethostbyname(socket.gethostname())}")

        self.max_clients = None
        self.clients = {}

        self.running = True

        while self.running:
            try:
                conn, info = self.socket.accept()

                if (
                    self.max_clients is not None
                    and len(self.clients) >= self.max_clients
                ):
                    conn.close()
                    if self.debug:
                        print(
                            f"SERVER {info} tried to connect but server is full ({len(self.clients)} client{'s' * (len(self.clients) > 1)})"
                        )
                    continue

                self.clients[info] = ClientInstance(info, conn)

                self.clients[info].thread = Thread(
                    target=self.client, args=[self.clients[info]]
                )
                self.clients[info].thread.start()

            except TimeoutError:
                continue
            except Exception as e:
                if self.debug:
                    print(f"SERVER {e}")
                self.stop()

        self.stop()

    def client(self, client: ClientInstance):
        if self.debug:
            print(
                f"SERVER {client.info} connected ({len(self.clients)} client{'s' * (len(self.clients) > 1)})"
            )

        client.conn.settimeout(SERVER_TIMEOUT)

        # Version check
        client_version = str(self.recv(client))
        self.send(client, f'"{VERSION}"')
        if VERSION != client_version:
            if self.debug:
                print(
                    f"SERVER {client.info} bad version (Server: {VERSION} Client: {client_version})"
                )
        else:
            client.data = True

        while client.data and self.running:
            client.data = self.recv(client)
            # Process data
            self.send(client, f'"{client.data}"')  # Send data back

        client.conn.close()
        del self.clients[client.info]

        if self.debug:
            print(
                f"SERVER {client.info} disconnected ({len(self.clients)} client{'s' * (len(self.clients) > 1)})"
            )

    def send(self, client: ClientInstance, data):
        try:
            client.conn.send(str(data).encode("utf-8"))
        except Exception as e:
            if self.debug:
                print(f"SERVER send {client.info} {e}")

    def recv(self, client: ClientInstance):
        try:
            data = client.conn.recv(NETWORK_BUFFER_SIZE).decode("utf-8")
            data = safe_eval(data, self.debug)
            return data
        except Exception as e:
            if self.debug:
                print(f"SERVER recv {client.info} {e}")
        return None

    def stop(self):
        if self.running:
            self.running = False

            self.socket.close()

            for client in self.clients.values():
                client.conn.close()

            if self.debug:
                print("SERVER stopped")


if __name__ == "__main__":
    port = None
    debug = None
    if len(argv) < 2:
        # Manual input of port
        while port is None:
            try:
                port = int(input("Port: "))
                if port < 0 or port > 65535:
                    port = None
                    raise ValueError
            except ValueError:
                print("Invalid port")
        debug = "n" not in input("Debug (Y/n): ").lower()
    else:
        try:
            port = int(argv[1])
            if port < 0 or port > 65535:
                raise ValueError
            debug = len(argv) > 2
        except:
            print("Usage: python -m laser_tag.network.Server <port> [debug]")
            sys_exit(1)

    server = Server(port, debug)
