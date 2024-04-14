from abc import ABC, abstractmethod


class DatabaseAdapter(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def add_games(self, game):
        pass

    @abstractmethod
    def get_games(self):
        pass

    @abstractmethod
    def add_players(self, game):
        pass

    @abstractmethod
    def get_players(self):
        pass

    @abstractmethod
    def add_rallies(self, rallies):
        pass

    @abstractmethod
    def get_rallies(self):
        pass


