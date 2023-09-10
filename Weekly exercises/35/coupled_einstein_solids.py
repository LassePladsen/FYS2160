"""
Created on 30.08.2023
"""

from math import factorial

import matplotlib.pyplot as plt

# Parameters
N_A = 50
N_B = N_A
q = 100


def einstein_multiplicity(N: int, q: int):
    return factorial(N + q - 1) / (factorial(q) * factorial(N - 1))


class Coupled_Einstein_Solids:
    def __init__(self, N_A: int, N_B: int, q: int):
        self.N_A = N_A
        self.N_B = N_B
        self.q = q

        # calculate total multiplicity (omega) for all macrostates of given values N_A, N_B, and q:
        self.omega_all = 0
        for q_A in range(self.q + 1):
            self.omega_all += self.omega_total(q_A)

    def check_valid_q(self, q_A: int):
        if q_A < 0:
            raise ValueError(f"q_A must be a non-negative integer, given q_A = {q_A} and self.q = {self.q}")
        if q_A > self.q:
            raise ValueError(f"q_A must be less than or equal to q, given q_A = {q_A} and self.q = {self.q}")
        if not isinstance(q_A, int):
            raise ValueError(f"q_A must be an integer, given q_A = {q_A}")

    def omega_a(self, q_A: int):
        self.check_valid_q(q_A)
        return einstein_multiplicity(self.N_A, q_A)

    def omega_b(self, q_A: int):
        self.check_valid_q(q_A)
        return einstein_multiplicity(self.N_B, self.q - q_A)

    def omega_total(self, q_A: int):
        return self.omega_a(q_A) * self.omega_b(q_A)

    def probability(self, q_A: int):
        return self.omega_total(q_A) / self.omega_all

    def probability_plot(self, show=True, savefig=False):
        P_list = []
        q_A_list = list(range(0, self.q + 1))
        for q_A in q_A_list:
            P_list.append(self.probability(q_A) * 100)

        # Plot
        plt.plot(q_A_list, P_list)
        plt.xlabel("$q_A$")
        plt.ylabel("$P(q_A)$ [%]")
        plt.title(f"Probability plot. q = {self.q}, $N_A$ = {self.N_A}, $N_A$ = {self.N_A}.")
        if savefig:
            if not isinstance(savefig, str):  # Default filename
                savefig = "coupled_einstein_probability_plot.png"
            plt.savefig(savefig)
        if show:
            plt.show()


inst = Coupled_Einstein_Solids(N_A, N_B, q)

# Exercises
print(f"Exercise o) P(q_a=0) = {inst.probability(0) * 100:g} %")

# Probability plot
inst.probability_plot()
