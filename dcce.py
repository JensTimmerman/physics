import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

# ============================================================
# DOUBLE-COVER CRITICALITY EXPLORATION
# ============================================================

# ------------------------------------------------------------
# Core geometry
# ------------------------------------------------------------

rho_c = np.sqrt(2)

rho = np.linspace(0.01, 3.0, 5000)

# Exact Koide functional
Q = 1/3 + rho**2 / 6

# Resonance enhancement
resonance = np.exp(-8 * (rho**2 / 2 - 1)**2)

# Criticality pole
criticality = 1 / (np.abs(rho**2 / 2 - 1) + 1e-6)

# Localization estimate
localization = 1 / (1 + rho**2)

# Participation estimate
participation = 1 / localization

# ------------------------------------------------------------
# Critical exponent exploration
# ------------------------------------------------------------

# Distance from critical point
delta = np.abs(rho - rho_c)

# Ignore exact singularity
mask = (delta > 1e-3) & (delta < 0.3)

x = delta[mask]
y = criticality[mask]

# Power law fit
def powerlaw(x, A, gamma):
    return A * x**(-gamma)

params, _ = curve_fit(powerlaw, x, y, p0=[1.0, 1.0])

A_fit, gamma_fit = params

fit_curve = powerlaw(x, A_fit, gamma_fit)

# ------------------------------------------------------------
# Orbit geometry
# ------------------------------------------------------------

phi = np.linspace(0, 4*np.pi, 4000)

def orbit_density(phi, rho):
    return (1 + rho * np.cos(phi))**2

dens_1 = orbit_density(phi, 1.0)
dens_c = orbit_density(phi, rho_c)
dens_2 = orbit_density(phi, 2.0)

# ------------------------------------------------------------
# Node structure
# ------------------------------------------------------------

def node_positions(rho):

    if rho < 1:
        return []

    val = -1 / rho

    if np.abs(val) > 1:
        return []

    phi0 = np.arccos(val)

    return [
        phi0,
        2*np.pi - phi0,
        2*np.pi + phi0,
        4*np.pi - phi0
    ]

nodes_1 = node_positions(1.0)
nodes_c = node_positions(rho_c)
nodes_2 = node_positions(2.0)

# ------------------------------------------------------------
# Plotting
# ------------------------------------------------------------

fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# ============================================================
# Q functional
# ============================================================

axs[0,0].plot(rho, Q, linewidth=2)
axs[0,0].axvline(rho_c, linestyle='--')
axs[0,0].axhline(2/3, linestyle=':')
axs[0,0].set_title("Exact Koide Functional")
axs[0,0].set_xlabel(r'$\rho$')
axs[0,0].set_ylabel(r'$Q(\rho)$')

# ============================================================
# Criticality
# ============================================================

axs[0,1].plot(rho, criticality, linewidth=2)
axs[0,1].axvline(rho_c, linestyle='--')
axs[0,1].set_ylim(0, 50)
axs[0,1].set_title("Criticality Divergence")
axs[0,1].set_xlabel(r'$\rho$')
axs[0,1].set_ylabel("Criticality")

# ============================================================
# Critical exponent fit
# ============================================================

axs[1,0].loglog(x, y, '.', markersize=3, label='Data')
axs[1,0].loglog(
    x,
    fit_curve,
    linewidth=2,
    label=fr'Fit: $\gamma={gamma_fit:.3f}$'
)

axs[1,0].set_title("Critical Exponent Scaling")
axs[1,0].set_xlabel(r'$|\rho-\sqrt{2}|$')
axs[1,0].set_ylabel("Criticality")
axs[1,0].legend()

# ============================================================
# Orbit density
# ============================================================

axs[1,1].plot(phi, dens_1, label=r'$\rho=1$')
axs[1,1].plot(phi, dens_c, label=r'$\rho=\sqrt{2}$')
axs[1,1].plot(phi, dens_2, label=r'$\rho=2$')

for n in nodes_c:
    axs[1,1].axvline(n, linestyle=':', alpha=0.5)

axs[1,1].set_title("Double-Cover Orbit Density")
axs[1,1].set_xlabel(r'$\phi$')
axs[1,1].set_ylabel(r'$m(\phi)$')
axs[1,1].legend()

plt.tight_layout()
plt.show()

# ============================================================
# PRINT RESULTS
# ============================================================

print()
print("=" * 60)
print("CRITICAL SCALING RESULTS")
print("=" * 60)

print()
print(f"Critical rho        = {rho_c:.12f}")
print(f"Koide value         = {2/3:.12f}")

print()
print(f"Critical exponent γ = {gamma_fit:.6f}")

print()
print("Interpretation:")
print("- γ ≈ 1 suggests simple pole criticality")
print("- Divergence occurs exactly at equipartition")
print("- Koide point corresponds to critical orbit geometry")

print()
print("=" * 60)
print("NODE STRUCTURE")
print("=" * 60)

print()
print(f"rho = 1")
print(nodes_1)

print()
print(f"rho = sqrt(2)")
print(nodes_c)

print()
print(f"rho = 2")
print(nodes_2)
