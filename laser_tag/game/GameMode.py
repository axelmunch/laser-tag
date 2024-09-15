from time import time

from ..configuration import VARIABLES
from ..entities.GameEntity import GameEntity
from ..entities.Player import Player
from ..language.Language import Language
from ..language.LanguageKey import LanguageKey
from .Mode import Mode, player_modes, team_modes
from .Team import Team, get_team_color, get_team_language_key


class GameMode:
    """Game mode manager"""

    def __init__(self, game_mode=Mode.SOLO):
        self.language = Language()
        self.reset(game_mode)

    def __repr__(self):
        return f"[{self.game_mode},{self.game_started},{self.game_finished},{self.grace_period_end},{self.game_time_end},{self.game_time_seconds}]"

    def set_state(self, parsed_object):
        try:
            self.game_mode = Mode(parsed_object[0])
            self.game_started = bool(parsed_object[1])
            self.game_finished = bool(parsed_object[2])
            self.grace_period_end = float(parsed_object[3])
            self.game_time_end = float(parsed_object[4])
            self.game_time_seconds = float(parsed_object[5])
        except Exception as e:
            if VARIABLES.debug:
                print("Error setting game mode state", e)

    def reset(self, game_mode):
        self.game_started = False
        self.game_finished = False
        self.game_mode = game_mode
        self.grace_period_seconds = 15
        self.grace_period_end = 0
        self.game_time_end = 0
        self.game_time_seconds = 0
        self.leaderboard = []
        self.scoreboard = []

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
            self.game_finished = False
            self.grace_period_end = time() + self.grace_period_seconds
            self.game_time_end = 0
        return self.game_started

    def is_game_started(self) -> bool:
        return self.game_started

    def update_leaderboard(self, entities: list[GameEntity]):
        self.leaderboard.clear()

        if self.game_mode in player_modes:
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
        elif self.game_mode in team_modes:
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

    def update_scoreboard(self, entities: list[GameEntity]):
        self.scoreboard.clear()

        for entity in entities.values():
            if isinstance(entity, Player):
                self.scoreboard.append(entity)

        # Sort
        try:
            if self.game_mode in player_modes:
                self.scoreboard.sort(
                    key=lambda element: element.eliminations, reverse=True
                )
            else:
                self.scoreboard.sort(key=lambda element: element.score, reverse=True)
        except ValueError:
            pass

    def get_winning_message(self) -> str:
        return f"{self.language.get(LanguageKey.GAME_END_GAME_WINNER_PLAYER) if self.game_mode in player_modes else self.language.get(LanguageKey.GAME_END_GAME_WINNER_TEAM)} {'' if len(self.leaderboard) == 0 else self.leaderboard[0][2]} {self.language.get(LanguageKey.GAME_END_GAME_WINNER_TITLE)}"

    def get_winning_color(self) -> tuple[int, int, int]:
        return get_team_color(self.leaderboard[0][1])

    def change_mode(self, mode: Mode) -> bool:
        """Returns true if mode teams have changed"""

        previous_teams = GameMode.get_teams_available(self.game_mode)

        self.reset(mode)

        return previous_teams != GameMode.get_teams_available(mode)

    def get_teams_available(mode: Mode) -> list[Team]:
        if mode in player_modes:
            return [Team.NONE]

        all_teams = list(Team)
        all_teams.remove(Team.NONE)

        match mode:
            case None:
                pass

        return all_teams

    def update(self, entities: list[GameEntity]):
        if not self.game_started or self.game_finished:
            for entity in entities.values():
                entity.can_attack = False

        # Time
        if self.grace_period_end > 0 and time() > self.grace_period_end:
            if self.game_time_end == 0 and not self.game_finished:
                self.game_time_end = time() + self.game_time_seconds
                self.grace_period_end = 0
                # End grace period (game started)
                for entity in entities.values():
                    entity.can_attack = True
        elif self.game_time_end > 0 and time() > self.game_time_end:
            # End of game
            self.game_finished = True
            self.game_time_end = 0

        # Leaderboard
        self.update_leaderboard(entities)
        # Scoreboard
        self.update_scoreboard(entities)
