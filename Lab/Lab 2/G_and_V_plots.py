"""
Created on 16.10.2023
"""

import numpy as np
import matplotlib.pyplot as plt


# Parameters
T_hat_b_list = np.arange(0.4, 1, 0.1)  # boiling temperature
V_hat = np.linspace(0.35, 400, 500)  # V_hat >=  1/3, otherwise we get ln(negative number) in G_hat.

# Plotting parameters
scatter_size = 20
scatter_color = "gray"
plot_marker = "k:"
nrows = 3
ncols = 4
fig, axs = plt.subplots(nrows, ncols, figsize=(10, 6))
fig.suptitle("$\hat{G}(\hat{P})$ and $\hat{V}(\hat{P})$ of different $\hat{T}_b$ values")

i = 0
j = 0
for k, T_hat_b in enumerate(T_hat_b_list):
    if j >= ncols:
        i += 1
        j = 0

    # Expressions
    P_hat = 8 * T_hat_b / (3 * V_hat - 1) - 3 / V_hat**2
    G_hat = -8 / 3 * T_hat_b * np.log(3 * V_hat - 1) - 3 / V_hat + P_hat * V_hat

    # Plot G_hat(P_hat):
    ax1 = axs[i, j]
    ax1.scatter(P_hat, G_hat, scatter_size, color=scatter_color, facecolors="none")
    ax1.plot(P_hat, G_hat, plot_marker)
    ax1.set_title("$\hat{G}(\hat{P}), \hat{T}_p=$" + f"{T_hat_b:.1f}")
    ax1.set_xlabel("$\hat{P}$")
    ax1.set_ylabel("$\hat{G}$")
    ax1.grid(True)

    j += 1
    if j >= ncols:
        i += 1
        j = 0

    # Plot V_hat(P_hat):
    ax2 = axs[i, j]
    ax2.scatter(P_hat, V_hat, scatter_size, color=scatter_color, facecolors="none")
    ax2.plot(P_hat, V_hat, plot_marker)
    ax2.set_title("$\hat{V}(\hat{P}), \hat{T}_p=$" + f"{T_hat_b:.1f}")
    ax2.set_xlabel("$\hat{P}$")
    ax2.set_ylabel("$\hat{V}$")
    ax2.grid(True)

    j += 1

plt.tight_layout()
plt.show()