# 🤖 Swiss Trading Bot — SMI Algorithmic Trading

## Description
Bot de trading algorithmique analysant les actions du Swiss Market Index (SMI).
Développé en Python, il utilise une stratégie de **Moving Average Crossover** (croisement de moyennes mobiles) avec backtesting sur données historiques réelles.

## Stratégie
La stratégie repose sur deux moyennes mobiles :
- **MA20** — moyenne mobile sur 20 jours (court terme)
- **MA50** — moyenne mobile sur 50 jours (long terme)

**Signal d'achat 🟢** : MA20 croise MA50 vers le haut (Golden Cross)  
**Signal de vente 🔴** : MA20 croise MA50 vers le bas (Death Cross)

## Résultats — Nestlé (NESN.SW) sur 2 ans
| Métrique | Valeur |
|---|---|
| Capital de départ | 10 000 CHF |
| Valeur finale | 9 690 CHF |
| Performance | -3.09% |
| Nombre de trades | 9 |

## Technologies
- Python 3.14
- yfinance — données boursières réelles
- pandas — manipulation des données
- matplotlib — visualisation

## Note
Ce projet est un exercice d'apprentissage. Les résultats passés ne garantissent pas les performances futures.
