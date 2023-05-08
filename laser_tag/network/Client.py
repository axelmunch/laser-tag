import socket
from threading import Lock, Thread
from time import sleep

from ..configuration import (
    CLIENT_MINIMUM_TICK,
    CLIENT_TIMEOUT,
    NETWORK_BUFFER_SIZE,
    VARIABLES,
    VERSION,
)
from ..events.EventInstance import EventInstance
from ..utils.Timer import Timer
from .safe_eval import safe_eval


class Client:
    def __init__(self, ip: str, port: int, debug=False):
        self.ip = ip
        self.port = port
        self.debug = VARIABLES.debug or debug

        self.connected = None
        self.thread = None

        self.events_to_send: list[EventInstance] = []
        self.data_received = []
        self.mutex = Lock()

        self.bytes_sent = []
        self.bytes_received = []
        self.pings = []
        self.network_stats_mutex = Lock()

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
        server_version = str(self.recv()[0])
        if VERSION != server_version:
            if self.debug:
                print(
                    f"CLIENT bad version (Client: {VERSION} Server: {server_version})"
                )
            self.disconnect()

        ping_timer = Timer()
        while self.connected:
            ping_timer.start()
            bytes_sent = self.send(self.get_events_to_send())
            if VARIABLES.fps > 0:
                sleep(1 / max(CLIENT_MINIMUM_TICK, VARIABLES.fps))

            data, bytes_received = self.recv()
            ping_timer.stop()
            if data is None:
                self.disconnect()
                continue
            else:
                self.add_received_data(data)

            self.set_network_stats(ping_timer.get_time(), bytes_sent, bytes_received)

        self.disconnect()

    def send(self, data):
        encoded_data = str(data).encode("utf-8")
        bytes_sent = len(encoded_data)
        try:
            self.socket.send(encoded_data)
        except Exception as e:
            if self.debug:
                print(f"CLIENT send {e}")
        return bytes_sent

    def recv(self):
        try:
            data = self.socket.recv(NETWORK_BUFFER_SIZE)
            bytes_received = len(data)
            data = safe_eval(data.decode("utf-8"), self.debug)
            return data, bytes_received
        except Exception as e:
            if self.debug:
                print(f"CLIENT recv {e}")
        return None, 0

    def add_events_to_send(self, events: list[EventInstance]):
        self.mutex.acquire()
        self.events_to_send += events
        self.mutex.release()

    def get_events_to_send(self) -> list[EventInstance]:
        self.mutex.acquire()
        events = self.events_to_send.copy()
        self.events_to_send.clear()
        self.mutex.release()
        return events

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

    def set_network_stats(self, ping, bytes_sent, bytes_received):
        self.network_stats_mutex.acquire()
        self.pings.append(ping)
        self.bytes_sent.append(bytes_sent)
        self.bytes_received.append(bytes_received)
        self.network_stats_mutex.release()

    def get_network_stats(self):
        self.network_stats_mutex.acquire()
        pings = self.pings.copy()
        bytes_sent = self.bytes_sent.copy()
        bytes_received = self.bytes_received.copy()
        self.pings.clear()
        self.bytes_sent.clear()
        self.bytes_received.clear()
        self.network_stats_mutex.release()
        return pings, self.connected, bytes_sent, bytes_received

    def is_connected(self):
        return self.connected

    def disconnect(self):
        if self.connected or self.connected is None:
            self.socket.close()
            self.connected = False
            if self.debug:
                print("CLIENT disconnected")
