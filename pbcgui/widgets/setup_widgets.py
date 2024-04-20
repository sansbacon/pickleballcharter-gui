import logging
from typing import List

from PySide6.QtCore import QDate, QObject, Signal

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QSizePolicy, QGroupBox,
    QLabel, QDateEdit, QLineEdit, QSpacerItem,
    QComboBox, QMessageBox
)

from ..data import Player
from .log import LogWidget
from .player_dialog import PlayerDialog


class SetupGameWidget(QWidget):
    """A widget for setting up a new game."""

    newGameRequested = Signal(list)

    def __init__(self, players):
        """
        Initialize the SetupGameWidget with the given players.

        Args:
            players (List[Player]): A list of player objects.
            
        """
        super().__init__()
        
        # instance variables
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())
        self.log_widget = LogWidget()
        self.game_date_picker = QDateEdit()
        self.game_location_edit = QLineEdit()
        self.existing_players = sorted(players, key=lambda player: player.first_name)
        self.player_combos = [self.create_player_combo() for _ in range(4)]
    
        # main layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # LEFT COLUMN
        # Create a vertical layout for the buttons and fields
        left_column = QVBoxLayout()
        main_layout.addLayout(left_column, 33)

        # INFO SECTION
        info_section = QGroupBox("Game Information")
        info_section_layout = QVBoxLayout()
        info_section.setLayout(info_section_layout)

        # Game Date
        game_date_label = QLabel("Game Date")
        self.game_date_picker.setDate(QDate.currentDate())
        self.game_date_picker.setCalendarPopup(True)
        self.game_date_picker.setDisplayFormat("yyyy-MM-dd")
        info_section_layout.addWidget(game_date_label)
        info_section_layout.addWidget(self.game_date_picker)

        # Game Location
        game_location_label = QLabel("Game Location")
        info_section_layout.addWidget(game_location_label)
        info_section_layout.addWidget(self.game_location_edit)

        info_section_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Add the section to the main layout
        left_column.addWidget(info_section)

        # Players  
        # Create the "Players" section
        players_section = QGroupBox("Player Information")
        players_section_layout = QVBoxLayout() 
        players_section.setLayout(players_section_layout)

        # Add instructions at the top of the box
        msg_section_layout = QHBoxLayout()
        msg = ["<b>Enter player names in the fields below.</b>",
               "<b>Player one should be the initial server, player two is server's partner.</b>",
                "<b>Player three is the returner, and player four is the returner's partner.</b>"]

        msg_section_layout.addWidget(QLabel('<br>'.join(msg)))
        addPlayerButton = QPushButton("Add New Player")
        addPlayerButton.setStyleSheet("background-color: #f0f0f0; color: #000000;")
        addPlayerButton.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        addPlayerButton.clicked.connect(self.launch_new_player_dialog)
        msg_section_layout.addWidget(addPlayerButton)
        players_section_layout.addLayout(msg_section_layout)

        # Add a spacer for padding
        players_section_layout.addItem(QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # now add player combos
        for idx, widget in enumerate(self.player_combos):
            player_label = QLabel(f"Player {idx + 1}")
            players_section_layout.addWidget(player_label)
            players_section_layout.addWidget(widget)

        # Add the section to the main layout
        left_column.addWidget(players_section)
        
        # BUTTON SECTION
        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        left_column.addLayout(button_layout)

        # Add a form for creating a new game or reading an existing game
        self.new_game_button = QPushButton("Create New Game")
        self.new_game_button.setStyleSheet("background-color: #f0f0f0; color: #000000;")
        self.new_game_button.clicked.connect(self.validate_and_emit_new_game)
        button_layout.addWidget(self.new_game_button)

        # LOG SECTION
        left_column.addWidget(self.log_widget)

        # RIGHT COLUMN
        right_column = QVBoxLayout()
        main_layout.addLayout(right_column, 67)  

        # Player Dialog
        self.add_player_dialog = PlayerDialog()
        self.add_player_dialog.player_added.connect(self.process_new_player)

    def clear(self):
        """Clears widget fields back to defaults."""
        self.game_date_picker.setDate(QDate.currentDate())
        self.game_location_edit.clear()
        for lw in self.player_combos:
            lw.setCurrentIndex(0)
        self.log_widget.clear()

    def create_player_combo(self):
        """
        Create a QListWidget for each player.

        Returns:
            QListWidget: A QListWidget with the player names.

        """
        lw = QComboBox()
        lw.setEditable(False)
        for p in self.existing_players:
            lw.addItem(p.full_name, p.player_guid)
        return lw

    def launch_new_player_dialog(self):
        self.add_player_dialog.show()
        self.add_player_dialog.setFocus()

    def process_new_player(self, new_player):
        self.existing_players.append(new_player)
        for lw in self.player_combos:
            lw.insertItem(0, new_player.full_name, new_player.player_guid)

    def validate_and_emit_new_game(self):
        """Validate the player names and emit the newGameRequested signal."""
        values = [cb.currentText() for cb in self.player_combos]

        if "" in values:
            QMessageBox.warning(self, "Validation Error", "Player Names Cannot Be Empty.")
            return

        if len(set(values)) != len(values):
            QMessageBox.warning(self, "Validation Error", "Player Names Cannot Be Duplicated.")
            return

        new_game_players = [p for p in self.existing_players if p.full_name in values]
        #self.logger.debug(f'newGameRequested emitted List[Player]: {new_game_players}')
        self.newGameRequested.emit(new_game_players)