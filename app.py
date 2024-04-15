import json
from pathlib import Path
import sys
from uuid import uuid4

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QTabWidget, QMainWindow, QApplication

from config import user_data_dir, user_data_file
from pbcgui.data import database_factory, Game, DateTimeEncoder, ShotTypes
from pbcgui.palettes import AppPalette
from pbcgui.widgets import *


class TouchscreenApp(QMainWindow):
    """Main class for charting app"""

    score_changed = Signal(tuple)

    def __init__(self):
        super().__init__()
        
        # database setup
        self.db = database_factory(db_type='tinydb', db_path=user_data_dir / user_data_file)
        
        # entity setup
        self.current_score = (0, 0, 2)
        self.existing_players = self.db.get_players()
        self.existing_games = self.db.get_games()
        self.game = Game()

        # setup the widgets
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

        # Create the UI
        self.initUI()

        # log data
        for game in self.db.get_games():
            self.setup_game_widget.log_widget.append(json.dumps(game, cls=DateTimeEncoder, indent=4))

        # Connect signals
        self.setup_game_widget.newGameRequested.connect(self.charting_widgets['player'].update_buttons)
        self.setup_game_widget.newGameRequested.connect(self.charting_widgets['stack'].update_buttons)
        self.setup_game_widget.newGameRequested.connect(self.switch_to_charting)
        self.charting_widgets['winner'].rally_over.connect(self.charting_widgets['score'].update_score)


    def initUI(self):
        # Set the palette
        self.setPalette(AppPalette())
        
        # Create a menu bar
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

    def create_new_game(self):
        # Read the tabs and fill out the game object
        self.game.game_date = self.setup_game_widget.game_date_picker.date().toString('m-d-yyyy')
        self.game.game_location = self.setup_game_widget.game_location_edit.text()
        self.game.teams = {
            "A": [self.setup_game_widget.player_combos[0].currentText(), self.setup_game_widget.player_combos[1].currentText()],
            "B": [self.setup_game_widget.player_combos[2].currentText(), self.setup_game_widget.player_combos[3].currentText()]
        }
        self.setup_game_widget.log_widget.append(json.dumps(self.game.to_dict(), cls=DateTimeEncoder, indent=4))
        self.db.add_games(self.game)

    def process_shot_button_click(self, button):
        """Process the shot button click event"""
        # Get the text of the button
        return button.text()

    def switch_to_charting(self):
        self.tab_widget.setCurrentIndex(1)

    def update_score(self, new_score):
        """Update the score and emits the score_changed signal"""
        self.current_score = new_score
        self.score_changed.emit(self.current_score)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TouchscreenApp()
    window.showMaximized()
    sys.exit(app.exec())
