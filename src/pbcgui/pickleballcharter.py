import sys

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QTabWidget, QMainWindow, QApplication, QPushButton

from charting_widgets import ChartGameWidget
from db import DatabaseHandler
from entities import Game
from menus import AppMenuBar
from palettes import AppPalette
from utility import next_possible_scores
from setup_widgets import SetupGameWidget


class TouchscreenApp(QMainWindow):
    """Main class for charting app"""

    score_changed = Signal(tuple)

    def __init__(self, db_path:str = None):
        super().__init__()
        # Create the UI
        self.initUI()

        # Instantiate class variables 
        self.current_score = (0, 0, 2)
        self.db_handler = DatabaseHandler(db_path)
        self.game = Game(*[None for _ in range(6)])

        # setup event handlers
        #self.chart_game_widget.shots_button_group.buttonClicked.connect(self.process_shot_button_click)


    def initUI(self):
        # Set the palette
        self.setPalette(AppPalette())

        # Create a menu bar
        menu_bar = AppMenuBar(self)
        self.setMenuBar(menu_bar)  # Set the menu bar of the main window

        # Create a tab widget
        self.tab_widget = QTabWidget()

        # Initialize the first tab
        self.setup_game_widget = SetupGameWidget(self)
        self.setup_game_widget.newGameRequested.connect(self.create_new_game)
        self.tab_widget.addTab(self.setup_game_widget, "Setup Game")
        
        # Initialize the second tab
        self.chart_game_widget = ChartGameWidget(self)
        self.tab_widget.addTab(self.chart_game_widget, "Chart Game")

        # Set the tab widget as the central widget
        self.setCentralWidget(self.tab_widget)

    def create_new_game(self):
        # Read the tabs and fill out the game object
        teams = {
            "A": [self.setup_game_widget.player_edits[0].text(), self.setup_game_widget.player_edits[1].text()],
            "B": [self.setup_game_widget.player_edits[2].text(), self.setup_game_widget.player_edits[3].text()]
        }

        self.game.teams = teams

    def process_shot_button_click(self, button):
        """Process the shot button click event"""
        # Get the text of the button
        return button.text()

    def update_score(self, new_score):
        """Update the score and emits the score_changed signal"""
        self.current_score = new_score
        self.score_changed.emit(self.current_score)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TouchscreenApp()
    window.showMaximized()
    sys.exit(app.exec())
