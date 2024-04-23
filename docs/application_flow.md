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

Emitted by sgw when game and player information is validated

Slots

app.add_current_players
-PlayerSectionWidget.update_buttons

StackSectionWidget.update_buttons

app.switch_to_charting

app.emit_initial_score

app.emit_serving_team

