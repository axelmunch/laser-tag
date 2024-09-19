import socket
from sys import argv
from sys import exit as sys_exit
from threading import Thread

from laser_tag.configuration import (
    MAX_PLAYER_NAME_LENGTH,
    NETWORK_BUFFER_SIZE,
    SERVER_DEFAULT_MAX_CLIENTS,
    SERVER_DELTA_TIME_NAME,
    SERVER_SOCKET_TIMEOUT,
    SERVER_TIMEOUT,
    VERSION,
)
from laser_tag.entities.Player import Player
from laser_tag.events.Event import Event
from laser_tag.events.EventInstance import EventInstance
from laser_tag.game.Game import Game
from laser_tag.math.Point import Point
from laser_tag.network.safe_eval import safe_eval
from laser_tag.utils.DeltaTime import DeltaTime


class ClientInstance:
    def __init__(self, info, conn):
        self.info = info
        self.conn = conn

        self.thread = None

        self.player_name = ""

        self.data = None

        self.controlled_entity_id = None


class Server:
    def __init__(self, port: int, debug=False):
        self.port = port
        self.debug = debug

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(SERVER_SOCKET_TIMEOUT)
        try:
            self.socket.bind(("", self.port))
            self.port = self.socket.getsockname()[1]
        except OSError:
            if self.debug:
                print(f"SERVER port {self.port} is already in use")
            self.socket.close()
            self.running = False
            return
        self.socket.listen()

        if self.debug:
            print(f"SERVER bound to {self.socket.getsockname()}")
            print(f"SERVER IP: {socket.gethostbyname(socket.gethostname())}")

        self.max_clients = SERVER_DEFAULT_MAX_CLIENTS
        self.clients = {}

        self.game = Game(server_mode=True)

        self.server_delta_time = DeltaTime(SERVER_DELTA_TIME_NAME)

        self.running = None

        self.running_thread = Thread(target=self.run)

    def start(self):
        if self.running is None:
            self.running = True
            self.running_thread.start()
        elif not self.running:
            if self.debug:
                print("SERVER was not started")
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

        # Get player name
        client.player_name = self.recv(client)
        if not (
            client.player_name is not None
            and isinstance(client.player_name, str)
            and len(client.player_name) >= 1
        ):
            client.player_name = "Player"
        client.player_name = client.player_name[:MAX_PLAYER_NAME_LENGTH]
        self.send(client, f'"{client.player_name}"')

        # Create player
        player = Player(Point(0, 0))
        client.controlled_entity_id = self.game.world.spawn_entity(player)
        spawn_point = self.game.world.map.get_spawn_point(client.controlled_entity_id)
        player.move(spawn_point.x, spawn_point.y)
        self.game.world.get_entity(client.controlled_entity_id).set_name(
            client.player_name
        )

        client_delta_time = DeltaTime(client.info)

        self.game.update(
            [EventInstance(Event.PLAYER_JOIN, client.controlled_entity_id)],
            controlled_entity_id=client.controlled_entity_id,
            delta_time=self.server_delta_time,
            player_delta_time=client_delta_time,
        )

        while client.data is not None and self.running:
            client.data = self.parse_events(self.recv(client))

            if client.data is not None:
                # Process data
                self.game.update(
                    client.data,
                    controlled_entity_id=client.controlled_entity_id,
                    delta_time=self.server_delta_time,
                    player_delta_time=client_delta_time,
                )

            # Send data
            self.send(client, self.get_state(client))

        # Disconnect client
        self.game.update(
            [EventInstance(Event.PLAYER_LEAVE, client.controlled_entity_id)],
            controlled_entity_id=client.controlled_entity_id,
            delta_time=self.server_delta_time,
            player_delta_time=client_delta_time,
        )
        client.conn.close()
        del self.clients[client.info]
        self.game.world.remove_entity(client.controlled_entity_id)

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

    def get_state(self, client: ClientInstance):
        return {"game": self.game, "controlled_entity_id": client.controlled_entity_id}

    def parse_events(self, data):
        if not isinstance(data, list):
            return None

        events = []
        for event in data:
            created_event = EventInstance.create(event)
            if created_event is not None and not created_event.local:
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
    non_interactive = False
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
            non_interactive = len(argv) > 3
        except:
            print(f"Usage: {argv[0]} [port] [debug] [non-interactive]")
            sys_exit(1)

    server = Server(port, debug)
    server.start()

    if not non_interactive:
        try:
            while (
                "exit"
                not in input(
                    'Enter "exit" or press Ctrl+C to stop the server\n'
                ).lower()
            ):
                continue

        except KeyboardInterrupt:
            if debug:
                print()
        server.stop()

    else:
        server.running_thread.join()
