import tkinter as tk
from tkinter import messagebox

# Constants for the game
ROWS = 6
COLUMNS = 7
EMPTY = " "
PLAYER_ONE = "X"
PLAYER_TWO = "O"

class ConnectFourGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect Four")
        self.root.configure(bg="#34495E")  # Set background color for the window

        # Set up the game board
        self.board = [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.current_player = PLAYER_ONE

        # Frame for player turn display
        self.turn_frame = tk.Frame(root, bg="#34495E")
        self.turn_frame.grid(row=0, column=0, columnspan=COLUMNS)

        self.turn_label = tk.Label(
            self.turn_frame, text="Player X's Turn", font=("Arial", 16, "bold"),
            fg="white", bg="#34495E"
        )
        self.turn_label.pack(pady=10)

        # Create the buttons and labels for the board
        self.buttons = [
            tk.Button(
                root, text=str(i + 1), font=("Arial", 12, "bold"), bg="#2980B9", fg="white",
                command=lambda c=i: self.make_move(c)
            ) for i in range(COLUMNS)
        ]
        for i, button in enumerate(self.buttons):
            button.grid(row=1, column=i, padx=2, pady=2)

        self.labels = [
            [
                tk.Label(
                    root, text=" ", width=10, height=5, borderwidth=2, relief="raised",
                    font=("Arial", 14), bg="#ECF0F1"
                ) for _ in range(COLUMNS)
            ] for _ in range(ROWS)
        ]
        for r in range(ROWS):
            for c in range(COLUMNS):
                self.labels[r][c].grid(row=r + 2, column=c, padx=2, pady=2)

    def make_move(self, column):
        """Handles the player's move when a column button is clicked."""
        if not self.is_valid_move(column):
            messagebox.showwarning("Invalid Move", "This column is full. Try a different column.")
            return

        # Place the player's piece in the selected column
        for row in reversed(range(ROWS)):
            if self.board[row][column] == EMPTY:
                self.board[row][column] = self.current_player
                self.labels[row][column].config(
                    text=self.current_player,
                    fg="red" if self.current_player == PLAYER_ONE else "blue",
                    bg="#F39C12" if self.current_player == PLAYER_ONE else "#8E44AD"
                )
                break

        # Check if the current player wins
        if self.check_winner(self.current_player):
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            self.reset_game()
            return

        # Check if the game is a draw
        if self.is_draw():
            messagebox.showinfo("Game Over", "The game is a draw!")
            self.reset_game()
            return

        # Switch to the other player
        self.current_player = PLAYER_TWO if self.current_player == PLAYER_ONE else PLAYER_ONE
        self.turn_label.config(
            text=f"Player {self.current_player}'s Turn",
            fg="red" if self.current_player == PLAYER_ONE else "blue"
        )

    def is_valid_move(self, column):
        """Checks if a move is valid (i.e., the column is not full)."""
        return self.board[0][column] == EMPTY

    def check_winner(self, player):
        """Checks if the given player has won the game."""
        # Check horizontal win
        for row in range(ROWS):
            for col in range(COLUMNS - 3):
                if all(self.board[row][col + i] == player for i in range(4)):
                    return True

        # Check vertical win
        for col in range(COLUMNS):
            for row in range(ROWS - 3):
                if all(self.board[row + i][col] == player for i in range(4)):
                    return True

        # Check positive diagonal win
        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                if all(self.board[row + i][col + i] == player for i in range(4)):
                    return True

        # Check negative diagonal win
        for row in range(3, ROWS):
            for col in range(COLUMNS - 3):
                if all(self.board[row - i][col + i] == player for i in range(4)):
                    return True

        return False

    def is_draw(self):
        """Checks if the game is a draw (i.e., the board is full)."""
        return all(self.board[0][col] != EMPTY for col in range(COLUMNS))

    def reset_game(self):
        """Resets the game board for a new game."""
        self.board = [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]
        for row in self.labels:
            for label in row:
                label.config(text=" ", bg="#ECF0F1")
        self.current_player = PLAYER_ONE
        self.turn_label.config(text="Player X's Turn", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    game = ConnectFourGUI(root)
    root.mainloop()