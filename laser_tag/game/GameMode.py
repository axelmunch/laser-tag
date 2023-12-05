from time import time

from ..configuration import VARIABLES
from ..entities.GameEntity import GameEntity
from ..entities.Player import Player
from .Mode import Mode


class GameMode:
    """Game mode manager"""

    def __init__(self, game_mode=Mode.SOLO):
        self.reset(game_mode)

    def __repr__(self):
        return f"[{self.game_mode}, {self.game_started}, {self.grace_period_end}, {self.game_time_end}, {self.game_time_seconds}]"

    def set_state(self, parsed_object):
        try:
            self.game_mode = Mode(parsed_object[0])
            self.game_started = bool(parsed_object[1])
            self.grace_period_end = float(parsed_object[2])
            self.game_time_end = float(parsed_object[3])
            self.game_time_seconds = float(parsed_object[4])
        except Exception as e:
            if VARIABLES.debug:
                print("Error setting game mode state", e)

    def reset(self, game_mode):
        self.game_started = False
        self.game_mode = game_mode
        self.grace_period_seconds = 20
        self.grace_period_end = 0
        self.game_time_end = 0
        self.game_time_seconds = 0
        self.leaderboard = []

        match game_mode:
            case Mode.SOLO:
                self.grace_period_seconds = 3
                self.game_time_seconds = 5
            case Mode.SOLO_ELIMINATION:
                self.grace_period_seconds = 3
                self.game_time_seconds = 10 * 60
            case Mode.TEAM:
                self.grace_period_seconds = 3
                self.game_time_seconds = 10 * 60
            case Mode.TEAM_ELIMINATION:
                self.grace_period_seconds = 3
                self.game_time_seconds = 10 * 60

    def start(self) -> bool:
        if not self.game_started:
            self.game_started = True
            self.grace_period_end = time() + self.grace_period_seconds
            self.game_time_end = 0
        return self.game_started

    def update_leaderboard(self, entities: list[GameEntity]):
        self.leaderboard.clear()

        if self.game_mode in [Mode.SOLO, Mode.SOLO_ELIMINATION]:
            for entity in entities.values():
                if isinstance(entity, Player):
                    if self.game_mode == Mode.SOLO:
                        self.leaderboard.append(
                            [int(entity.score), entity.team, "Name"]
                        )
                    else:
                        self.leaderboard.append(
                            [entity.eliminations, entity.team, "Name"]
                        )
        elif self.game_mode in [Mode.TEAM, Mode.TEAM_ELIMINATION]:
            teams = {}
            for entity in entities.values():
                if isinstance(entity, Player):
                    if self.game_mode == Mode.TEAM:
                        teams[entity.team] = teams.get(entity.team, 0) + entity.score
                    else:
                        teams[entity.team] = (
                            teams.get(entity.team, 0) + entity.eliminations
                        )

            for team, score in teams.items():
                self.leaderboard.append([int(score), team, team])

        # Sort
        self.leaderboard.sort(key=lambda element: element[0], reverse=True)

    def update(self, entities: list[GameEntity]):
        if not self.game_started:
            for entity in entities.values():
                entity.can_attack = False
            return

        # Time
        if self.grace_period_end > 0 and time() > self.grace_period_end:
            if self.game_time_end == 0:
                self.game_time_end = time() + self.game_time_seconds
                self.grace_period_end = 0
                # End grace period (game started)
                for entity in entities.values():
                    entity.can_attack = True
        elif self.game_time_end > 0 and time() > self.game_time_end:
            self.game_started = False
            self.game_time_end = 0
            # End of game

        # Leaderboard
        self.update_leaderboard(entities)
