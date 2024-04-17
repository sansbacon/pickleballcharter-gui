from pbcgui.data import Game, Player

g = Game()
print(g)

p = Player(first_name='Eric', last_name='Truett')
assert p.full_name == 'Eric Truett'
p = Player(first_name='Eric', last_name='Truett', nickname='JimBob')
assert p.full_name == 'Eric Truett (JimBob)'