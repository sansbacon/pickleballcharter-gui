from PySide6.QtCore import QDate, Signal

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QGridLayout,
    QPushButton, QSizePolicy, QGroupBox, QTextEdit,
    QLabel, QDateEdit, QLineEdit, QSpacerItem
)


class SetupGameWidget(QWidget):

    newGameRequested = Signal()

    def __init__(self, parent=None):
        super(SetupGameWidget, self).__init__(parent)
        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)

        self.game_date_picker = QDateEdit()

        self.game_location_edit = QLineEdit()
        self.game_location_edit.editingFinished.connect(self.log_text_change)

        self.player_edits = [QLineEdit() for _ in range(4)]
        
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

        # now add player line edits
        for idx, widget in enumerate(self.player_edits):
            player_label = QLabel(f"Player {idx + 1}")
            widget.editingFinished.connect(self.log_text_change)
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
        self.new_game_button.clicked.connect(self.newGameRequested.emit)
        button_layout.addWidget(self.new_game_button)

        # LOG SECTION
        log_section = QGroupBox("Log")
        log_section_layout = QVBoxLayout()
        log_section_layout.addWidget(self.log_console)
        log_section.setLayout(log_section_layout)
        left_column.addWidget(log_section)

        # RIGHT COLUMN
        right_column = QVBoxLayout()
        main_layout.addLayout(right_column, 67)  

    def log_text_change(self):
        line_edit = self.sender()
        new_text = line_edit.text()
        self.log_console.append(new_text)

    def log_date_change(self, new_date):
        self.log_console.append(new_date.toString())