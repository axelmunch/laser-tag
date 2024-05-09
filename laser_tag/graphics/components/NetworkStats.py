from time import time

from ...configuration import DEFAULT_FONT
from ...language.LanguageKey import LanguageKey
from ..resize import resize
from ..Text import Text
from .Component import Component


class NetworkStats(Component):
    """Network stats component"""

    def __init__(
        self,
        data={"pings": [], "connected": False, "bytes_sent": [], "bytes_received": []},
    ):
        super().__init__()

        self.text = Text(
            DEFAULT_FONT["font"],
            DEFAULT_FONT["font_is_file"],
            DEFAULT_FONT["size_multiplier"],
        )

        self.set_original_size(250, 400)

        self.precision = 100
        self.pings = []
        self.bytes_sent = []
        self.bytes_received = []
        self.average_send_per_tick = []
        self.total_sent = 0
        self.send_per_second = 0
        self.next_second = time() + 1

        self.update(
            data["pings"], data["connected"], data["bytes_sent"], data["bytes_received"]
        )

    def update(
        self,
        pings: list[float],
        connected: bool,
        bytes_sent: list[int],
        bytes_received: list[int],
    ):
        """
        Update the component

        Parameters:
            pings (list): Pings in seconds the last game tick
            connected (bool): The client is connected to the server
            bytes_sent (list): Bytes sent the last game tick
            bytes_received (list): Bytes received the last game tick
        """
        self.pings += pings
        self.bytes_sent += bytes_sent
        self.bytes_received += bytes_received
        self.average_send_per_tick.append(len(bytes_sent))

        self.total_sent += len(bytes_sent)
        if time() > self.next_second:
            self.send_per_second = self.total_sent
            self.total_sent = 0
            self.next_second = time() + 1

        self.pings = self.pings[-self.precision :]
        self.bytes_sent = self.bytes_sent[-self.precision :]
        self.bytes_received = self.bytes_received[-self.precision :]
        self.average_send_per_tick = self.average_send_per_tick[-self.precision :]

        self.data = {
            "pings": self.pings,
            "connected": connected,
            "bytes_sent": self.bytes_sent,
            "bytes_received": self.bytes_received,
            "average_send_per_tick": self.average_send_per_tick,
            "send_per_second": self.send_per_second,
        }
        super().update()

    def render(self):
        self.surface.fill((0, 0, 0, 0))

        connection_text = (
            self.language.get(LanguageKey.NETWORK_STATS_CONNECTED)
            if self.data["connected"]
            else (
                self.language.get(LanguageKey.NETWORK_STATS_DISCONNECTED)
                if self.data["connected"] is not None
                else self.language.get(LanguageKey.NETWORK_STATS_CONNECTING)
            )
        )
        self.surface.blit(
            self.text.get_surface(
                connection_text,
                30,
                (255, 255, 255),
            ),
            (resize(0, "x"), resize(0, "y")),
        )

        self.surface.blit(
            self.text.get_surface(
                f"{self.language.get(LanguageKey.NETWORK_STATS_PING)} {round((sum(self.data['pings']) / max(1, len(self.data['pings'])) * 1000), 2)}ms",
                30,
                (255, 255, 255),
            ),
            (resize(0, "x"), resize(50, "y")),
        )

        self.surface.blit(
            self.text.get_surface(
                f"{self.language.get(LanguageKey.NETWORK_STATS_AVG_SEND_TICK)} {round((sum(self.data['average_send_per_tick']) / max(1, len(self.data['average_send_per_tick']))), 2)}",
                30,
                (255, 255, 255),
            ),
            (resize(0, "x"), resize(100, "y")),
        )

        self.surface.blit(
            self.text.get_surface(
                f"{self.language.get(LanguageKey.NETWORK_STATS_SEND_SECOND)} {self.data['send_per_second']}",
                30,
                (255, 255, 255),
            ),
            (resize(0, "x"), resize(150, "y")),
        )

        self.surface.blit(
            self.text.get_surface(
                f"{self.language.get(LanguageKey.NETWORK_STATS_AVG_SEND)} {round(sum(self.data['bytes_sent']) / max(1, len(self.data['bytes_sent']))/1000, 2)}kbits",
                30,
                (255, 255, 255),
            ),
            (resize(0, "x"), resize(200, "y")),
        )

        self.surface.blit(
            self.text.get_surface(
                f"{self.language.get(LanguageKey.NETWORK_STATS_MAX_SEND)} {round(0 if len(self.data['bytes_sent']) == 0 else max(self.data['bytes_sent']) / 1000, 2)}kbits",
                30,
                (255, 255, 255),
            ),
            (resize(0, "x"), resize(250, "y")),
        )

        self.surface.blit(
            self.text.get_surface(
                f"{self.language.get(LanguageKey.NETWORK_STATS_AVG_RECV)} {round(sum(self.data['bytes_received']) / max(1, len(self.data['bytes_received']))/1000, 2)}kbits",
                30,
                (255, 255, 255),
            ),
            (resize(0, "x"), resize(300, "y")),
        )

        self.surface.blit(
            self.text.get_surface(
                f"{self.language.get(LanguageKey.NETWORK_STATS_MAX_RECV)} {round(0 if len(self.data['bytes_received']) == 0 else max(self.data['bytes_received']) / 1000, 2)}kbits",
                30,
                (255, 255, 255),
            ),
            (resize(0, "x"), resize(350, "y")),
        )

        super().render()
