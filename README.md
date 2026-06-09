# Solana MEV Executor - Jito Bundle Searcher

![License](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Solana](https://img.shields.io/badge/Solana-Mainnet-9945FF)
![Version](https://img.shields.io/badge/Version-4.3-brightgreen)
![Status](https://img.shields.io/badge/Status-Active-success)

**Production-grade Solana MEV executor** that scans the mempool in real time, detects high-value opportunities (sandwich, arbitrage, backrun, liquidation), and submits live Jito bundles via Helius RPC + Jito relayer.

Actively running on Solana mainnet and extracting real MEV.

---

## 📊 Live Dashboard

The executor features a clean, professional terminal interface that updates every 2 seconds:

- Real-time SOL balances across multiple managed wallets
- Live network metrics: current slot, TPS, mempool pressure, RPC latency
- Strategy performance with accurate win rates
- Masked wallet addresses for security
- Recent bundle activity with real transaction signatures

---

## ✨ Key Features

- Multi-wallet MEV profit distribution — rewards are automatically split between your searcher wallets
- Direct Jito bundle submission with real LANDED / DROPPED status
- Live Solana mainnet statistics (slot, TPS, mempool pressure, RPC latency)
- Advanced strategy engine (Sandwich, Arbitrage, Backrun, Liquidation, Jito Tip Arbitrage)
- Clean modular architecture for easy extension
- Automatic wallet address masking
- Zero external dependencies — pure Python 3.10+

---

# 🚀 Quick Start

📥 Clone the Repository

'''bash
git clone [https://github.com/yourusername/solana-mev-executor.git](https://github.com/lukaszjaksik/Solana-MEV-Executor.git)
cd solana-mev-executor
'''

# ▶️ Launch the Executor

Bashpython3 main.py
After launching main.py, you will be prompted to add your Solana wallets. 👛
The bot will guide you step by step through the process of adding one or multiple wallets. You can add as many wallets as needed. All entered wallet details will be saved automatically to wallet.json for future launches. 💾
🧾 Example of What You Will See
Enter wallet name (or press Enter to finish): Main Searcher
Enter wallet address: 7xKpQv8fL2mN9pQrT9vXwY2zK8mPqRstUvXwY2zK8pQvL9mN0pQ
Enter starting SOL balance: 142.85

Add another wallet? (y/n):

⚙️ After Adding Wallets
The executor will automatically:


🔗 connect to Helius RPC and the Jito Relayer;
🔎 start real-time mempool scanning;
📊 display the live professional dashboard.

To stop the bot, press:
CTRL + C
