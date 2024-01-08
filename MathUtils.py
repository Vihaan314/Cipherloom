import numpy as np
import math

"""
General
"""

def rearrangeRow(arr: np.ndarray, row: int, key: list[int]) -> np.ndarray:
    """
    Rearranges row of numpy array given order as list of integers
    """
    return [arr[row, i] for i in key]

def rearrangeColumn(arr: np.ndarray, column: int, key: list[int]) -> np.ndarray:
    """
    Rearranges column of numpy array given order as list of integers
    """
    return [arr[i, column] for i in key]

def toSquareMatrix(arr: list[list[int]], oneDim = False) -> np.ndarray:
    """
    Converts default list to numpy square array
    """
    length = int(math.sqrt(len(arr))) if oneDim else len(arr)
    return np.array(arr).reshape(length, length)

"""
End of general
"""

"""
Number theory and linear algebra
"""

def extendedEuclidean(a, b):
    """
    Implementation of Euclidean Algorithm
    """
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extendedEuclidean(b % a, a)
        return gcd, y - (b // a) * x, x

def inverseMod(a, m):
    """
    The modular inverse of integer a mod m
    """
    gcd, x, y = extendedEuclidean(a, m)
    if gcd != 1:
        raise Exception("Modular inverse does not exist")
    else:
        return x % m

def minor(matrix, i, j):
    """
    Returns the minor of matrix[i][j]
    """
    return [row[:j] + row[j+1:] for row in (matrix[:i] + matrix[i+1:])]

def cofactorMatrix(matrix):
    """
    Returns the cofactor of a matrix
    """
    if len(matrix) == 2:
        return [[matrix[1][1], -matrix[1][0]], [-matrix[0][1], matrix[0][0]]]

    cofactorMat = []
    for i in range(len(matrix)):
        cofactorRow = []
        for j in range(len(matrix)):
            minorDet = determinant(minor(matrix, i, j))
            cofactorRow.append(((-1) ** (i + j)) * minorDet)
        cofactorMat.append(cofactorRow)
    return cofactorMat

def adjugateMatrix(matrix):
    """
    Computes the adjugate of a matrix
    """
    cofactorMat = cofactorMatrix(matrix)
    return [list(row) for row in zip(*cofactorMat)]

def determinant(matrix):
    """
    Calculates the determinant of a matrix
    """
    if len(matrix) == 2:
        return (matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0])

    det = 0
    for c in range(len(matrix)):
        det += ((-1)**c) * matrix[0][c] * determinant(minor(matrix, 0, c))
    return det 

def isMatrixInvertibleModN(matrix, m: int) -> bool:
    """
    Returns if a matrix is invertible mod an integer m, namely, if the determinant of the array is coprime with m
    """
    det = determinant(matrix)
    return math.gcd(det, 26) == 1

def matrixInverseModN(matrix, mod):
    """
    Returns the inverse of a matrix modulo mod
    """
    det = determinant(matrix) % 26
    detInv = inverseMod(det, mod)
    adj = adjugateMatrix(matrix)
    return [[(detInv * adj[i][j]) % mod for j in range(len(matrix))] for i in range(len(matrix))]

"""
End of number theory and linear algebra
"""
