class Player:
    def __init__(self, name: str, symbol: str, is_turn: bool = False):
        self.name = name
        self.symbol = symbol
        self.is_turn = is_turn

    def toggle_turn(self):
        self.is_turn = not self.is_turn
