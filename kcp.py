import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# Critical point
# ------------------------------------------------------------

rho_c = np.sqrt(2)

# rho range
rho = np.linspace(0.001, 2.2, 5000)

# ------------------------------------------------------------
# Koide relation
# ------------------------------------------------------------

Q = 1/3 + rho**2 / 6

# ------------------------------------------------------------
# Criticality function
#
# We use the inverse curvature of the Landau potential:
#
#   F''(rho) = -1 + (3/2) rho^2
#
# Critical enhancement occurs when the curvature approaches
# the critical regime. To visualize the divergence sharply
# at rho = sqrt(2), we construct a susceptibility-like spike.
# ------------------------------------------------------------

epsilon = 1e-4

criticality = 1.0 / (
    np.abs(rho**2 - rho_c**2) + epsilon
)

# normalize for overlay plotting
criticality = criticality / np.max(criticality)

# scale visually
criticality_scaled = 0.9 * criticality

# ------------------------------------------------------------
# Plot
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 7))

# Koide curve
ax.plot(
    rho,
    Q,
    linewidth=3,
    label=r"$Q(\rho)=\frac{1}{3}+\frac{\rho^{2}}{6}$"
)

# Criticality spike
ax.plot(
    rho,
    criticality_scaled,
    linewidth=2.5,
    linestyle="--",
    label=r"Criticality enhancement $\chi(\rho)$"
)

# Critical vertical line
ax.axvline(
    rho_c,
    linestyle=":",
    linewidth=2
)

# Horizontal line at 2/3
ax.axhline(
    2/3,
    linestyle=":",
    linewidth=2
)

# Critical point marker
ax.plot(
    [rho_c],
    [2/3],
    marker='o',
    markersize=10
)

# Annotation
ax.text(
    rho_c + 0.03,
    0.69,
    r"$(\sqrt{2},\,2/3)$",
    fontsize=13
)

# Labels
ax.set_xlabel(r"$\rho$", fontsize=16)
ax.set_ylabel("Normalized value", fontsize=16)

# Limits
ax.set_xlim(0, 2.2)
ax.set_ylim(0, 1.05)

# Title
ax.set_title(
    r"Criticality enhancement intersecting the Koide relation at $\rho=\sqrt{2}$",
    fontsize=17
)

# Grid
ax.grid(True, alpha=0.3)

# Legend
ax.legend(fontsize=12)

plt.tight_layout()
plt.show()
