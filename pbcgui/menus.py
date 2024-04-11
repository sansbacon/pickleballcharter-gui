from PySide6.QtGui import QKeySequence, QAction
from PySide6.QtWidgets import QMenuBar, QMenu


class AppMenuBar(QMenuBar):
    """Custom app menu bar"""
    def __init__(self, parent=None):
        super(AppMenuBar, self).__init__(parent)

        file_menu = QMenu("File", self)
        
        # New Game action
        new_game_action = QAction("New Game", self)
        new_game_action.setShortcut(QKeySequence.New)  # Set the shortcut to Ctrl+N
        #new_game_action.triggered.connect(parent.initUISetupGame)  # Connect to the parent's method
        file_menu.addAction(new_game_action)

        # Load Game action
        load_game_action = QAction("Load Game", self)
        load_game_action.setShortcut(QKeySequence.Open)  # Set the shortcut to Ctrl+O
        #load_game_action.triggered.connect(parent.initUIChartGame)  # Connect to the parent's method
        file_menu.addAction(load_game_action)

        quit_action = QAction("Quit", self)
        quit_action.setShortcut(QKeySequence.Quit)  # Set the shortcut to Ctrl+Q
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        self.addMenu(file_menu)

        # Edit menu
        edit_menu = QMenu("Edit", self)
        copy_action = QAction("Copy", self)
        copy_action.setShortcut(QKeySequence.Copy)  # Set the shortcut to Ctrl+C
        edit_menu.addAction(copy_action)
        self.addMenu(edit_menu)

        # Help menu
        help_menu = QMenu("Help", self)
        self.addMenu(help_menu)