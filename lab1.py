import sys
from sys import setrecursionlimit

import numpy as np

setrecursionlimit(1000000)


class TransportationProblem:
    def __init__(self, shops=None, warehouses=None, cost_matrix=None):
        self.best_cycles_count = 10 ** 99
        self.best_len_all_cycles = 10 ** 99
        self.best_way = []

        self.cycles = []

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
            U, V = self.solve_uv_nw(self.table, self.U, self.V)
            print(self.V, self.U)
            print(self.table)

            self.solve_nw(self.table, U, V, [])
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

    def find_cycles(self, table, cycle, sign):
        i, j = cycle[-1]
        j -= 1
        if sign == "+":
            while j > -1:
                if table[i][j] != "-" and [i, j] not in cycle[1:]:
                    self.find_cycles(table, cycle + [[i, j]], "-")
                j -= 1
            i, j = cycle[-1]
            j += 1
            while j != self.M:
                if table[i][j] != "-" and [i, j] not in cycle[1:]:
                    self.find_cycles(table, cycle + [[i, j]], "-")
                j += 1
        elif sign == "-":
            while i > -1:
                if [i, j] == cycle[0]:
                    self.cycles += [cycle]
                if table[i][j] != "-" and [i, j] not in cycle:
                    self.find_cycles(table, cycle + [[i, j]], "+")
                i -= 1
            i, j = cycle[-1]
            i += 1
            while i != self.N:
                if [i, j] == cycle[0]:
                    self.cycles += [cycle]
                if table[i][j] != "-" and [i, j] not in cycle:
                    self.find_cycles(table, cycle + [[i, j]], "-")
                i += 1

    def solve_nw(self, table, U, V, last_cycles):
        self.cycles = []
        for i in range(self.N):
            for j in range(self.M):
                if table[i][j] == "-":
                    if U[i] + V[j] > self.cost_matrix[i][j]:
                        self.find_cycles(table, [[i, j]], "+")

        if not self.cycles:
            len_last_cycles = len(last_cycles)
            len_all_steps_last_cycles = sum(map(len, last_cycles))

            if len_last_cycles < self.best_cycles_count:
                self.best_cycles_count = len_last_cycles
                self.best_len_all_cycles = len_all_steps_last_cycles
                self.best_way = last_cycles

            if len_last_cycles == self.best_cycles_count:
                if len_all_steps_last_cycles < self.best_len_all_cycles:
                    self.best_cycles_count = len_last_cycles
                    self.best_len_all_cycles = len_all_steps_last_cycles
                    self.best_way = last_cycles

        for cycle in self.cycles:
            new_table = table[:]
            min_elem = min(table[i][j] for i, j in cycle[1::2])
            for i, j in cycle[1::2]:
                new_table[i][j] -= min_elem
                if new_table[i][j] == 0:
                    new_table[i][j] = "-"
            for i, j in cycle[::2]:
                if new_table[i][j] == "-":
                    new_table[i][j] = min_elem
                else:
                    new_table[i][j] += min_elem
            U_new, V_new = self.solve_uv_nw(new_table, self.U, self.V)
            self.solve_nw(new_table, U_new, V_new, cycle)


shops = [7, 8, 4, 11, 30]
warehouses = [16, 12, 14, 18]
cost_matrix = [[25, 28, 20, 15, 7], [25, 5, 11, 23, 10], [1, 25, 14, 16, 16], [8, 6, 4, 16, 18]]
tr1 = TransportationProblem(shops, warehouses, cost_matrix)
