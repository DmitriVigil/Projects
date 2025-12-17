# N-Queens Backtracking Visualizer ♕

A real-time visualization of the classic **N-Queens** constraint satisfaction problem. This application demonstrates how **Recursive Backtracking** algorithms explore decision trees, identify conflicts, and prune invalid paths to find a solution.


## 🚀 Overview

The N-Queens puzzle is the problem of placing $N$ chess queens on an $N \times N$ chessboard so that no two queens attack each other. This project visualizes the computer's "thought process" as it attempts to solve the puzzle, offering a clear look at:
* **Recursion Depth:** How the algorithm dives into sub-problems.
* **Backtracking:** How it "undoes" a move when it hits a dead end.
* **State Management:** How the application handles user interruptions and dynamic resizing.

## ✨ Features

* **Dynamic Board Size:** User can adjust the board from $4 \times 4$ up to $15 \times 15$ via a slider.
* **Real-Time Visualization:**
    * 🟡 **Yellow:** Algorithm "thinking" (checking a cell).
    * 🟢 **Green:** Queen placed safely (for now).
    * 🔴 **Red:** Conflict detected or Backtracking triggered.
* **Interactive Controls:** Users can **Start** or **Stop/Cancel** the simulation at any time.
* **Responsive UI:** The grid and pieces resize automatically to fit the window.

## 🛠️ Technologies Used

* **Language:** Python 3.x
* **GUI Library:** Tkinter (Standard Python Library)
* **Concepts:** Recursion, Backtracking, Algorithm Complexity, Event-Driven Programming.

## ⚙️ Installation & Usage

### Prerequisites
You need **Python 3** installed on your machine. Tkinter is included with standard Python installations.

### Running the App
1.  Clone the repository:
    ```bash
    git clone [https://github.com/DmitriVigil/Projects.git](https://github.com/DmitriVigil/Projects.git)
    cd n-queens-visualizer
    ```

2.  Run the application:
    ```bash
    python nqueens.py
    ```
    *(Note: If `python` doesn't work, try `python3` or `py`).*

## 🧠 How the Algorithm Works

The application uses a **Recursive Backtracking** approach:

1.  **Place:** Attempt to place a queen in the current column of the current row.
2.  **Validate:** Check constraints (Vertical, Horizontal, and Diagonal attacks).
    * *If Valid:* Move to the next row (`row + 1`).
    * *If Invalid:* Try the next column in the current row.
3.  **Backtrack:** If all columns in the current row are tried and none work, return `False` to the previous row. The previous row then removes its queen and tries its next available column.

```python
# Pseudocode snippet
def solve(row):
    if row == size: return True
    for col in range(size):
        if is_safe(row, col):
            place_queen(row, col)
            if solve(row + 1): return True
            remove_queen(row, col) # Backtrack
    return False