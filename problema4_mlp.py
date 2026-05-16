import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

tf.random.set_seed(42)
np.random.seed(42)

# Dados do Problema 4
data = np.array([
    [28, 0.8, 35,  78.4],
    [32, 1.0, 38,  91.2],
    [35, 1.2, 42, 104.5],
    [38, 1.5, 45, 119.3],
    [42, 1.8, 48, 138.7],
    [45, 2.0, 52, 156.1],
    [48, 2.2, 55, 172.9],
    [50, 2.5, 60, 191.4],
    [30, 2.0, 32,  93.8],
    [40, 1.3, 50, 128.6],
])

X = data[:, :3]
y = data[:, 3]

# Normalização Min-Max
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()
X_norm = scaler_X.fit_transform(X)
y_norm = scaler_y.fit_transform(y.reshape(-1, 1)).ravel()

# Arquitetura MLP: 3 -> 16(tanh) -> 8(tanh) -> 1(linear)
model = Sequential([
    Dense(16, activation='tanh', input_shape=(3,)),
    Dense(8,  activation='tanh'),
    Dense(1,  activation='linear')
])
model.compile(optimizer=Adam(learning_rate=0.01), loss='mse')

history = model.fit(X_norm, y_norm, epochs=1000, verbose=0)

# Previsão
y_pred_norm = model.predict(X_norm, verbose=0).ravel()
y_pred = scaler_y.inverse_transform(y_pred_norm.reshape(-1, 1)).ravel()

# Métricas
mse  = mean_squared_error(y, y_pred)
rmse = np.sqrt(mse)
mae  = np.mean(np.abs(y - y_pred))
r2   = r2_score(y, y_pred)

print("=" * 40)
print(f"MSE  : {mse:.4f} kN²")
print(f"RMSE : {rmse:.4f} kN")
print(f"MAE  : {mae:.4f} kN")
print(f"R²   : {r2:.6f}")
print("=" * 40)
print("\nComparação real vs. previsto:")
print(f"{'fc':>6} {'rho':>6} {'d':>6} | {'P_real':>8} {'P_prev':>8} {'erro%':>7}")
for i in range(len(y)):
    err = 100*(y_pred[i]-y[i])/y[i]
    print(f"{X[i,0]:>6.0f} {X[i,1]:>6.1f} {X[i,2]:>6.0f} | {y[i]:>8.1f} {y_pred[i]:>8.2f} {err:>7.2f}%")

pasta = "C:/Users/Jordana/OneDrive - FUNAI - Fundação Nacional dos Povos Indígenas/projetos programação/sertão/"

# Figura 1 — Real vs. Previsto
fig, ax = plt.subplots(figsize=(5.5, 5))
ax.scatter(y, y_pred, color='steelblue', s=60, zorder=5, label='Amostras')
lim = [min(y.min(), y_pred.min())-5, max(y.max(), y_pred.max())+5]
ax.plot(lim, lim, 'r--', linewidth=1.2, label='Previsão perfeita')
ax.set_xlabel('P real (kN)', fontsize=11)
ax.set_ylabel('P previsto (kN)', fontsize=11)
ax.set_title(f'MLP — Real vs. Previsto  (R² = {r2:.4f})', fontsize=11)
ax.legend()
ax.set_xlim(lim); ax.set_ylim(lim)
plt.tight_layout()
plt.savefig(pasta + 'p4_real_vs_previsto.png', dpi=150)
print("Figura 1 salva.")

# Figura 2 — Curva de treinamento
fig2, ax2 = plt.subplots(figsize=(5.5, 4))
ax2.semilogy(history.history['loss'], color='steelblue', linewidth=1.2)
ax2.set_xlabel('Épocas', fontsize=11)
ax2.set_ylabel('MSE (normalizado)', fontsize=11)
ax2.set_title('Curva de Treinamento — MLP', fontsize=11)
plt.tight_layout()
plt.savefig(pasta + 'p4_curva_treinamento.png', dpi=150)
print("Figura 2 salva.")
