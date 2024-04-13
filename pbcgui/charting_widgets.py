from PySide6.QtWidgets import (
    QWidget, QSizePolicy, QGridLayout, QVBoxLayout, QHBoxLayout, 
    QGroupBox, QPushButton, QButtonGroup)
from PySide6.QtGui import QKeySequence
from PySide6.QtCore import Qt, Signal

from .entities import ShotTypes
from .utility import next_score, unique_names


class PlayerSectionWidget(QWidget):
    """A widget for the player section of the sidebar"""
    
    def __init__(self, parent=None):
        super(PlayerSectionWidget, self).__init__(parent)
        self.player_section = QGroupBox("Player")
        self.player_section_layout = QVBoxLayout()
        self.player_section.setLayout(self.player_section_layout)
    
        self.player_button_group = QButtonGroup()
        self.player_button_group.setExclusive(True)
        self.player_buttons = []

        player_shortcuts = {
            ('A', 1): QKeySequence(Qt.ControlModifier | Qt.Key_Up),
            ('A', 2): QKeySequence(Qt.ControlModifier | Qt.Key_Right),
            ('B', 1): QKeySequence(Qt.ControlModifier | Qt.Key_Left),
            ('B', 2): QKeySequence(Qt.ControlModifier | Qt.Key_Down),
        }

        for team in ["A", "B"]:
            row_layout = QHBoxLayout()
            self.player_section_layout.addLayout(row_layout)
            for i in range(1, 3):
                player_button = QPushButton(f"Player {team}{i}")
                player_button.setCheckable(True)
                player_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                player_button.setShortcut(player_shortcuts[(team, i)])
                row_layout.addWidget(player_button)
                self.player_button_group.addButton(player_button)
                self.player_buttons.append(player_button)
    
class ScoreSectionWidget(QWidget):
    """Creates the score section of the sidebar"""

    rally_over = Signal(tuple)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.score_section = QGroupBox('Score')
        self.score_section_layout = QVBoxLayout()
        self.score_section.setLayout(self.score_section_layout)

        self.score_button = QPushButton("0-0-2")
        self.score_section_layout.addWidget(self.score_button)

        self.server_wins_button = QPushButton("Server Wins")
        self.score_section_layout.addWidget(self.server_wins_button)

        self.receiver_wins_button = QPushButton("Receiver Wins")
        self.score_section_layout.addWidget(self.receiver_wins_button)

       # Connect the clicked signal of the buttons to a method that emits rally_over
        self.server_wins_button.clicked.connect(lambda: self.emit_rally_over("server"))
        self.receiver_wins_button.clicked.connect(lambda: self.emit_rally_over("receiver"))

    def emit_rally_over(self, winner):
        score = self.score_button.text().split('-')
        new_score = next_score(score, winner)
        self.rally_over.emit('-'.join([str(s) for s in new_score]))


class StackSectionWidget(QWidget):
    """Class to encapsulate stack section for sidear"""

    stacks_possible = [
        ['A2 Left', 'A2 Right'],
        ['B2 Left', 'B2 Right'],
        ['No Stack']
    ]

    stack_shortcuts = {
        'A2 Left': QKeySequence(Qt.ControlModifier | Qt.ShiftModifier | Qt.Key_Up),
        'A2 Right': QKeySequence(Qt.ControlModifier | Qt.ShiftModifier | Qt.Key_Right),
        'B2 Left': QKeySequence(Qt.ControlModifier | Qt.ShiftModifier | Qt.Key_Left),
        'B2 Right': QKeySequence(Qt.ControlModifier | Qt.ShiftModifier | Qt.Key_Down)
    }

    def __init__(self, parent=None):
        super(PlayerSectionWidget, self).__init__(parent)
        self.section = QGroupBox("Stack")
        self.layout = QVBoxLayout()   
        self.section.setLayout(self.layout)
        
        # create the button group
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        self.buttons = []

        # keyboard shortcuts
    
        # create the button grid
        button_grid = QGridLayout()
        self.layout.addLayout(button_grid)

        for idx, stacks in enumerate(self.stacks_possible):
            for jdx, stack in enumerate(stacks):
                button = QPushButton(stack)
                button.setCheckable(True)
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                button.setShortcut(self.stack_shortcuts[stack])
                button_grid.addWidget(button, idx, jdx)
                self.buttons.append(button)
                self.button_group.addButton(button)



