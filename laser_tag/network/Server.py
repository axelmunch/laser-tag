import socket
from sys import argv
from sys import exit as sys_exit
from threading import Thread

from laser_tag.configuration import (
    DEFAULT_MAX_CLIENTS,
    NETWORK_BUFFER_SIZE,
    SERVER_SOCKET_TIMEOUT,
    SERVER_TIMEOUT,
    VARIABLES,
    VERSION,
)
from laser_tag.entities.Player import Player
from laser_tag.events.EventInstance import EventInstance
from laser_tag.game.Game import Game
from laser_tag.network.safe_eval import safe_eval
from laser_tag.utils.DeltaTime import DeltaTime


class ClientInstance:
    def __init__(self, info, conn):
        self.info = info
        self.conn = conn

        self.thread = None

        self.data = None

        self.controlled_entity_id = None


class Server:
    def __init__(self, port: int, debug=False):
        self.port = port
        self.debug = VARIABLES.debug or debug

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(SERVER_SOCKET_TIMEOUT)
        try:
            self.socket.bind(("", self.port))
            self.port = self.socket.getsockname()[1]
        except OSError:
            if self.debug:
                print(f"SERVER port {self.port} is already in use")
            self.socket.close()
            sys_exit(1)
        self.socket.listen()

        if self.debug:
            print(f"SERVER bound to {self.socket.getsockname()}")
            print(f"SERVER IP: {socket.gethostbyname(socket.gethostname())}")

        self.max_clients = DEFAULT_MAX_CLIENTS
        self.clients = {}

        self.game = Game()

        self.running = None

        self.running_thread = Thread(target=self.run)

    def start(self):
        if self.running is None:
            self.running = True
            self.running_thread.start()
        else:
            if self.debug:
                print("SERVER has already been started")

    def run(self):
        if self.debug and self.running:
            print("SERVER started")
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

        # Create player
        client.controlled_entity_id = self.game.world.spawn_entity(Player(4, 4, 0))

        delta_time = DeltaTime(client.info)

        while client.data is not None and self.running:
            client.data = self.parse_events(self.recv(client))

            delta_time.update()

            if client.data is not None:
                # Process data
                self.game.update(
                    client.data,
                    controlled_entity_id=client.controlled_entity_id,
                    delta_time=delta_time,
                )

            # Send data
            self.send(client, self.get_state(client))

        # Disconnect client
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

    def set_max_clients(self, max_clients: int):
        self.max_clients = max_clients

    def get_state(self, client: ClientInstance) -> list:
        state = {}

        state["game"] = self.game
        state["controlled_entity_id"] = client.controlled_entity_id

        return state

    def parse_events(self, data):
        if not isinstance(data, list):
            return None

        events = []
        for event in data:
            created_event = EventInstance.create(event)
            if created_event is not None:
                events.append(created_event)

        return events

    def stop(self):
        if self.running:
            if self.debug:
                print("SERVER stopping...")

            self.running = False

            self.socket.close()

            for client in self.clients.copy().values():
                client.conn.close()

    def get_port(self):
        return self.port


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
    server.start()
    try:
        while (
            "exit"
            not in input('Enter "exit" or press Ctrl+C to stop the server\n').lower()
        ):
            continue

    except KeyboardInterrupt:
        if debug:
            print()
    server.stop()
