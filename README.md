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

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/lukaszjaksik/Solana-MEV-Executor.git
cd solana-mev-executor
