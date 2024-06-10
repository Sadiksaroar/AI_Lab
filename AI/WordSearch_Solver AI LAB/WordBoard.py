import tkinter as tk
import tkinter.font as tkFont
from os import listdir, getcwd
from random import choice
from functools import partial
from WordSearch import WordSearch

class WordBoard:
    def __init__(self, size=20, color="yellow", file_name="words.txt", words=None):
        try:
            assert size > 3, "Size must be greater than 3"
            
            self._root = tk.Tk()
            self._root.title("Word Search")
            self._root.resizable(width=False, height=False)

            self._word_grid = tk.Frame(self._root)
            self._word_list = tk.Frame(self._root)
            self._button_frame = tk.Frame(self._root)
            self._menu = tk.Frame(self._button_frame)

            self._solution_shown = False
            self._size = size
            self._color = color

            new_words_button = tk.DISABLED
            if file_name in listdir(getcwd()):
                new_words_button = tk.NORMAL
                with open(file_name, mode="r") as f:
                    self._wordstxt = list(filter(None, f.read().split("\n")))
                    self._wordstxt = list(
                        filter(lambda x: len(x) < self._size - 3, self._wordstxt)
                    )
            elif words is None:
                raise FileNotFoundError(
                    f"""{file_name} not present in the current directory. {file_name}
                                        must contain words separated by newline (\\n) characters."""
                )

            self._pushed = set()

            self._words = words
            if self._words is None:
                self._choose_random_words()
            else:
                self._words = list(set(map(str.upper, self._words)))

            self._buttons = []
            for i in range(self._size):
                row = []
                for j in range(self._size):
                    row.append(
                        tk.Button(
                            self._word_grid, padx=5, command=partial(self._pressed, i, j)
                        )
                    )
                    row[-1].grid(row=i, column=j, sticky="ew", padx=0, pady=0)
                self._buttons.append(row)

            tk.Button(
                self._menu, text="Solution", padx=1, pady=1, bg="green", command=self._solution
            ).grid(row=1, column=0, sticky="ew", padx=5)
            tk.Button(
                self._menu, text="Reshuffle", padx=1, pady=1, bg="lightblue", command=self._reshuffle
            ).grid(row=1, column=1, sticky="ew", padx=5)
            tk.Button(
                self._menu,
                text="New Words",
                padx=1,
                pady=1,
                bg="lightgreen",
                state=new_words_button,
                command=self._select_new,
            ).grid(row=1, column=2, sticky="ew", padx=5)
            tk.Button(
                self._menu, text="Exit", padx=1, pady=1, bg="red", command=self._exit
            ).grid(row=1, column=3, sticky="ew", padx=5)

            self._labels = {}
            self._word_search = None
            self._create_labels()
            self._reshuffle()

            self._word_grid.pack(side=tk.TOP, pady=20)
            self._word_list.pack(side=tk.TOP, pady=20)
            self._button_frame.pack(side=tk.TOP, pady=20)
            self._menu.pack(side=tk.TOP)

            tk.mainloop()
        
        except AssertionError as e:
            print(f"Initialization error: {e}")
        except FileNotFoundError as e:
            print(f"File error: {e}")
        except tk.TclError as e:
            print(f"Tkinter error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def _create_labels(self):
        for label in self._labels.values():
            label.destroy()
        self._labels.clear()
        self._labels = {
            "Words": tk.Label(
                self._word_list, text="Words", pady=5, font=tkFont.Font(weight="bold")
            )
        }
        self._labels["Words"].grid(row=0, column=0, columnspan=2, sticky="ew")
        for i, word in enumerate(sorted(self._words)):
            self._labels[word] = tk.Label(self._word_list, text=word, anchor="w")
            self._labels[word].grid(
                row=(i // 2) + (i % 1) + 1, column=i % 2, sticky="W"
            )

    def _choose_random_words(self):
        self._words = set()
        for _ in range(choice(range(self._size // 3, self._size))):
            self._words.add(choice(self._wordstxt).upper())
        self._words = list(self._words)

    def _pressed(self, row, col):
        if self._buttons[row][col].cget("bg") == self._color:
            self._buttons[row][col].configure(bg="lightgrey")
            self._pushed.remove((self._buttons[row][col].cget("text"), col, row))
        else:
            self._buttons[row][col].configure(bg=self._color)
            self._pushed.add((self._buttons[row][col].cget("text"), col, row))
            for word, coords in self._word_search.solutions.items():
                if coords & self._pushed == coords:
                    for _, col, row in coords:
                        self._buttons[row][col].configure(state=tk.DISABLED)
                    self._labels[word].configure(bg=self._color)

    def _exit(self):
        self._root.destroy()

    def _solution(self):
        if self._solution_shown:
            bg = "lightgrey"
            state = tk.NORMAL
            self._pushed.clear()
        else:
            bg = self._color
            state = tk.DISABLED

        self._solution_shown = not self._solution_shown
        for word, coords in self._word_search.solutions.items():
            self._labels[word].configure(bg=bg)
            for _, col, row in coords:
                self._buttons[row][col].configure(state=state, bg=bg)

    def _reshuffle(self):
        if self._solution_shown:
            self._solution_shown = not self._solution_shown
        self._word_search = WordSearch(self._size, self._words)
        self._pushed.clear()

        for i in range(self._size):
            for j in range(self._size):
                self._buttons[i][j].configure(
                    text=self._word_search.board[i][j],
                    bg="lightgrey",
                    state=tk.NORMAL,
                )

        for label in self._labels.values():
            label.configure(bg="lightgrey")

    def _select_new(self):
        self._choose_random_words()
        self._reshuffle()
        self._create_labels()

# Test initialization
word_board = WordBoard()
