"""
Created on 30.08.2023
"""

import numpy as np
import matplotlib.pyplot as plt


# Parameters
N = 100
q = 100
steps = int(1e4)

class Single_Oscillator_System:
    def __init__(self, N: int, q: int):
        """N = no. oscillators, q = total energy."""
        self.N = N
        self.q = q
        self.steps = None
        self.states = None
        self.end_state = None

        # Generate random initial microstate
        self.init_state = self.initialize_microstate()

    def initialize_microstate(self) -> np.ndarray[int]:
        """Returns a randomized microstate of oscillators' energies."""
        state = np.zeros(self.N)
        for q_i in range(self.q):  # Place each energy unit in a random oscillator
            ind = np.random.randint(0, self.N)
            state[ind] += 1
        return state

    def step(self, state: np.ndarray[int]) -> np.ndarray[int]:
        """Flips the microstate such that one random oscillator transfer one unit of energy to another random oscillator.
        If the donator-oscillators energy is zero, nothing happens."""
        # Select random donator-oscillator
        state_cp = state.copy()
        i = np.random.randint(0, self.N)
        if state_cp[i] == 0:
            return state_cp

        # Select random target-oscillator
        j = np.random.randint(0, self.N)

        # Donate
        state_cp[j] += 1
        state_cp[i] -= 1
        return state_cp

    def simulate(self, steps: int) -> np.ndarray[int]:
        states = np.zeros((steps, self.N))
        states[0, :] = self.init_state.copy()
        for i in range(steps-1):
            states[i+1, :] = self.step(states[i, :])
        self.steps = steps
        self.states = states
        self.end_state = states[-1, :]
        return states

    def plot_init_end_states(self, show=True, savefig=False):
        """Show/save a bar plot of the inital- and end microstates."""
        if self.end_state is None:  # simulation hasn't been run
            print("Simulation has not been run, run the simulate() method first")
            return
        fig = plt.figure()
        oscillators = range(self.N)

        plt.subplot(2,1,1)
        plt.bar(oscillators, self.init_state)
        plt.title("Initial")

        plt.subplot(2, 1, 2)
        plt.bar(oscillators, self.end_state)
        plt.title("End")

        fig.suptitle(f"Initial- and end microstates after {self.steps} steps.")
        fig.supxlabel("Oscillator #")
        fig.supylabel("Energy")
        plt.tight_layout()
        if savefig:
            if not isinstance(savefig, str):  # Default filename
                savefig = "oscillator_simulation_bar_plot.png"
            plt.savefig(savefig)
        if show:
            plt.show()

class Double_Oscillator_System(Single_Oscillator_System):
    def __init__(self, N_A: int, N_B: int, q: int):
        super().__init__(N_A+N_B, q)
        self.N_A = N_A
        self.N_B = N_B

    def plot_ratios(self, show=True, savefig=False):
        if self.end_state is None:  # simulation hasn't been run
            print("Simulation has not been run, run the simulate() method first")
            return
        time = range(self.steps)
        q_A = np.asarray([np.sum(self.states[i, :self.N_A]) for i in time])
        q_B = np.asarray([np.sum(self.states[i, self.N_B:]) for i in time])

        plt.plot( time, q_A/self.N_A, label="A")
        plt.plot( time, q_B/self.N_B, label="B")
        plt.xlabel("Step/time")
        plt.ylabel("$q_i/N_i$")
        plt.legend()
        if savefig:
            if not isinstance(savefig, str):  # Default filename
                savefig = "oscillator_simulation_ratios_time_plot.png"
            plt.savefig(savefig)
        if show:
            plt.show()



# Simulate
# single = Single_Oscillator_System(N, q)
# single.simulate(steps)
double = Double_Oscillator_System(N//2, int(np.ceil(N/2)), q)
double.simulate(steps)

# Plotting
# single.plot_init_end_states()
double.plot_ratios()
