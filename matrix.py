from sys import stdin
from copy import deepcopy


class MatrixError(BaseException):
    def __init__(self, Matrix, other):
        self.matrix1 = Matrix
        self.matrix2 = other


class Matrix:
    def __init__(self, __matrix: list):
        self.matrix = deepcopy(__matrix)

    def size(self):
        return len(self.matrix), len(self.matrix[0])

    def __str__(self):
        # string - итоговая матрица
        string = ''
        k = 0
        for matrix in self.matrix:
            if k != 0:
                string += '\n'
            current_string = '\t'.join(str(i) for i in matrix)
            string += current_string

            k += 1
        return string

    def __add__(self, other):
        if len(self.matrix) == len(other.matrix):
            for row in self.matrix:
                if len(row) != len(self.matrix[0]):
                    raise MatrixError(self, other)
            for row2 in other.matrix:
                if len(row2) != len(self.matrix[0]):
                    raise MatrixError(self, other)
            result = []
            sum_list = []
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[0])):
                    summa = other.matrix[i][j] + self.matrix[i][j]
                    sum_list.append(summa)
                    if len(sum_list) == len(self.matrix[0]):
                        result.append(sum_list)
                        sum_list = []
            return Matrix(result)
        else:
            raise MatrixError(self, other)

    def solve(self, other):
        for i in range(len(other)):
            self.matrix[i].append(other[i])
        w = 0
        for i in range(len(self.matrix)):
            while w < len(self.matrix[0]) and self.matrix[i][w] == 0:
                w += 1
            for j in range(i + 1, len(self.matrix)):
                past = self.matrix[j][w]
                for k in range(w, len(self.matrix[0])):
                    self.matrix[j][k] -= self.matrix[i][k] \
                                         * (past / self.matrix[i][w])
        while w < len(self.matrix[0]) \
                and self.matrix[len(self.matrix) - 1][w] == 0:
            w += 1
        if w == len(self.matrix[0]) - 1 or w < len(self.matrix[0]) - 2:
            raise MatrixError(self, self)
        for i in range(len(self.matrix) - 1, -1, -1):
            while w > -1 and self.matrix[i][w] == 0:
                w -= 1
            past = self.matrix[i][w]
            for j in range(w, len(self.matrix[0])):
                self.matrix[i][j] *= 1 / past
            for j in range(i - 1, -1, -1):
                past = self.matrix[j][w]
                for k in range(w, len(self.matrix[0])):
                    self.matrix[j][k] -= self.matrix[i][k] \
                                         * (past / self.matrix[i][w])
        ans = []
        for i in range(len(self.matrix)):
            ans.append(self.matrix[i][len(self.matrix[0]) - 1])
        return ans

    def __mul__(self, argument):
        if isinstance(argument, int) or isinstance(argument, float):
            result = []
            scalar_list = []
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[0])):
                    scalar_product = self.matrix[i][j] * argument
                    scalar_list.append(scalar_product)
                    if len(scalar_list) == len(self.matrix[0]):
                        result.append(scalar_list)
                        scalar_list = []
            return Matrix(result)
        else:
            rows_a = len(self.matrix)
            cols_a = len(self.matrix[0])
            rows_b = len(argument.matrix)
            cols_b = len(argument.matrix[0])

            if cols_a != rows_b:
                raise MatrixError(self, argument)

            result = [[0 for row in range(cols_b)] for col in range(rows_a)]

            for i in range(rows_a):
                for j in range(cols_b):
                    for k in range(rows_b):
                        result[i][j] += self.matrix[i][k] \
                                        * argument.matrix[k][j]
            return Matrix(result)

    __rmul__ = __mul__

    def transpose(self):
        list_ = zip(*self.matrix)
        transpose_matrix = list(list_)
        self.matrix = transpose_matrix
        return Matrix(transpose_matrix)

    def transposed(self):
        list_ = zip(*self.matrix)
        transposed_matrix = list(list_)
        return Matrix(transposed_matrix)


class SquareMatrix(Matrix):
    def __pow__(self, power):
        if power == 0:
            matrix = []
            for i in range(len(self.matrix)):
                line = []
                for j in range(len(self.matrix)):
                    if i == j:
                        line.append(1)
                    else:
                        line.append(0)
                matrix.append(line)
            return SquareMatrix(matrix)
        if power % 2 == 1:
            return self ** (power - 1) * self
        else:
            b = self ** (power // 2)
            return b * b


exec(stdin.read())
