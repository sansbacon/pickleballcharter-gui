import json
import logging
import logging.handlers
import sys

from PySide6.QtWidgets import QTabWidget, QMainWindow, QApplication, QMessageBox

from config import user_data_dir, user_data_file
from pbcgui.data import database_factory, Game, Rally, Score, Shot, ShotTypes
from pbcgui.palettes import AppPalette
from pbcgui.utility import StructuredMessage, next_score
from pbcgui.widgets import *

m = StructuredMessage


class TouchscreenApp(QMainWindow):
    """Main class for charting app"""

    log_shot = Signal(Shot)
    log_rally = Signal(Rally)

    def __init__(self):
        super().__init__()   
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())
        self._initProperties()
        self._initUI()
        self._initSlots()

    def _create_widgets(self):
        """Create the widgets for the application"""
        self.charting_widgets = {
            "player": PlayerSectionWidget(),
            "score": ScoreSectionWidget(),
            "stack": StackSectionWidget(),
            "side": ShotSideWidget(),
            "location": ShotLocationWidget(),
            "outcome": ShotOutcomeWidget(),
            "shots": ChartingShotsWidget(shot_types=ShotTypes),
            "winner": RallyWinnerWidget(),
            "log": RallyLogWidget()
        }

        self.charting_widgets['sidebar'] =  ChartingSidebarWidget(
            self.charting_widgets['player'], self.charting_widgets['score'], self.charting_widgets['stack']
        )

        self.charting_widgets['main'] = ChartingMainWidget(
                self.charting_widgets['shots'], 
                [self.charting_widgets['side'], self.charting_widgets['location'], 
                 self.charting_widgets['outcome'], self.charting_widgets['winner']]
        )

        self.charting_widgets['tab'] = ChartTabWidget(self.charting_widgets['sidebar'], self.charting_widgets['main'], self.charting_widgets['log'])

    def _initProperties(self):
        """Initialize the properties of the application"""
        self.current_game = Game()
        self.current_players = []
        self.current_score = Score(*[0, 0, 2, 0])
        self.current_rally = Rally(rally_score=self.current_score)
        self.current_shot = Shot()
        self.db = database_factory(db_type='tinydb', db_path=user_data_dir / user_data_file)
        self.existing_players = self.db.get_players()
        self.games = []

    def _initSlots(self):
        """Initialize the slots for the application"""
        self.setup_game_widget.add_player_dialog.player_added.connect(self.add_player_to_db)
        self._game_over_slots()       
        self._new_game_slots()
        self._rally_over_slots()
        self._shot_over_slots()
        self._shot_slots()
        
    def _initUI(self):
        """Initialize the user interface"""
        self._create_widgets()
        self.setPalette(AppPalette())
        menu_bar = AppMenuBar(self)
        self.setMenuBar(menu_bar)

        # Create a tab widget
        self.tab_widget = QTabWidget()

        # Initialize the first tab
        self.setup_game_widget = SetupGameWidget(players=self.existing_players)
        self.setup_game_widget.new_game_button.clicked.connect(self.create_new_game)
        self.tab_widget.addTab(self.setup_game_widget, "Setup Game")
        
        # Initialize the second tab
        self.tab_widget.addTab(self.charting_widgets['tab'], "Chart Game")

        # Set the tab widget as the central widget
        self.setCentralWidget(self.tab_widget)

    def _game_over_slots(self):
        """Connect signals for when the game is over"""
        pass

    def _new_game_slots(self):
        """Connect signals for when a new game is requested"""
        self.setup_game_widget.newGameRequested.connect(self.add_current_players)
        self.setup_game_widget.newGameRequested.connect(self.charting_widgets['player'].update_buttons)
        self.setup_game_widget.newGameRequested.connect(self.charting_widgets['stack'].update_buttons)
        self.setup_game_widget.newGameRequested.connect(self.switch_to_charting)

    def _rally_over_slots(self):
        """Connect signals for when the rally is over"""
        self.charting_widgets['winner'].rally_over.connect(self.add_rally_outcome)
        self.log_rally.connect(self.charting_widgets['log'].add_entity)
        self.charting_widgets['winner'].rally_over.connect(self.update_score)
        for key in ['side', 'shots', 'player', 'stack']:
            self.charting_widgets['winner'].rally_over.connect(self.charting_widgets[key].reset_buttons)

    def _shot_slots(self):
        """Connect signals for when the shot starts"""
        self.charting_widgets['player'].shot_started.connect(self.add_shot_player)
        self.charting_widgets['shots'].shot_type.connect(self.add_shot_type)
        self.charting_widgets['side'].shot_side.connect(self.add_shot_side)
        self.charting_widgets['location'].shot_location.connect(self.add_shot_location)

    def _shot_over_slots(self):
        """Connect signals for when the shot is over"""
        self.charting_widgets['outcome'].shot_over.connect(self.add_shot_outcome)
        self.log_shot.connect(self.charting_widgets['log'].add_entity)
        for key in ['side', 'shots', 'player']:
            self.charting_widgets['outcome'].shot_over.connect(self.charting_widgets[key].reset_buttons)

    def add_current_players(self, players):
        """Add the current players to the game"""
        self.current_players = players
        l = [p.to_dict() for p in self.current_players]
        self.setup_game_widget.log_widget.append(json.dumps(l, indent=4))

    def add_player_to_db(self, player):
        """Adds new players to the database"""
        print(f'Add_player_to_db: {type(player)} {player}')
        self.db.add_players(player)

    def add_rally_outcome(self, value):
        """Add the rally outcome to the current rally"""
        self.current_rally.rally_winner = value

        # now that rally is complete, add to log with additional info
        rd = self.current_rally.to_dict()
        rd['game_guid'] = self.current_game.game_guid
        rd['player_guids'] = [p.player_guid for p in self.current_players]
        self.logger.info(m(**rd))

        # move on to the next rally
        self.current_game.rallies.append(self.current_rally)
        self.log_rally.emit(self.current_rally)
        self.current_rally = Rally()

    def add_shot_location(self, value):
        self.current_shot.shot_location = value

    def add_shot_outcome(self, value):
        """Add the shot_outcome to the current shot"""
        self.current_shot.shot_outcome = value
        valid, message = self.validate_shot()
        if valid:       
            self.current_rally.shots.append(self.current_shot)
            self.log_shot.emit(self.current_shot)
            self.current_shot = Shot()
        else:
            QMessageBox.warning(self, "Invalid Shot", message, QMessageBox.Ok)

    def add_shot_player(self, player_index):
        """Add the player to the current shot"""
        self.current_shot.player_guid = self.current_players[player_index].player_guid

    def add_shot_side(self, value):
        self.current_shot.shot_side = value

    def add_shot_type(self, value):
        self.current_shot.shot_type = value

    def create_new_game(self):
        # Read the tabs and fill out the game object
        self.current_game.game_date = self.setup_game_widget.game_date_picker.date().toString('m-d-yyyy')
        self.current_game.game_location = self.setup_game_widget.game_location_edit.text()
        player_guids = [item.currentData() for item in self.setup_game_widget.player_combos]
        self.current_game.players = self.db.get_players(guids=player_guids)

    def find_new_players(self):
        """Find the new players that have been added"""
        existing = [player.player_guid for player in self.existing_players]
        return [p for p in self.current_players if p.player_guid not in existing]            

    def switch_to_charting(self):
        self.tab_widget.setCurrentIndex(1)

    def update_score(self, winner):
        """Update the score in response to rally_over signal"""
        self.current_rally.rally_winner = winner
        self.current_game.rallies.append(self.current_rally)
        self.current_score = next_score(self.current_score, winner)
        self.logger.debug(f"Score is now {self.current_score.to_dict()}")
        self.charting_widgets['score'].update_label(self.current_score)
        self.current_rally = Rally(rally_score=self.current_score)

    def validate_shot(self):
        """Validate the shot"""
        prev_shot = self.current_rally.shots[-1] if self.current_rally.shots else None

        # shot should not have any empty attributes
        for key, value in vars(self.current_shot).items():
            if any((value is None, value == '')):
                return (False, f'Shot has empty attributes {key=} {value=}')

        # for first shot it should be the serve
        if not prev_shot:
            if self.current_shot.shot_type != '1 - SERVE':
                return (False, f'First shot should be a serve: {self.current_shot.shot_type=}')
            else:
                return (True, None)
        
        # test that return follows serve
        if prev_shot.shot_type == '1 - SERVE':
            if self.current_shot.shot_type != '2 - RETURN':
                return (False, f'Second shot should be a return: {self.current_shot.shot_type=}')
        
        # test that teams alternate
        # get the index of the current player and the previous player
        player_guids = [p.player_guid for p in self.current_players]
        current_player = player_guids.index(self.current_shot.player_guid)
        prev_player = player_guids.index(prev_shot.player_guid)

        # now apply rules to ensure that the players alternate
        if all((prev_player < 2, current_player < 2)):   
            return (False, f'Players should alternate: {prev_player=} {current_player=}')
        if all((prev_player >= 2, current_player >= 2)):   
            return (False, f'Players should alternate: {prev_player=} {current_player=}')

        # test that the rally is not already over
        if prev_shot.shot_outcome != 'Continue':
            return (False, 'Should not have another shot after a winner or error - rally is over')
        return (True, None)


if __name__ == "__main__":

    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Set the logger level to the lowest level you want to log

    # Create a handler for exceptions and errors
    error_handler = logging.handlers.RotatingFileHandler(user_data_dir / 'pbcgui_errors.log', maxBytes=10*1024*1024, backupCount=3)
    error_handler.setLevel(logging.ERROR)

    # Create a handler for info
    info_handler = logging.handlers.RotatingFileHandler(user_data_dir / 'pbcgui_rallies.log', maxBytes=10*1024*1024, backupCount=3)
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(logging.Formatter('%(message)s'))

    # Add handlers to the logger
    logger.addHandler(error_handler)
    logger.addHandler(info_handler)

    app = QApplication(sys.argv)
    window = TouchscreenApp()
    window.showMaximized()
    sys.exit(app.exec())

