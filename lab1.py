import sys

import numpy as np


class TransportationProblem:
    def __init__(self, shops=None, warehouses=None, cost_matrix=None):
        self.cycles = 0

        if shops:
            self.shops = shops
        else:
            self.shops = list(map(int, input("Введите спрос через пробел: ").split()))

        if warehouses:
            self.warehouses = warehouses
        else:
            self.warehouses = list(map(int, input("Введите склады через пробел: ").split()))

        self.N, self.M = len(self.warehouses), len(self.shops)
        self.cost_matrix = []
        if cost_matrix:
            for row in cost_matrix:
                self.cost_matrix += row
        else:
            for i in range(self.N):
                while True:
                    row = list(
                        map(int,
                            input(f"Введите значения {i + 1}-й строки через пробел ({self.M} значений): ").split()))
                    if len(row) != self.M:
                        print(f"Ожидалось {self.M} значений, введено {len(row)}")
                    else:
                        break
                self.cost_matrix += row

        self.cost_matrix = np.array(self.cost_matrix).reshape(self.N, self.M)
        print("Полученная матрица:")
        np.savetxt(sys.stdout, self.cost_matrix, fmt="%3d")

        self.check_balance()

        self.table = [["-" for _ in range(self.M)] for _ in range(self.N)]
        self.U = ["-" for _ in range(self.N)]
        self.V = ["-" for _ in range(self.M)]

        if input(
                "Введите 1, если решить способом северо-зпадного угла, иначе задача будет решена методом минимального элмента: ") == "1":
            self.make_table_nw()
            self.U, self.V = self.solve_uv_nw(self.table, self.U, self.V)

            self.solve_nw(self.table, self.U, self.V, 0)
        # else:
        # self.make_table_me()

    def print_tabel(self):
        print(*self.table, sep="\n")

    def check_balance(self):
        if sum(self.shops) != sum(self.warehouses):
            print("Задача открытого типа, перевести к закрытому? (введите exit если нет)")
            if input() == "exit":
                sys.exit()
            else:
                self.make_close()
        else:
            print("Задача открытого типа")

    def make_close(self):
        if self.N < self.M:
            self.N += 1
            self.cost_matrix = np.vstack((self.cost_matrix, np.zeros((1, self.M))))
            self.warehouses.append(0)
        else:
            self.M += 1
            self.cost_matrix = np.hstack((self.cost_matrix, np.zeros((self.N, 1))))
            self.shops.append(0)

        print("Результат приведения к закрытому типу:")
        np.savetxt(sys.stdout, self.cost_matrix, fmt="%3d")

    def make_table_nw(self):
        for i in range(self.N):
            for j in range(self.M):
                potential_elem = min(self.warehouses[i], self.shops[j])
                if potential_elem:
                    self.table[i][j] = potential_elem
                    self.warehouses[i] -= potential_elem
                    self.shops[j] -= potential_elem

        self.print_tabel()

    # def check_ready(self) -> bool:
    #     for i in range(self.N):
    #         for j in range(self.M):
    #             if self.table[i][j] == "-":
    #                 if self.U[i] + self.V[j] > self.cost_matrix[i][j]:
    #                     return False
    #     print("Задача решена")
    #     return True

    # def solve_uv_nw(self):
    #     for i in range(self.N):
    #         if self.table[i].count("-") == self.M - 1:
    #             self.U[i] = 0
    #     while self.U.count("-") or self.V.count("-"):
    #         for i in range(self.N):
    #             for j in range(self.M):
    #                 if self.table[i][j] != "-" and (self.U[i] != "-" or self.V[j] != "-"):
    #                     if self.U[i] != "-":
    #                         self.V[j] = self.cost_matrix[i][j] - self.U[i]
    #                     else:
    #                         self.U[i] = self.cost_matrix[i][j] - self.V[j]

    def solve_uv_nw(self, table, U, V) -> (list, list):
        for i in range(self.N):
            if table[i].count("-") == self.M - 1:
                U[i] = 0
        while U.count("-") or V.count("-"):
            for i in range(self.N):
                for j in range(self.M):
                    if table[i][j] != "-" and (U[i] != "-" or V[j] != "-"):
                        if U[i] != "-":
                            V[j] = self.cost_matrix[i][j] - U[i]
                        else:
                            U[i] = self.cost_matrix[i][j] - V[j]

        return U, V

    def find_cycles(self, table, U, V, i_start, j_start, cycles) -> bool:
        ...


    def solve_nw(self, table, U, V, cycles):
        for i in range(self.N):
            for j in range(self.M):
                if table[i][j] == "-":
                    if U[i] + V[j] > self.cost_matrix[i][j]:
                        self.find_cycles(table, U, V, i, j, cycles)





shops = [7, 8, 4, 11, 30]
warehouses = [16, 12, 14, 18]
cost_matrix = [[25, 28, 20, 15, 7], [25, 5, 11, 23, 10], [1, 25, 14, 16, 16], [8, 6, 4, 16, 18]]
tr1 = TransportationProblem(shops, warehouses, cost_matrix)
