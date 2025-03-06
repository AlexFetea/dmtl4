#Minesweeper solver

"""
(a) Problem:  
This script creates a random Minesweeper board, then computes the values for the clues, and finally solves the game using Z3. The solver finds mine locations based on the constraints.

(b) Formalization in Z3:
Every cell is Boolean. For every non-mine cell we make sure that the number of mines surrounding matches the clue number. The Z3 solver finds valid solutions, but skips the mine cells which are -1.

(c) Experience:
Setting up the board and input was trivial, but placing the rules in Z3 logical contstraints was much harder. required careful indexing and handling of neighbors.  
"""

import random
from z3 import Bool, Solver, Sum, If, sat

# Board size and number of mines
num_rows = 10
num_cols = 10
num_mines = 6
board = [[0] * num_cols for _ in range(num_rows)]
mine_positions = set()

# Randomly place mines
while len(mine_positions) < num_mines:
    random_row = random.randint(0, num_rows - 1)
    random_col = random.randint(0, num_cols - 1)
    if (random_row, random_col) not in mine_positions:
        mine_positions.add((random_row, random_col))
        board[random_row][random_col] = -1  

for row_index in range(num_rows):
    for col_index in range(num_cols):
        if board[row_index][col_index] == -1:
            continue
        mine_count = 0
        for row_offset, col_offset in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            neighbor_row = row_index + row_offset
            neighbor_col = col_index + col_offset
            if (neighbor_row, neighbor_col) in mine_positions:
                mine_count += 1
        board[row_index][col_index] = mine_count  

# Z3 solver
mine_variables = [[Bool(f"mine_at_{row_index}_{col_index}") for col_index in range(num_cols)] for row_index in range(num_rows)]
solver = Solver()

for row_index in range(num_rows):
    for col_index in range(num_cols):
        if board[row_index][col_index] >= 0:
            neighbor_mine_conditions = []
            for row_offset, col_offset in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                neighbor_row = row_index + row_offset
                neighbor_col = col_index + col_offset
                if 0 <= neighbor_row < num_rows and 0 <= neighbor_col < num_cols:
                    neighbor_mine_conditions.append(If(mine_variables[neighbor_row][neighbor_col], 1, 0))
            solver.add(Sum(neighbor_mine_conditions) == board[row_index][col_index])  

# Solve
solver_output = None
if solver.check() == sat:
    model = solver.model()
    solver_output = []
    for row_index in range(num_rows):
        solver_output.append([])
        for col_index in range(num_cols):
            solver_output[row_index].append(1 if model.evaluate(mine_variables[row_index][col_index], model_completion=True) else 0)

print("\nGenerated Board:")
for row in board:
    print(row)

if solver_output:
    print("\nSolver Output:")
    for row in solver_output:
        print(row)

    # Verify correctness
    is_solver_correct = True
    for row_index in range(num_rows):
        for col_index in range(num_cols):
            if solver_output[row_index][col_index] == 1 and (row_index, col_index) not in mine_positions:
                is_solver_correct = False
            if solver_output[row_index][col_index] == 0 and (row_index, col_index) in mine_positions:
                is_solver_correct = False
    if is_solver_correct:
        print("\nSolver Correct")
    else:
        print("\nSolver Incorrect")
else:
    print("\nNo valid solution")
    
    

