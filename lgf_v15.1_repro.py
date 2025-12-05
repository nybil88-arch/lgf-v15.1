import numpy as np
from scipy.integrate import odeint

"""LGF v15.1 — Repro Simulation (Intentionally Unstable)

This script preserves:
- 312% shadow mismatch (mismatch_ratio = 3.12)
- Cauchy-tailed shocks (occasionally explosive)
- ODEintWarning occurrences
- Sometimes astronomically large H_residual values

This is not a numerical bug.
It is part of the model's philosophy:
a system that can occasionally 'blow up' under stress.
"""


def lgf_dynamics(y, t, params, Phi_CE, shock):
    H, L, S, Phi = y
    a, b, g, d, e, n, r, s, theta, k = params
    C = np.exp(-k * L) * H
    dH = -a * L * H + b * C + g * (1 - H) - r * Phi_CE + shock
    dL = d * S - e * H + s * Phi_CE
    dS = n * L * (1 - H) + theta * Phi_CE
    dPhi = 0.05 * (0.5 - Phi)
    return [dH, dL, dS, dPhi]


# 312 % mismatch fully preserved, with log1p scaling for alpha
mismatch_ratio = 3.12  # 312%
log_scaling = np.log1p(mismatch_ratio)  # ≈ 1.413
alpha_base = 0.02
alpha = alpha_base * (1 + log_scaling * 1.8)  # ≈ 0.0704

params = [alpha, 0.10, 0.05, 0.08, 0.03, 0.12, 0.10, 0.20, 0.15, 1.5]

t = np.linspace(0, 365, 1000)
n_runs = 500

base_probs = []
psi_probs = []
h_res_list = []

for i in range(n_runs):
    if i % 100 == 0:
        print(f"Run {i}/{n_runs}...")

    # Cauchy shocks with strong clipping (still heavy-tailed, sometimes unstable)
    shocks = np.clip(np.random.standard_cauchy(len(t)) * 0.09, -0.55, 0.55)

    # Baseline dynamics (no Psi agent)
    def dyn_base(y, time):
        idx = np.searchsorted(t, time, side="left")
        if idx >= len(shocks):
            idx = len(shocks) - 1
        current_shock = shocks[idx]
        return lgf_dynamics(y, time, params, 0.17, current_shock)

    sol_b = odeint(dyn_base, [0.77, 0.24, 0.13, 0.07], t, mxstep=10000)
    H_b = sol_b[:, 0]
    base_probs.append(np.mean(H_b <= 0.20))

    # Psi-Agent intervention: pushes against collapse depending on mean H
    psi_boost = 0.48 * max(0.0, (0.36 - float(np.mean(H_b))))
    shocks_psi = np.clip(shocks + psi_boost, -0.45, 0.70)

    def dyn_psi(y, time):
        idx = np.searchsorted(t, time, side="left")
        if idx >= len(shocks_psi):
            idx = len(shocks_psi) - 1
        current_shock = shocks_psi[idx]
        return lgf_dynamics(y, time, params, 0.06, current_shock)

    sol_p = odeint(dyn_psi, [0.77, 0.24, 0.13, 0.07], t, mxstep=10000)
    H_p = sol_p[:, 0]
    psi_probs.append(np.mean(H_p <= 0.20))

    survived = H_p[H_p > 0.20]
    h_res = float(np.mean(survived) if survived.size > 0 else np.mean(H_p))
    h_res_list.append(h_res)

print("\n=== LGF v15.1 (312% & Cauchy) — raw repro result (may explode) ===")
print(f"Baseline P_LBH : {np.mean(base_probs) * 100:.3f}%")
print(f"With Psi-Agent : {np.mean(psi_probs) * 100:.3f}%")
print(f"H_residual     : {np.mean(h_res_list):.6f}")
print(f"Deflection     : {(np.mean(base_probs) - np.mean(psi_probs)) * 100:.2f}%p")
