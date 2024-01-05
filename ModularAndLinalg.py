import numpy as np
import math

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

##def extendedEuclidean(a: int, b: int) -> tuple[int, int, int]:
##    """
##    Implementation of the extended Euclidean algorithm
##    """
##    if a == 0:
##        return b, 0, 1
##    else:
##        gcd, x1, y1 = extendedEuclidean(b % a, a)
##        x = y1 - (b // a) * x1
##        y = x1
##        return gcd, x, y
##
##def inverseMod(n: int, m: int) -> int:
##    """
##    Returns the modular inverse of an integer n mod m
##    """
##    gcd, x, y = extendedEuclidean(n, m)
##    if gcd != 1:
##        return None  
##    else:
##        return x % m
##
##def isMatrixInvertibleModN(arr: np.ndarray, m: int) -> bool:
##    """
##    Returns if a matrix is invertible mod an integer m, namely, if the determinant of the array is coprime with m
##    """
##    det = getPreciseDeterminant(arr)
##    return math.gcd(det, m) == 1
##
##def matrixInverseModN(arr: np.ndarray, m: int) -> np.ndarray:
##    """
##    Returns the inverse of a matrix mod n
##    """
##    det = getPreciseDeterminant(arr) % m
##    detInv = inverseMod(det, m)
##
##    cofactorMatrix = np.linalg.inv(arr).T * det
##    adjugateMatrix = np.round(cofactorMatrix).astype(int).T
##
##    return (adjugateMatrix * detInv) % m
