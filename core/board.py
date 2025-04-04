class Board:
    def __init__(self, size=3):
        self.size = size
        self.grid = [["" for _ in range(size)] for _ in range(size)]

    def reset(self):
        self.grid = [["" for _ in range(self.size)] for _ in range(self.size)]

    def make_move(self, row: int, col: int, symbol: str) -> bool:
        if self.grid[row][col] == "":
            self.grid[row][col] = symbol
            return True
        return False

    def check_winner(self) -> str or None:
        size = self.size
        lines = []

        for i in range(size):
            lines.append(self.grid[i])  # rows
            lines.append([self.grid[r][i] for r in range(size)])  # columns

        lines.append([self.grid[i][i] for i in range(size)])
        lines.append([self.grid[i][size - i - 1] for i in range(size)])

        for line in lines:
            if line.count(line[0]) == size and line[0] != "":
                return line[0]

        return None

    def is_draw(self) -> bool:
        for row in self.grid:
            if "" in row:
                return False
        return self.check_winner() is None
