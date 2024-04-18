import sys

from PySide6.QtWidgets import QTabWidget, QMainWindow, QApplication, QMessageBox

from config import user_data_dir, user_data_file
from pbcgui.data import database_factory, Game, Rally, Shot, ShotTypes
from pbcgui.palettes import AppPalette
from pbcgui.widgets import *


class TouchscreenApp(QMainWindow):
    """Main class for charting app"""

    #score_changed = Signal(tuple)

    def __init__(self):
        super().__init__()        
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
            "outcome": ShotOutcomeWidget(),
            "shots": ChartingShotsWidget(shot_types=ShotTypes),
            "winner": RallyWinnerWidget()
        }

        self.charting_widgets['sidebar'] =  ChartingSidebarWidget(
            self.charting_widgets['player'], self.charting_widgets['score'], self.charting_widgets['stack']
        )

        self.charting_widgets['main'] = ChartingMainWidget(
                self.charting_widgets['shots'], 
                [self.charting_widgets['side'], self.charting_widgets['outcome'], self.charting_widgets['winner']]
        )

        self.charting_widgets['tab'] = ChartTabWidget(self.charting_widgets['sidebar'], self.charting_widgets['main'])

    def _initProperties(self):
        """Initialize the properties of the application"""
        self.current_game = Game()
        self.current_players = []
        self.current_score = (0, 0, 2)
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
        self.setup_game_widget.newGameRequested.connect(self.charting_widgets['player'].update_buttons)
        self.setup_game_widget.newGameRequested.connect(self.charting_widgets['stack'].update_buttons)
        self.setup_game_widget.newGameRequested.connect(self.switch_to_charting)

    def _rally_over_slots(self):
        """Connect signals for when the rally is over"""
        self.charting_widgets['winner'].rally_over.connect(self.update_score)
        self.charting_widgets['winner'].rally_over.connect(self.charting_widgets['score'].update_label)
        for key in ['side', 'shots', 'player', 'stack']:
            self.charting_widgets['winner'].rally_over.connect(self.charting_widgets[key].reset_buttons)

    def _shot_slots(self):
        """Connect signals for when the shot starts"""
        self.charting_widgets['player'].shot_started.connect(self.add_shot_player)
        self.charting_widgets['shots'].shot_type.connect(self.add_shot_type)
        self.charting_widgets['side'].shot_side.connect(self.add_shot_side)

    def _shot_over_slots(self):
        """Connect signals for when the shot is over"""
        self.charting_widgets['outcome'].shot_over.connect(self.add_shot_outcome)
        for key in ['side', 'shots', 'player']:
            self.charting_widgets['outcome'].shot_over.connect(self.charting_widgets[key].reset_buttons)

    def add_player_to_db(self, player):
        """Adds new players to the database"""
        print(f'Add_player_to_db: {type(player)} {player}')
        self.db.add_players(player)

    def add_shot_outcome(self, value):
        """Add the shot_outcome to the current shot"""
        self.current_shot.outcome = value
        self.current_rally.shots.append(self.current_shot)
        self.current_shot = Shot()

    def add_shot_player(self, player_index):
        """Add the player to the current shot"""
        self.current_shot.player_guid = self.current_players[player_index].player_guid

    def add_shot_side(self, value):
        self.current_shot.side = value

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
        """Update the score and emits the score_changed signal"""
        self.current_rally.winner = winner
        self.current_game.rallies.append(self.current_rally)
        self.current_score = next_score(self.current_score, winner)
        self.current_rally = Rally(rally_score=self.current_score)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TouchscreenApp()
    window.showMaximized()
    sys.exit(app.exec())
