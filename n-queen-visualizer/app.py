import tkinter as tk
import time

class NQueensApp:
    def __init__(self, root):
        self.master = root
        self.master.title("N-Queens Visualizer")
        
        # --- CONFIGURATION ---
        self.board_size_px = 600 # Fixed screen size for the board
        self.speed = 0.05        # Default animation speed
        self.n = 8               # Default N
        self.running = False     # Flag to control the simulation
        
        # --- UI LAYOUT ---
        # 1. Control Panel Frame (Top)
        control_frame = tk.Frame(root, pady=10)
        control_frame.pack()

        # Label
        tk.Label(control_frame, text="Size:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

        # Slider (Scale)
        self.size_slider = tk.Scale(control_frame, from_=4, to=15, orient=tk.HORIZONTAL, command=self.reset_board)
        self.size_slider.set(8)
        self.size_slider.pack(side=tk.LEFT, padx=10)

        # Start Button
        self.start_btn = tk.Button(control_frame, text="Start", command=self.start_simulation, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=10)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        # Stop Button (Initially Disabled)
        self.stop_btn = tk.Button(control_frame, text="Stop", command=self.stop_simulation, bg="#f44336", fg="white", font=("Arial", 10, "bold"), width=10, state="disabled")
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # Status Label
        self.status_lbl = tk.Label(root, text="Ready", font=("Arial", 10, "italic"))
        self.status_lbl.pack()

        # 2. The Canvas (The Board)
        self.canvas = tk.Canvas(self.master, width=self.board_size_px, height=self.board_size_px, bg="white")
        self.canvas.pack(pady=10)
        
        # Initialize the grid
        self.reset_board()

    def reset_board(self, value=None):
        """ Clears the board and redraws the grid based on the slider value. """
        # Only allow resizing if NOT running
        if self.running:
            return

        # Get new size
        if value:
            self.n = int(value)
        else:
            self.n = self.size_slider.get()

        # Dynamic cell size
        self.cell_size = self.board_size_px // self.n

        # Clear and redraw
        self.canvas.delete("all")
        for r in range(self.n):
            for c in range(self.n):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = "white" if (r + c) % 2 == 0 else "#ddd"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", tags=f"cell-{r}-{c}")
        
        self.status_lbl.config(text=f"Board Size: {self.n}x{self.n}")

    def update_visual(self, row, col, color, text=""):
        """ Helper to update the GUI """
        self.canvas.itemconfig(f"cell-{row}-{col}", fill=color)
        self.canvas.delete(f"text-{row}-{col}")
        
        if text:
            font_size = int(self.cell_size * 0.5)
            x = col * self.cell_size + self.cell_size/2
            y = row * self.cell_size + self.cell_size/2
            self.canvas.create_text(x, y, text=text, font=("Arial", font_size, "bold"), tags=f"text-{row}-{col}")
        
        # Force redraw so we see the animation
        self.master.update()
        time.sleep(self.speed)

    def start_simulation(self):
        # UI Logic
        self.running = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.size_slider.config(state="disabled") # Lock slider
        self.status_lbl.config(text="Solving...", fg="blue")
        
        # Clean board but keep grid
        self.reset_board() 
        
        # Run Algorithm
        board = [-1] * self.n
        found = self.solve_queens(board, 0, self.n)
        
        # If we finished naturally (didn't click stop)
        if self.running:
            if found:
                self.status_lbl.config(text="Solution Found!", fg="green")
            else:
                self.status_lbl.config(text="No Solution Possible", fg="red")
            self.stop_simulation() # Reset buttons

    def stop_simulation(self):
        self.running = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.size_slider.config(state="normal") # Unlock slider
        
        if self.status_lbl.cget("text") == "Solving...":
             self.status_lbl.config(text="Cancelled by User", fg="orange")

    # --- RECURSIVE LOGIC ---

    def solve_queens(self, board, current, size):
        # 1. CHECK FOR CANCEL SIGNAL
        if not self.running:
            return False

        if current == size:
            return True
        
        for i in range(size):
            # Check cancel again inside loop for responsiveness
            if not self.running:
                return False

            board[current] = i
            
            # Visual: Thinking
            self.update_visual(current, i, "#ffeb3b", "?") 

            if self.no_conflicts(board, current):
                # Visual: Valid
                self.update_visual(current, i, "#81c784", "♕") 

                if self.solve_queens(board, current + 1, size):
                    return True
                
                # Visual: Backtracking
                self.update_visual(current, i, "#e57373", "X") 
                
            # Visual: Reset
            base_color = "white" if (current + i) % 2 == 0 else "#ddd"
            self.update_visual(current, i, base_color, "")

        return False

    def no_conflicts(self, board, current):
        for i in range(current):
            if board[i] == board[current]:
                return False
            if current - i == abs(board[current] - board[i]):
                return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("650x700") 
    app = NQueensApp(root)
    root.mainloop()