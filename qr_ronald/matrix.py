from typing import List

QR_SIZE = 21  # Version 1 QR size

def empty_matrix() -> List[List[int]]:
    """Create an empty 21x21 matrix filled with zeros."""
    return [[0 for _ in range(QR_SIZE)] for _ in range(QR_SIZE)]


def place_finder_pattern(matrix, row, col):
    """Place a 7x7 finder pattern at (row, col)."""
    pattern = [
        [1,1,1,1,1,1,1],
        [1,0,0,0,0,0,1],
        [1,0,1,1,1,0,1],
        [1,0,1,1,1,0,1],
        [1,0,1,1,1,0,1],
        [1,0,0,0,0,0,1],
        [1,1,1,1,1,1,1],
    ]
    for r in range(7):
        for c in range(7):
            matrix[row + r][col + c] = pattern[r][c]


def add_finder_patterns(matrix):
    """Add the three required finder patterns for Version 1 QR."""
    # Top-left
    place_finder_pattern(matrix, 0, 0)
    # Top-right
    place_finder_pattern(matrix, 0, QR_SIZE - 7)
    # Bottom-left
    place_finder_pattern(matrix, QR_SIZE - 7, 0)

def add_timing_patterns(matrix):
    """Add timing patterns to the QR matrix."""

    # Horizontal timing pattern (row 6, columns 8 to 20)
    for col in range(8, QR_SIZE):
        matrix[6][col] = (col % 2)

    # Vertical timing pattern (column 6, rows 8 to 20)
    for row in range(8, QR_SIZE):
        matrix[row][6] = (row % 2)
