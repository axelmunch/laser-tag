from time import time

from ..configuration import VARIABLES
from ..entities.GameEntity import GameEntity
from ..entities.Player import Player
from ..language.Language import Language
from .Mode import Mode
from .Team import Team, get_team_language_key


class GameMode:
    """Game mode manager"""

    def __init__(self, game_mode=Mode.SOLO):
        self.language = Language()
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
        self.grace_period_seconds = 15
        self.grace_period_end = 0
        self.game_time_end = 0
        self.game_time_seconds = 0
        self.leaderboard = []

        match self.game_mode:
            case Mode.SOLO:
                self.game_time_seconds = 10 * 60
            case Mode.SOLO_ELIMINATION:
                self.game_time_seconds = 10 * 60
            case Mode.TEAM:
                self.game_time_seconds = 10 * 60
            case Mode.TEAM_ELIMINATION:
                self.game_time_seconds = 10 * 60

    def start(self) -> bool:
        if not self.game_started:
            self.game_started = True
            self.grace_period_end = time() + self.grace_period_seconds
            self.game_time_end = 0
        return self.game_started

    def is_game_started(self) -> bool:
        return self.game_started

    def update_leaderboard(self, entities: list[GameEntity]):
        self.leaderboard.clear()

        if self.game_mode in [Mode.SOLO, Mode.SOLO_ELIMINATION]:
            for entity in entities.values():
                if isinstance(entity, Player):
                    if self.game_mode == Mode.SOLO:
                        self.leaderboard.append(
                            [int(entity.score), entity.team, entity.name]
                        )
                    else:
                        self.leaderboard.append(
                            [entity.eliminations, entity.team, entity.name]
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
                self.leaderboard.append(
                    [int(score), team, self.language.get(get_team_language_key(team))]
                )

        # Sort
        try:
            self.leaderboard.sort(key=lambda element: element[0], reverse=True)
        except ValueError:
            pass

    def change_mode(self, mode: Mode) -> bool:
        """Returns true if mode teams have changed"""

        previous_teams = GameMode.get_teams_available(self.game_mode)

        self.reset(mode)

        return previous_teams != GameMode.get_teams_available(mode)

    def get_teams_available(mode: Mode) -> list[Team]:
        all_teams = list(Team)
        all_teams.remove(Team.NONE)

        match mode:
            case Mode.SOLO:
                return [Team.NONE]
            case Mode.SOLO_ELIMINATION:
                return [Team.NONE]
            case Mode.TEAM:
                return all_teams
            case Mode.TEAM_ELIMINATION:
                return all_teams

        return all_teams

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
            # End of game
            self.game_started = False
            self.game_time_end = 0

        # Leaderboard
        self.update_leaderboard(entities)
