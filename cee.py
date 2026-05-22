"""
Critical Equipartition Explorer
===============================

Goal
----
Explore whether the Koide point

    Q = 2/3

emerges naturally as a critical point where:

    modulation energy
        =
    homogeneous background energy

on a double-covered spinorial orbit.

Core hypothesis
----------------
The orbit amplitude is:

    sqrt(m(phi)) = mu * (1 + rho cos(phi))

Then:

    m(phi) = mu^2 (1 + 2 rho cos(phi) + rho^2 cos^2(phi))

Orbit averaging gives:

    <m> = mu^2 (1 + rho^2 / 2)

Therefore:

    background energy  = 1
    modulation energy  = rho^2 / 2

Critical equipartition:

    rho^2 / 2 = 1
        -> rho = sqrt(2)

which predicts:

    Q = 1/3 + rho^2 / 6 = 2/3

This script explores whether:
    - stability,
    - entropy,
    - resonance,
    - localization,
    - bifurcation behavior

all become special near rho = sqrt(2).
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PARAMETERS
# ============================================================

NPHI = 4000
NRHO = 1200

RHO_MAX = 3.0

# nonlinear coupling
K = 0.45

# dissipation
GAMMA = 0.08

# noise
NOISE = 0.0005

# ============================================================
# ORBIT
# ============================================================

phi = np.linspace(0,4*np.pi,NPHI)

# ============================================================
# HELPERS
# ============================================================

def normalize(x):

    s = np.sum(x)

    if s < 1e-12:
        return x

    return x / s

# ------------------------------------------------------------

def Q_of_rho(rho):

    return 1/3 + rho**2 / 6

# ------------------------------------------------------------

def orbit_density(rho):

    psi = 1 + rho*np.cos(phi)

    m = psi**2

    return normalize(m)

# ------------------------------------------------------------

def entropy(m):

    return -np.sum(
        m*np.log(m + 1e-12)
    )

# ------------------------------------------------------------

def participation(m):

    return 1 / np.sum(m**2)

# ------------------------------------------------------------

def localization(m):

    return np.max(m)

# ------------------------------------------------------------

def modulation_energy(rho):

    return rho**2 / 2

# ------------------------------------------------------------

def background_energy():

    return 1.0

# ------------------------------------------------------------

def free_energy(rho):

    """
    Effective free-energy ansatz.

    Balanced at rho = sqrt(2)
    """

    Emod = modulation_energy(rho)

    Ebg = background_energy()

    imbalance = (Emod - Ebg)**2

    nonlinear = K * rho**4

    entropy_term = -np.log(1 + rho**2)

    return (
        imbalance
        +
        0.1*nonlinear
        +
        0.2*entropy_term
    )

# ------------------------------------------------------------

def resonance_signal(rho):

    """
    Resonance enhancement near equipartition.
    """

    Emod = modulation_energy(rho)

    Ebg = background_energy()

    return np.exp(
        -8*(Emod - Ebg)**2
    )

# ------------------------------------------------------------

def criticality(rho):

    """
    Diverges near equipartition.
    """

    Emod = modulation_energy(rho)

    Ebg = background_energy()

    return 1 / (
        abs(Emod - Ebg)
        + 1e-6
    )

# ============================================================
# SCAN
# ============================================================

rhos = np.linspace(0,RHO_MAX,NRHO)

Qvals = []
Svals = []
Pvals = []
Lvals = []
Fvals = []
Rvals = []
Cvals = []

# ============================================================
# MAIN LOOP
# ============================================================

best = None

for rho in rhos:

    m = orbit_density(rho)

    Q = Q_of_rho(rho)

    S = entropy(m)

    P = participation(m)

    L = localization(m)

    F = free_energy(rho)

    R = resonance_signal(rho)

    C = criticality(rho)

    Qvals.append(Q)
    Svals.append(S)
    Pvals.append(P)
    Lvals.append(L)
    Fvals.append(F)
    Rvals.append(R)
    Cvals.append(C)

    # --------------------------------------------------------
    # search for strongest critical resonance
    # --------------------------------------------------------

    score = R / (F + 1e-6)

    if best is None or score > best["score"]:

        best = {

            "rho": rho,
            "Q": Q,
            "entropy": S,
            "participation": P,
            "localization": L,
            "free_energy": F,
            "resonance": R,
            "criticality": C,
            "score": score

        }

# ============================================================
# REPORT
# ============================================================

print("\n" + "="*60)
print("CRITICAL EQUIPARTITION STATE")
print("="*60)

print(f"\nrho                = {best['rho']:.12f}")
print(f"sqrt(2)            = {np.sqrt(2):.12f}")

print(f"\nQ                  = {best['Q']:.12f}")
print(f"Target 2/3         = {2/3:.12f}")

print(f"\nEntropy            = {best['entropy']:.12f}")
print(f"Participation      = {best['participation']:.12f}")
print(f"Localization       = {best['localization']:.12f}")

print(f"\nFree energy        = {best['free_energy']:.12f}")
print(f"Resonance          = {best['resonance']:.12f}")
print(f"Criticality        = {best['criticality']:.12f}")

# ============================================================
# PLOTS
# ============================================================

# ------------------------------------------------------------
# Q(rho)
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10,6))

ax.plot(rhos,Qvals)

ax.axvline(
    np.sqrt(2),
    linestyle='--',
    label=r'$\rho=\sqrt{2}$'
)

ax.axhline(
    2/3,
    linestyle=':',
    label=r'$Q=2/3$'
)

ax.set_xlabel(r'$\rho$')
ax.set_ylabel(r'$Q(\rho)$')

ax.set_title(
    r'Exact Koide Functional: $Q(\rho)=1/3+\rho^2/6$'
)

ax.legend()

# ------------------------------------------------------------
# Free energy
# ------------------------------------------------------------

fig2, ax2 = plt.subplots(figsize=(10,6))

ax2.plot(rhos,Fvals)

ax2.axvline(
    np.sqrt(2),
    linestyle='--'
)

ax2.set_xlabel(r'$\rho$')
ax2.set_ylabel(r'$F(\rho)$')

ax2.set_title(
    'Effective Free Energy'
)

# ------------------------------------------------------------
# Resonance
# ------------------------------------------------------------

fig3, ax3 = plt.subplots(figsize=(10,6))

ax3.plot(rhos,Rvals)

ax3.axvline(
    np.sqrt(2),
    linestyle='--'
)

ax3.set_xlabel(r'$\rho$')
ax3.set_ylabel('Resonance')

ax3.set_title(
    'Critical Resonance Enhancement'
)

# ------------------------------------------------------------
# Criticality
# ------------------------------------------------------------

fig4, ax4 = plt.subplots(figsize=(10,6))

ax4.plot(rhos,Cvals)

ax4.axvline(
    np.sqrt(2),
    linestyle='--'
)

ax4.set_ylim(0,50)

ax4.set_xlabel(r'$\rho$')
ax4.set_ylabel('Criticality')

ax4.set_title(
    'Equipartition Criticality'
)

# ------------------------------------------------------------
# Entropy + participation
# ------------------------------------------------------------

fig5, ax5 = plt.subplots(figsize=(10,6))

ax5.plot(rhos,Svals,label='Entropy')

ax5.plot(rhos,Pvals,label='Participation')

ax5.axvline(
    np.sqrt(2),
    linestyle='--'
)

ax5.set_xlabel(r'$\rho$')

ax5.set_title(
    'Entropy and Participation'
)

ax5.legend()

# ------------------------------------------------------------
# Orbit profiles
# ------------------------------------------------------------

fig6, ax6 = plt.subplots(figsize=(10,6))

for rho in [

    0.0,
    1.0,
    np.sqrt(2),
    2.0

]:

    m = orbit_density(rho)

    ax6.plot(
        phi,
        m,
        label=fr'$\rho={rho:.3f}$'
    )

ax6.set_xlabel(r'$\phi$')
ax6.set_ylabel(r'$m(\phi)$')

ax6.set_title(
    'Double-Cover Orbit Density'
)

ax6.legend()

plt.show()