class ChartSidebarWidget(QWidget):
    """A widget for the sidebar of the charting tab"""

    rally_over = Signal()

    def __init__(self, parent=None):
        super(ChartSidebarWidget, self).__init__(parent)
        self._score_section = self.score_section()
        self._player_section = self.player_section()
        self._stack_section = self.stack_section()
        self._sidebar = self.sidebar()
        self.setLayout(self._sidebar)

    def player_section(self):
        """Creates the player section of the sidebar"""
        player_section = QGroupBox("Player")
        player_section_layout = QVBoxLayout()
        player_section.setLayout(player_section_layout)

        self.player_button_group = QButtonGroup()
        self.player_button_group.setExclusive(True)
        self.player_buttons = []

        player_shortcuts = {
            ('A', 1): QKeySequence(Qt.ControlModifier | Qt.Key_Up),
            ('A', 2): QKeySequence(Qt.ControlModifier | Qt.Key_Right),
            ('B', 1): QKeySequence(Qt.ControlModifier | Qt.Key_Left),
            ('B', 2): QKeySequence(Qt.ControlModifier | Qt.Key_Down),
        }

        for team in ["A", "B"]:
            row_layout = QHBoxLayout()
            player_section_layout.addLayout(row_layout)
            for i in range(1, 3):
                player_button = QPushButton(f"Player {team}{i}")
                player_button.setCheckable(True)
                player_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                player_button.setShortcut(player_shortcuts[(team, i)])
                row_layout.addWidget(player_button)
                self.player_button_group.addButton(player_button)
                self.player_buttons.append(player_button)

        self._player_section = player_section
        return player_section

    def score_section(self):
        """Creates the score section of the sidebar"""
        score_section = QGroupBox('Score')
        score_section_layout = QVBoxLayout()
        score_section.setLayout(score_section_layout)

        self.score_button = QPushButton("0-0-2")
        score_section_layout.addWidget(self.score_button)

        self.server_wins_button = QPushButton("Server Wins")
        score_section_layout.addWidget(self.server_wins_button)

        self.receiver_wins_button = QPushButton("Receiver Wins")
        score_section_layout.addWidget(self.receiver_wins_button)

        self._score_section = score_section
        return score_section
    
    def stack_section(self):
        """Creates the stack section for the sidebar"""
        stack_section = QGroupBox("Stack")
        stack_section_layout = QVBoxLayout()
        stack_section.setLayout(stack_section_layout)

        # create the button group
        self.stack_button_group = QButtonGroup()
        self.stack_button_group.setExclusive(True)
        self.stack_buttons = []

        # Create the first row of buttons
        first_row_layout = QHBoxLayout()
        stack_section_layout.addLayout(first_row_layout)

        stack_shortcuts = {
            'A2 Left': QKeySequence(Qt.ControlModifier | Qt.ShiftModifier | Qt.Key_Up),
            'A2 Right': QKeySequence(Qt.ControlModifier | Qt.ShiftModifier | Qt.Key_Right),
            'B2 Left': QKeySequence(Qt.ControlModifier | Qt.ShiftModifier | Qt.Key_Left),
            'B2 Right': QKeySequence(Qt.ControlModifier | Qt.ShiftModifier | Qt.Key_Down)
        }

        for idx, stacks in enumerate(['A2 Left', 'A2 Right']):
            button = QPushButton(stacks)
            button.setCheckable(True)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setShortcut(QKeySequence(stack_shortcuts[stacks]))
            self.stack_buttons.append(button)
            first_row_layout.addWidget(self.stack_buttons[idx])
            self.stack_button_group.addButton(self.stack_buttons[idx])

        # Create the second row of buttons
        second_row_layout = QHBoxLayout()
        stack_section_layout.addLayout(second_row_layout)

        for stacks in ['B2 Left', 'B2 Right']:
            button = QPushButton(stacks)
            button.setCheckable(True)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setShortcut(QKeySequence(stack_shortcuts[stacks]))
            self.stack_buttons.append(button)
            second_row_layout.addWidget(button)
            self.stack_button_group.addButton(button)

        # Create the third row of buttons
        third_row_layout = QHBoxLayout()
        stack_section_layout.addLayout(third_row_layout)
        button = QPushButton('No Stack')
        button.setCheckable(True)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button.setChecked(True)
        self.stack_buttons.append(button)
        third_row_layout.addWidget(button)
        self.stack_button_group.addButton(button)

        self._stack_section = stack_section
        return stack_section

    def sidebar(self):
        """Creates the sidebar column with the following sections:"""
        # Create the first column with three sections
        # This column is on the left - sidebar
        first_column = QVBoxLayout()

        # Left 1 - Section 1 - Score and Rally Winner
        first_column.addWidget(self._score_section, 15)

        # clicking button indicates rally is over
        self.server_wins_button.clicked.connect(self.rally_over.emit)
        self.receiver_wins_button.clicked.connect(self.rally_over.emit)

        # Left 2 - Section 2 - Player
        first_column.addWidget(self._player_section, 50)

        # Left 3 - Section 3 - Stack
        first_column.addWidget(self._stack_section, 35)

        self._sidebar = first_column    
        return first_column

