"""
Visualizações completas — Problema 4: Carga de ruptura MLP
Gera 6 figuras de alta qualidade para o artigo III MCSM.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D  # noqa
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

PASTA = (r"C:\Users\Jordana\OneDrive - FUNAI - Fundação Nacional dos "
         r"Povos Indígenas\projetos programação\sertão")

tf.random.set_seed(42)
np.random.seed(42)

CORES = {
    "azul":     "#2176AE",
    "laranja":  "#E07A5F",
    "verde":    "#3D9970",
    "roxo":     "#6C3483",
    "cinza":    "#7F8C8D",
    "amarelo":  "#F4C430",
}

# ═══════════════════════════════════════════════════════════════
# DADOS E MODELO
# ═══════════════════════════════════════════════════════════════
data = np.array([
    [28,  0.8, 35,  78.4],
    [32,  1.0, 38,  91.2],
    [35,  1.2, 42, 104.5],
    [38,  1.5, 45, 119.3],
    [42,  1.8, 48, 138.7],
    [45,  2.0, 52, 156.1],
    [48,  2.2, 55, 172.9],
    [50,  2.5, 60, 191.4],
    [30,  2.0, 32,  93.8],
    [40,  1.3, 50, 128.6],
])
X, y = data[:, :3], data[:, 3]

scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()
X_norm = scaler_X.fit_transform(X)
y_norm = scaler_y.fit_transform(y.reshape(-1, 1)).ravel()

model = Sequential([
    Dense(16, activation='tanh', input_shape=(3,)),
    Dense(8,  activation='tanh'),
    Dense(1,  activation='linear'),
])
model.compile(optimizer=Adam(0.01), loss='mse')
history = model.fit(X_norm, y_norm, epochs=1000, verbose=0)

y_pred_norm = model.predict(X_norm, verbose=0).ravel()
y_pred = scaler_y.inverse_transform(y_pred_norm.reshape(-1, 1)).ravel()

# regressão linear (comparação)
lr = LinearRegression().fit(X, y)
y_lr = lr.predict(X)

r2_mlp = r2_score(y, y_pred)
r2_lr  = r2_score(y, y_lr)
rmse_mlp = np.sqrt(mean_squared_error(y, y_pred))
rmse_lr  = np.sqrt(mean_squared_error(y, y_lr))


# ═══════════════════════════════════════════════════════════════
# FIG 1 — CURVA DE TREINAMENTO
# ═══════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(6, 4))
ax.semilogy(history.history['loss'], color=CORES["azul"], linewidth=1.8, label='MSE treino')
ax.set_xlabel("Épocas", fontsize=12)
ax.set_ylabel("MSE (escala log, normalizado)", fontsize=12)
ax.set_title("Curva de Treinamento — MLP Problema 4", fontsize=13, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(f"{PASTA}/fig1_curva_treinamento.png", dpi=180)
plt.close()
print("Fig 1 salva.")


# ═══════════════════════════════════════════════════════════════
# FIG 2 — REAL vs. PREVISTO (MLP vs Regressão Linear)
# ═══════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(11, 5))
lim = [70, 200]

for ax, yp, label, r2, rmse, cor in [
    (axes[0], y_pred, "MLP",              r2_mlp, rmse_mlp, CORES["azul"]),
    (axes[1], y_lr,   "Regressão Linear", r2_lr,  rmse_lr,  CORES["laranja"]),
]:
    ax.scatter(y, yp, color=cor, s=70, zorder=5, label='Amostras')
    ax.plot(lim, lim, 'k--', linewidth=1.2, label='Ideal', alpha=0.6)
    ax.set_xlim(lim); ax.set_ylim(lim)
    ax.set_xlabel("P real (kN)", fontsize=12)
    ax.set_ylabel("P previsto (kN)", fontsize=12)
    ax.set_title(f"{label}\nR² = {r2:.4f} | RMSE = {rmse:.2f} kN",
                 fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.4)

fig.suptitle("Comparação: MLP vs. Regressão Linear", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(f"{PASTA}/fig2_real_vs_previsto.png", dpi=180)
plt.close()
print("Fig 2 salva.")


# ═══════════════════════════════════════════════════════════════
# FIG 3 — ANÁLISE DE SENSIBILIDADE (variação individual de fc, ρ, d)
# ═══════════════════════════════════════════════════════════════
fc_med  = X[:, 0].mean()   # ≈ 38.8 MPa
rho_med = X[:, 1].mean()   # ≈ 1.63 %
d_med   = X[:, 2].mean()   # ≈ 44.7 cm

def predict_p(fc_arr, rho_arr, d_arr):
    inp = np.column_stack([fc_arr, rho_arr, d_arr])
    inp_n = scaler_X.transform(inp)
    out_n = model.predict(inp_n, verbose=0).ravel()
    return scaler_y.inverse_transform(out_n.reshape(-1, 1)).ravel()

fc_range  = np.linspace(25, 50, 60)
rho_range = np.linspace(0.5, 2.5, 60)
d_range   = np.linspace(30, 60, 60)

P_fc  = predict_p(fc_range,           np.full(60, rho_med), np.full(60, d_med))
P_rho = predict_p(np.full(60, fc_med), rho_range,           np.full(60, d_med))
P_d   = predict_p(np.full(60, fc_med), np.full(60, rho_med), d_range)

fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

axes[0].plot(fc_range, P_fc, color=CORES["azul"], linewidth=2.2)
axes[0].set_xlabel("fc — Resistência do concreto (MPa)", fontsize=11)
axes[0].set_ylabel("P previsto (kN)", fontsize=11)
axes[0].set_title(f"Sensibilidade a fc\n(ρ = {rho_med:.2f}%, d = {d_med:.1f} cm)", fontsize=11)
axes[0].grid(True, linestyle='--', alpha=0.4)

axes[1].plot(rho_range, P_rho, color=CORES["verde"], linewidth=2.2)
axes[1].set_xlabel("ρ — Taxa de armadura (%)", fontsize=11)
axes[1].set_ylabel("P previsto (kN)", fontsize=11)
axes[1].set_title(f"Sensibilidade a ρ\n(fc = {fc_med:.1f} MPa, d = {d_med:.1f} cm)", fontsize=11)
axes[1].grid(True, linestyle='--', alpha=0.4)

axes[2].plot(d_range, P_d, color=CORES["laranja"], linewidth=2.2)
axes[2].set_xlabel("d — Altura útil (cm)", fontsize=11)
axes[2].set_ylabel("P previsto (kN)", fontsize=11)
axes[2].set_title(f"Sensibilidade a d\n(fc = {fc_med:.1f} MPa, ρ = {rho_med:.2f}%)", fontsize=11)
axes[2].grid(True, linestyle='--', alpha=0.4)

fig.suptitle("Análise de Sensibilidade — Influência Individual de cada Variável sobre P",
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(f"{PASTA}/fig3_sensibilidade.png", dpi=180)
plt.close()
print("Fig 3 salva.")


# ═══════════════════════════════════════════════════════════════
# FIG 4 — SUPERFÍCIE 3D: P = f(fc, d)  com ρ fixo na média
# ═══════════════════════════════════════════════════════════════
FC_g, D_g = np.meshgrid(np.linspace(25, 50, 40), np.linspace(30, 60, 40))
RHO_g = np.full_like(FC_g, rho_med)

P_grid_mlp = predict_p(FC_g.ravel(), RHO_g.ravel(), D_g.ravel()).reshape(FC_g.shape)
P_grid_ana = 0.35*FC_g + 12*rho_med + 2.1*D_g - 0.02*FC_g*D_g   # modelo analítico

fig = plt.figure(figsize=(14, 6))

ax1 = fig.add_subplot(121, projection='3d')
surf1 = ax1.plot_surface(FC_g, D_g, P_grid_mlp, cmap='viridis', alpha=0.85)
ax1.set_xlabel("fc (MPa)", fontsize=10, labelpad=8)
ax1.set_ylabel("d (cm)",   fontsize=10, labelpad=8)
ax1.set_zlabel("P (kN)",   fontsize=10, labelpad=8)
ax1.set_title(f"MLP  (ρ = {rho_med:.2f}%)", fontsize=12, fontweight='bold')
fig.colorbar(surf1, ax=ax1, shrink=0.5, pad=0.1)

ax2 = fig.add_subplot(122, projection='3d')
surf2 = ax2.plot_surface(FC_g, D_g, P_grid_ana, cmap='plasma', alpha=0.85)
ax2.set_xlabel("fc (MPa)", fontsize=10, labelpad=8)
ax2.set_ylabel("d (cm)",   fontsize=10, labelpad=8)
ax2.set_zlabel("P (kN)",   fontsize=10, labelpad=8)
ax2.set_title(f"Modelo Analítico  (ρ = {rho_med:.2f}%)", fontsize=12, fontweight='bold')
fig.colorbar(surf2, ax=ax2, shrink=0.5, pad=0.1)

fig.suptitle("Superfície 3D — P = f(fc, d): MLP vs. Modelo Analítico",
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(f"{PASTA}/fig4_superficie_3d.png", dpi=180)
plt.close()
print("Fig 4 salva.")


# ═══════════════════════════════════════════════════════════════
# FIG 5 — RESÍDUOS
# ═══════════════════════════════════════════════════════════════
residuos = y_pred - y
pct_err  = 100 * residuos / y

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

# Resíduo absoluto
axes[0].bar(range(1, 11), residuos,
            color=[CORES["azul"] if r >= 0 else CORES["laranja"] for r in residuos],
            edgecolor='black', linewidth=0.6)
axes[0].axhline(0, color='black', linewidth=1.0, linestyle='--')
axes[0].set_xticks(range(1, 11))
axes[0].set_xlabel("Amostra", fontsize=12)
axes[0].set_ylabel("Resíduo  (kN)", fontsize=12)
axes[0].set_title("Resíduo Absoluto (P_prev − P_real)", fontsize=12, fontweight='bold')
axes[0].grid(axis='y', linestyle='--', alpha=0.4)

# Erro percentual
axes[1].bar(range(1, 11), pct_err,
            color=[CORES["verde"] if e >= 0 else CORES["roxo"] for e in pct_err],
            edgecolor='black', linewidth=0.6)
axes[1].axhline(0, color='black', linewidth=1.0, linestyle='--')
axes[1].set_xticks(range(1, 11))
axes[1].set_xlabel("Amostra", fontsize=12)
axes[1].set_ylabel("Erro (%)", fontsize=12)
axes[1].set_title("Erro Percentual por Amostra", fontsize=12, fontweight='bold')
axes[1].grid(axis='y', linestyle='--', alpha=0.4)

fig.suptitle("Análise de Resíduos — MLP Problema 4",
             fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(f"{PASTA}/fig5_residuos.png", dpi=180)
plt.close()
print("Fig 5 salva.")


# ═══════════════════════════════════════════════════════════════
# FIG 6 — PAINEL RESUMO (dashboard compacto)
# ═══════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(14, 9))
gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

# 6a — Curva de treinamento
ax6a = fig.add_subplot(gs[0, 0])
ax6a.semilogy(history.history['loss'], color=CORES["azul"], linewidth=1.5)
ax6a.set_title("Curva de Treinamento", fontsize=11, fontweight='bold')
ax6a.set_xlabel("Épocas"); ax6a.set_ylabel("MSE (log)")
ax6a.grid(True, linestyle='--', alpha=0.4)

# 6b — Real vs. Previsto MLP
ax6b = fig.add_subplot(gs[0, 1])
ax6b.scatter(y, y_pred, color=CORES["azul"], s=60, zorder=5)
ax6b.plot(lim, lim, 'k--', linewidth=1)
ax6b.set_xlim(lim); ax6b.set_ylim(lim)
ax6b.set_title(f"Real vs. Previsto\nR² = {r2_mlp:.4f}", fontsize=11, fontweight='bold')
ax6b.set_xlabel("P real (kN)"); ax6b.set_ylabel("P previsto (kN)")
ax6b.grid(True, linestyle='--', alpha=0.4)

# 6c — Erro percentual
ax6c = fig.add_subplot(gs[0, 2])
ax6c.bar(range(1, 11), pct_err,
         color=[CORES["verde"] if e >= 0 else CORES["laranja"] for e in pct_err],
         edgecolor='black', linewidth=0.5)
ax6c.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax6c.set_title("Erro Percentual por Amostra", fontsize=11, fontweight='bold')
ax6c.set_xlabel("Amostra"); ax6c.set_ylabel("Erro (%)")
ax6c.set_xticks(range(1, 11))
ax6c.grid(axis='y', linestyle='--', alpha=0.4)

# 6d — Sensibilidade a fc
ax6d = fig.add_subplot(gs[1, 0])
ax6d.plot(fc_range, P_fc, color=CORES["azul"], linewidth=2)
ax6d.set_title("Sensibilidade: P vs fc", fontsize=11, fontweight='bold')
ax6d.set_xlabel("fc (MPa)"); ax6d.set_ylabel("P (kN)")
ax6d.grid(True, linestyle='--', alpha=0.4)

# 6e — Sensibilidade a ρ
ax6e = fig.add_subplot(gs[1, 1])
ax6e.plot(rho_range, P_rho, color=CORES["verde"], linewidth=2)
ax6e.set_title("Sensibilidade: P vs ρ", fontsize=11, fontweight='bold')
ax6e.set_xlabel("ρ (%)"); ax6e.set_ylabel("P (kN)")
ax6e.grid(True, linestyle='--', alpha=0.4)

# 6f — Sensibilidade a d
ax6f = fig.add_subplot(gs[1, 2])
ax6f.plot(d_range, P_d, color=CORES["laranja"], linewidth=2)
ax6f.set_title("Sensibilidade: P vs d", fontsize=11, fontweight='bold')
ax6f.set_xlabel("d (cm)"); ax6f.set_ylabel("P (kN)")
ax6f.grid(True, linestyle='--', alpha=0.4)

fig.suptitle("Painel Geral — MLP para Previsão de Carga de Ruptura em Vigas de Concreto",
             fontsize=14, fontweight='bold')
plt.savefig(f"{PASTA}/fig6_painel_resumo.png", dpi=180, bbox_inches='tight')
plt.close()
print("Fig 6 salva.")

print("\n=== Todas as figuras geradas com sucesso! ===")
print(f"Pasta: {PASTA}")
print("Arquivos: fig1 a fig6 (.png)")
