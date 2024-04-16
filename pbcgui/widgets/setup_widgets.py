from PySide6.QtCore import QDate, Signal

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QSizePolicy, QGroupBox, QTextEdit,
    QLabel, QDateEdit, QLineEdit, QSpacerItem,
    QComboBox, QMessageBox, QCompleter
)

from .log import LogWidget

class SetupGameWidget(QWidget):

    newGameRequested = Signal(list)

    def __init__(self, players, parent=None):
        super(SetupGameWidget, self).__init__(parent)
        
        # instance variables
        self.log_widget = LogWidget()
        self.game_date_picker = QDateEdit()
        self.game_location_edit = QLineEdit()
        self.game_location_edit.editingFinished.connect(self.log_text_change)
        self.players = [''] + players
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
        self.game_date_picker.setDisplayFormat("MMMM d, yyyy")
        info_section_layout.addWidget(game_date_label)
        info_section_layout.addWidget(self.game_date_picker)
        self.game_date_picker.dateChanged.connect(self.log_date_change)

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
        msg = ["<b>Enter player names in the fields below.</b>",
               "<b>Player one should be the initial server, player two is server's partner.</b>",
                "<b>Player three is the returner, and player four is the returner's partner.</b>"]

        players_section_layout.addWidget(QLabel('<br>'.join(msg)))

        # Add a spacer for padding
        players_section_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # now add player combos
        for idx, widget in enumerate(self.player_combos):
            player_label = QLabel(f"Player {idx + 1}")
            widget.currentTextChanged.connect(self.log_cb_change)
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
        self.new_game_button.clicked.connect(self.validate_and_emit_new_game)
        button_layout.addWidget(self.new_game_button)

        # LOG SECTION
        left_column.addWidget(self.log_widget)

        # RIGHT COLUMN
        right_column = QVBoxLayout()
        main_layout.addLayout(right_column, 67)  

    def create_player_combo(self):
        combo = QComboBox()
        combo.setEditable(True)
        combo.addItems([str(p) for p in self.players])
        completer = QCompleter()
        completer.setModel(combo.model())
        combo.setCompleter(completer)
        return combo

    def log_cb_change(self, s):
        self.log_widget.append(s)

    def log_text_change(self):
        line_edit = self.sender()
        new_text = line_edit.text()
        self.log_widget.append(new_text)

    def log_date_change(self, new_date):
        self.log_widget.append(new_date.toString())

    def validate_and_emit_new_game(self):
        """Validates against duplicates and empty strings, then emits a signal with the player names."""
        values = [cb.currentText() for cb in self.player_combos]

        if "" in values:
            QMessageBox.warning(self, "Validation Error", "Player Names Cannot Be Empty.")
            return

        if len(set(values)) != len(values):
            QMessageBox.warning(self, "Validation Error", "Player Names Cannot Be Duplicated.")
            return

        self.newGameRequested.emit(values)