class ChartGameWidget(QWidget):

    def __init__(self, parent=None):
        super(ChartGameWidget, self).__init__(parent)

        vlayout = QVBoxLayout()
        self.setLayout(vlayout)

        # Create a horizontal layout
        hlayout = QHBoxLayout()
        self.sidebar = ChartSidebarWidget()
        hlayout.addWidget(self.sidebar)
        #hlayout.addLayout(self.sidebar)
        hlayout.addLayout(self.main_column())

        hlayout.setStretch(0, 25)
        hlayout.setStretch(1, 75)

        # Add the second tab to the tab widget
        vlayout.addLayout(hlayout)

        # event handling
        #self.rally_over.connect(self.handle_rally_over)

    def main_column(self):
        """Creates the main column with the following sections:"""
        main_column = QVBoxLayout()

        # Create the "Shots" section
        shots_section = QGroupBox("Shots")
        shots_section_layout = QGridLayout()
        shots_section.setLayout(shots_section_layout)
        main_column.addWidget(shots_section)

        # Add shots buttons
        self.shots_button_group = QButtonGroup()
        self.shots_button_group.setExclusive(True)
        for idx, shot_type in enumerate(ShotTypes):
            j = idx % 5
            i = idx // 5
            button = QPushButton(f"{shot_type.value} - {shot_type.name}")
            button.setCheckable(True)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            if idx < 9:
                button.setShortcut(QKeySequence(f"Ctrl+{idx+1}"))
            elif idx == 9:
                button.setShortcut(QKeySequence(f"Ctrl+0"))
            else:
                button.setShortcut(QKeySequence(f"Ctrl+Alt+{idx-9}"))
            shots_section_layout.addWidget(button, j, i)
            self.shots_button_group.addButton(button)

        ############
        # Create the other sections
        # Create a horizontal layout for the "Side" and "Effect" sections
        side_effect_layout = QHBoxLayout()

        for section_name in ["Side", "Effect", "Rally Winner"]:
            section = QGroupBox(section_name)
            section_layout = QVBoxLayout()
            section.setLayout(section_layout)
            side_effect_layout.addWidget(section)

        # Add the horizontal layout to the main column
        main_column.addLayout(side_effect_layout)

        return main_column
    
    def handle_rally_over(self):
        # This method will be called when the rally is over
        pass

    def update_player_buttons(self, players):
        """Updates the text of the stack buttons"""
        for idx, player in enumerate(unique_names([p.split()[0] for p in players])):
            self.sidebar.player_buttons[idx].setText(player)
        
    def update_stack_buttons(self, players):
        """Updates the text of the stack buttons"""
        players = unique_names([p.split()[0] for p in players])
        self.sidebar.stack_buttons[0].setText(f'{players[1]} Left')
        self.sidebar.stack_buttons[1].setText(f'{players[1]} Right')
        self.sidebar.stack_buttons[2].setText(f'{players[3]} Right')
        self.sidebar.stack_buttons[3].setText(f'{players[3]} Left')
 