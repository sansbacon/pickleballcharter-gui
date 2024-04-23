# pickleballcharter-gui
GUI desktop application for pickleball charting

# Data Model

```
class Player:
    """Data class for a player"""
    first_name: str
    last_name: str
    nickname: str 
    gender: str 
    full_name: str 
    player_guid: str = str(uuid4())
```

```
class Team:
    """Data class for a team"""
    players: List[Player] 
    score: int
    opp_score: int
    win: int
```

```
class Shot:
    """Data class for a shot"""
    player_guid: str 
    shot_type: str 
    shot_side: str 
    shot_outcome: str 
```

```
class Rally:
    """Data class for a rally
    Score is when the rally starts"""
    rally_score: tuple
    rally_winner: str 
    shots: List[Shot]
    stack: List[str]
```

```
class Game:
    """Data class for a game"""
    game_guid: str = str(uuid4())
    game_date: datetime 
    game_location: str 
    teams: List[Team]
    rallies: List[Rally]
    final_score: tuple # always team 1 then team 2
```

# Signals and Slots

* newGameRequested
  * member of: SetupGameWidget
  * description: signal to indicate completion/validation of creating a new game
  * trigger: new_game_button.clicked()
  * emitted by: validate_and_emit_new_game
  * slots:
    * TouchscreenApp.add_current_players
    * TouchscreenApp.switch_to_charting
    * TouchscreenApp.emit_score_signal
    * TouchscreenApp.emit_player_sign


            self.setup_game_widget.newGameRequested.connect(self.add_current_players)
        self.setup_game_widget.newGameRequested.connect(self.switch_to_charting)
        self.setup_game_widget.newGameRequested.connect(self.emit_score_signal)
        self.setup_game_widget.newGameRequested.connect(self.emit_player_signal)


* player_added
  * member of: PlayerDialog
  * description: signal that dialog is complete and Player should be added to db and comboboxes.
  * trigger: buttonBox.accepted
  * emitted by: accept
  * slots:
    * TouchscreenApp.add_player_to_db
    * SetupGameWidget.process_new_player
      
* shot_started
  * member of: PlayerSectionWidget
  * description: when click on a Player button, that is a signal of the start of a new shot. Sends the index of the clicked player button which can be used to get Player object.
  * trigger: button_group.buttonClicked
  * emitted by: emit_shot_started
  * slots:
    * PlayerSectionWidget.add_shot_player: Sets TouchscreenApp.current_shot.player_guid = player_guid


* shot_type
  * member of: ChartingShotsWidget
  * description: signal that selected Shot Type. Is the button text.
  * trigger: button_group.buttonClicked
  * emitted by: emit_shot_type, where shot_type is the text of the shot button
  * slots:
    * ShotTypeWidget.add_shot_type: Sets TouchscreenApp.current_shot.shot_type = shot_type


* shot_side
  * member of: ChartingShotsWidget
  * description: signal that selected Shot Type. Is the button text.
  * trigger: button_group.buttonClicked
  * emitted by: emit_shot_type, where shot_type is the text of the shot button
  * slots:
    * ShotTypeWidget.add_shot_sie: Sets TouchscreenApp.current_shot.shot_side = shot_side


* shot_over
  * member of: ShotOutcomeWidget
  * description: signal that shot is over (last step is the ShotOutcome). Is the button text.
  * trigger: button_group.buttonClicked
  * emitted by: emit_shot_over, where shot_outcome is the text of the button.
  * slots:
    * TouchscreenApp.add_shot_outcome: adds shot_outcome value to current_shot
    * ShotSideWidget.reset_buttons: clears the buttons in this widget
    * ShotOutcomeWidget.reset_buttons: clears the buttons in this widget
    * ChartingShotsWidget.reset_buttons: clears the buttons in this widget
    * PlayerSectionWidget: clears the buttons in this widget

* rally_over
  * member of: RallyWinnerWidget
  * description: signal that rally is over (last step is clicking on the button). Is the button text.
  * trigger: button_group.buttonClicked
  * emitted by: emit_rally_winner, where rally_winner is either server or receiver.
  * slots:
    * TouchscreenApp.update_score: updates current_score based on prior score and rally_winner
    * ScoreSectionWidget.update_label: updates the score label with the current value
    * ShotSideWidget.reset_buttons: clears the buttons in this widget
    * ShotOutcomeWidget.reset_buttons: clears the buttons in this widget
    * ChartingShotsWidget.reset_buttons: clears the buttons in this widget
    * PlayerSectionWidget: clears the buttons in this widget

* game_edited
  * member of: RallyReviewWidget
  * description: signal that game has been edited on the rally review page.
  * trigger: save_button.clicked.
  * emitted by: save_changes, where updated Game is emitted.
  * slots:
    * NOT IMPLEMENTED YET