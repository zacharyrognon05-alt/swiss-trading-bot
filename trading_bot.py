import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# ============================================
# CONFIGURATION
# ============================================
TICKER = "NESN.SW"
PERIODE = "2y"
MA_COURT = 20
MA_LONG = 50
CAPITAL_DEPART = 10000

# ============================================
# 1. TÉLÉCHARGEMENT DES DONNÉES
# ============================================
print("Téléchargement des données de Nestlé...")
df = yf.download(TICKER, period=PERIODE, auto_adjust=True)
df = df[['Close']].copy()
df.columns = ['Close']
df = df.dropna()
print(f"✅ {len(df)} jours de données récupérés")

# ============================================
# 2. CALCUL DES MOYENNES MOBILES
# ============================================
df['MA20'] = df['Close'].rolling(window=MA_COURT).mean()
df['MA50'] = df['Close'].rolling(window=MA_LONG).mean()

# ============================================
# 3. GÉNÉRATION DES SIGNAUX
# ============================================
df['Signal'] = 0
df.loc[df['MA20'] > df['MA50'], 'Signal'] = 1
df.loc[df['MA20'] < df['MA50'], 'Signal'] = -1
df['Position'] = df['Signal'].diff()

# ============================================
# 4. BACKTESTING
# ============================================
capital = CAPITAL_DEPART
actions = 0
trades = []

for date, row in df.iterrows():
    prix = float(row['Close'])
    position = float(row['Position'])
    if position == 2 and capital > 0:
        actions = capital / prix
        capital = 0
        trades.append({'date': date, 'type': 'ACHAT', 'prix': prix})
    elif position == -2 and actions > 0:
        capital = actions * prix
        actions = 0
        trades.append({'date': date, 'type': 'VENTE', 'prix': prix})

valeur_finale = capital if capital > 0 else actions * float(df['Close'].iloc[-1])

# ============================================
# 5. RÉSULTATS
# ============================================
print("\n========== RÉSULTATS DU BACKTEST ==========")
print(f"Capital de départ   : {CAPITAL_DEPART} CHF")
print(f"Valeur finale       : {valeur_finale:.2f} CHF")
print(f"Performance         : {((valeur_finale - CAPITAL_DEPART) / CAPITAL_DEPART * 100):.2f}%")
print(f"Nombre de trades    : {len(trades)}")
print("============================================\n")

# ============================================
# 6. GRAPHIQUE
# ============================================
fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(df.index, df['Close'], label='Cours Nestlé', color='gray', alpha=0.7)
ax.plot(df.index, df['MA20'], label='MA20', color='blue', linewidth=1.5)
ax.plot(df.index, df['MA50'], label='MA50', color='orange', linewidth=1.5)

for trade in trades:
    if trade['type'] == 'ACHAT':
        ax.axvline(x=trade['date'], color='green', alpha=0.4, linestyle='--')
        ax.annotate('▲ Achat', xy=(trade['date'], trade['prix']),
                    color='green', fontsize=8)
    else:
        ax.axvline(x=trade['date'], color='red', alpha=0.4, linestyle='--')
        ax.annotate('▼ Vente', xy=(trade['date'], trade['prix']),
                    color='red', fontsize=8)

ax.set_title('Bot de Trading — Nestlé (NESN.SW) — Stratégie Moyennes Mobiles', fontsize=14)
ax.set_xlabel('Date')
ax.set_ylabel('Prix (CHF)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/Users/zach/Desktop/resultats_trading.png', dpi=150)
plt.show()
print("✅ Graphique sauvegardé : resultats_trading.png")