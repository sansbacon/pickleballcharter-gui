# Application Flow

## Setup Game tab:

Add details about games and players.

Implemented by SetupGameWidget class (sgw).

When user clicks Create New Game (sgw.new_game_button):

* Button signal connected to sgw.validate_and_emit_new_game.

* Slot checks that there are no empty or duplicate player names.

* If not valid, display error message and button action canceled

* If valid, emits sgw.newGameRequested

## newGameRequested signal

Emitted by sgw when game and player information is validated. Connected to the following slots:

* app.add_current_players
* PlayerSectionWidget.update_buttons
* StackSectionWidget.update_buttons
* app.switch_to_charting
* app.emit_initial_score
* app.emit_serving_team

## Charting Tab

- Click PlayerSectionWidget Button:

Emits PlayerSectionWidget.shot_started signal - is an integer of the button that was clicked in the group
PlayerSectionWidget.shot_started signal connected to the following slots:
* app.add_shot_player - adds the player to the app.current_shot Shot object
* app.focus_on_next_widget - switches focus to ShotType button group (skips over StackSection)

- Click ChartingShotsWidget Button:

Emits ChartingShotsWidget.shot_type signal - is a string of the clicked button's label (1 - SERVE, etc.)
ChartingShotsWidget.shot_type is connected to the following slots:
* app.add_shot_type - adds the shot type to the app.current_shot Shot object
* app.focus_on_next_widget - switches focus to ShotSide button group

- Click ShotSideWidget Button:

Emits ShotSideWidget.shot_side signal - is a string of the clicked button's label (Forehand, Backhand)
ShotSideWidget.shot_side is connected to the following slots:
* app.add_shot_side - adds the shot side to the app.current_shot Shot object
* app.focus_on_next_widget - switches focus to ShotLocation button group

- Click ShotLocationWidget Button:

Emits ShotLocationWidget.shot_location signal - is a string of the clicked button's label (Left Outer, etc.)
ShotSideWidget.shot_side is connected to the following slots:
* app.add_shot_location - adds the shot location to the app.current_shot Shot object
* app.focus_on_next_widget - switches focus to ShotLocation button group

- Click ShotOutcomeWidget Button:

Emits ShotOutcomeWidget.shot_outcome signal - is a string of the clicked button's label (Winner, etc.)
ShotSideWidget.shot_outcome is connected to the following slots:
* app.add_shot_outcome - adds the shot outcome to the app.current_shot Shot object
* app.focus_on_next_widget - switches focus to RallyOutcome button group [TODO: this may not be needed]

