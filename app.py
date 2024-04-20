from flask import Flask, jsonify, request, render_template
import random

app = Flask(__name__)

def is_valid(board, row, col, num):
    # Check row
    if num in board[row]:
        return False
    
    # Check column
    for r in range(9):
        if board[r][col] == num:
            return False
    
    # Check 3x3 box
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False
    
    return True

def solve_sudoku(board):
    empty_cell = find_empty_cell(board)
    if not empty_cell:
        return True
    
    row, col = empty_cell
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    
    return False

def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def generate_sudoku():
    board = [[0 for _ in range(9)] for _ in range(9)]
    solve_sudoku(board)
    
    # Remove some numbers to create a puzzle
    for _ in range(45):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while board[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        board[row][col] = 0
    
    return board

def is_valid_solution(board):
    for i in range(9):
        for j in range(9):
            num = board[i][j]
            if num == 0:
                return False
            board[i][j] = 0
            if not is_valid(board, i, j, num):
                return False
            board[i][j] = num
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['GET'])
def api_generate():
    sudoku_board = generate_sudoku()
    return jsonify(sudoku_board)

@app.route('/api/solve', methods=['POST'])
def api_solve():
    data = request.json
    sudoku_board = data['board']
    solve_sudoku(sudoku_board)
    return jsonify({'solution': sudoku_board})

@app.route('/api/check', methods=['POST'])
def api_check():
    data = request.json
    sudoku_board = data['board']
    valid = is_valid_solution(sudoku_board)
    return jsonify({'valid': valid})

if __name__ == '__main__':
    app.run(debug=True)
