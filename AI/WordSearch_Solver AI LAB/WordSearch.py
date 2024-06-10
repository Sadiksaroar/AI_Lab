from random import choice, shuffle

class WordSearch:
    def __init__(self, size, words):
        self._size = size
        self._words = list(set(map(str.upper, words)))
        assert self._size - max(map(len, self._words)) > 2, f"Board size {self._size} is too small."
        shuffle(self._words)
        self.board = [[None for _ in range(self._size)] for _ in range(self._size)]
        self.solutions = {}
        check = False
        while not check:
            self._init_board()
            check = self._fill_with_words()
        self._fill_board()

    def _get_orientation(self, word_len):
        starty = startx = 0
        endy = endx = self._size
        orient = choice(range(0, 4))
        if orient == 0:  # Horizontal
            ox = 1
            oy = 0
            endx = self._size - word_len
        elif orient == 1:  # Vertical Down
            ox = 0
            oy = 1
            endy = self._size - word_len
        elif orient == 2:  # Upward Diagonal
            ox = 1
            oy = -1
            starty = word_len
            endx = self._size - word_len
        elif orient == 3:  # Downward Diagonal
            ox = 1
            oy = 1
            endy = self._size - word_len
            endx = self._size - word_len
        x = choice(range(startx, endx))
        y = choice(range(starty, endy))
        return x, y, ox, oy

    def _check_board(self, word, x, y, ox, oy):
        for i, letter in enumerate(word):
            x_coord = x + i * ox
            y_coord = y + i * oy
            if self.board[y_coord][x_coord] != letter and self.board[y_coord][x_coord]:
                return False
        return True

    def _add_word(self, word):
        x, y, ox, oy = self._get_orientation(len(word))
        count = 0
        while not self._check_board(word, x, y, ox, oy):
            x, y, ox, oy = self._get_orientation(len(word))
            count += 1
            if count > 20000:
                return False
        self.solutions[word] = set()
        for i, letter in enumerate(word):
            x_coord = x + i * ox
            y_coord = y + i * oy
            self.board[y_coord][x_coord] = letter
            self.solutions[word].add((letter, x_coord, y_coord))
        return True

    def _fill_board(self):
        for i in range(self._size):
            for j in range(self._size):
                if not self.board[i][j]:
                    self.board[i][j] = choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def _init_board(self):
        for i in range(self._size):
            for j in range(self._size):
                self.board[i][j] = None

    def _fill_with_words(self):
        for word in self._words:
            if not self._add_word(word):
                return False
        return True

    def __len__(self):
        return self._size

    def __str__(self):
        return "\n".join([" ".join(row) for row in self.board])
