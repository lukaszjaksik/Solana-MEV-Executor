class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


APP_NAME = "Solana MEV Executor"
APP_VERSION = "4.3.7"
NETWORK = "mainnet-beta"
DEFAULT_ENCODING = "utf-8"
WALLET_FILE = "wallet.json"
LOG_FILE = "executor.log"
STATE_FILE = "runtime_state.json"


RPC_ENDPOINTS = [
    {
        "name": "helius-fra-priority",
        "provider": "Helius",
        "region": "fra",
        "weight": 34,
        "latency_target_ms": 42,
        "slot_lag_limit": 2,
        "enabled": True,
    },
    {
        "name": "helius-ams-private",
        "provider": "Helius",
        "region": "ams",
        "weight": 21,
        "latency_target_ms": 48,
        "slot_lag_limit": 2,
        "enabled": True,
    },
    {
        "name": "jito-main-relay",
        "provider": "Jito",
        "region": "global",
        "weight": 26,
        "latency_target_ms": 36,
        "slot_lag_limit": 1,
        "enabled": True,
    },
    {
        "name": "quicknode-lon-burst",
        "provider": "QuickNode",
        "region": "lon",
        "weight": 12,
        "latency_target_ms": 64,
        "slot_lag_limit": 3,
        "enabled": True,
    },
    {
        "name": "alchemy-nyc-fallback",
        "provider": "Alchemy",
        "region": "nyc",
        "weight": 7,
        "latency_target_ms": 88,
        "slot_lag_limit": 4,
        "enabled": True,
    },
]


RELAYER_ENDPOINTS = [
    {
        "name": "jito-fra",
        "region": "fra",
        "enabled": True,
        "max_inflight_bundles": 8,
        "tip_floor_sol": 0.0012,
    },
    {
        "name": "jito-ams",
        "region": "ams",
        "enabled": True,
        "max_inflight_bundles": 8,
        "tip_floor_sol": 0.0014,
    },
    {
        "name": "jito-nyc",
        "region": "nyc",
        "enabled": True,
        "max_inflight_bundles": 5,
        "tip_floor_sol": 0.0018,
    },
    {
        "name": "private-relay-a",
        "region": "lon",
        "enabled": True,
        "max_inflight_bundles": 4,
        "tip_floor_sol": 0.0021,
    },
]


STRATEGIES = [
    "Sandwich",
    "Arbitrage",
    "Backrun",
    "Liquidation",
    "Jito Tip Arbitrage",
    "Latency Capture",
    "Route Repricing",
    "Spread Sweep",
    "Priority Replay",
    "Slot Edge",
]


STRATEGY_WEIGHTS = {
    "Sandwich": 24,
    "Arbitrage": 22,
    "Backrun": 18,
    "Liquidation": 11,
    "Jito Tip Arbitrage": 7,
    "Latency Capture": 5,
    "Route Repricing": 5,
    "Spread Sweep": 4,
    "Priority Replay": 3,
    "Slot Edge": 1,
}


TOKENS = [
    "WIF/SOL",
    "PEPE/SOL",
    "BONK/SOL",
    "POPCAT/SOL",
    "DOGE/SOL",
    "MOTHER/SOL",
    "GIGA/SOL",
    "JUP/SOL",
    "PYTH/SOL",
    "RAY/SOL",
    "ORCA/SOL",
    "JTO/SOL",
    "HNT/SOL",
    "MOBILE/SOL",
    "MEW/SOL",
    "SAMO/SOL",
    "FIDA/SOL",
    "MSOL/SOL",
    "BSOL/SOL",
    "USDC/SOL",
    "USDT/SOL",
    "WEN/SOL",
    "BOME/SOL",
    "TNSR/SOL",
]


TOKEN_METADATA = {
    "WIF/SOL": {"category": "meme", "min_depth_usd": 85000, "max_slippage_bps": 90},
    "PEPE/SOL": {"category": "meme", "min_depth_usd": 54000, "max_slippage_bps": 110},
    "BONK/SOL": {"category": "meme", "min_depth_usd": 220000, "max_slippage_bps": 80},
    "POPCAT/SOL": {"category": "meme", "min_depth_usd": 73000, "max_slippage_bps": 125},
    "DOGE/SOL": {"category": "meme", "min_depth_usd": 62000, "max_slippage_bps": 120},
    "MOTHER/SOL": {"category": "meme", "min_depth_usd": 45000, "max_slippage_bps": 145},
    "GIGA/SOL": {"category": "meme", "min_depth_usd": 47000, "max_slippage_bps": 135},
    "JUP/SOL": {"category": "defi", "min_depth_usd": 330000, "max_slippage_bps": 60},
    "PYTH/SOL": {"category": "oracle", "min_depth_usd": 180000, "max_slippage_bps": 70},
    "RAY/SOL": {"category": "dex", "min_depth_usd": 290000, "max_slippage_bps": 65},
    "ORCA/SOL": {"category": "dex", "min_depth_usd": 210000, "max_slippage_bps": 70},
    "JTO/SOL": {"category": "staking", "min_depth_usd": 250000, "max_slippage_bps": 75},
    "HNT/SOL": {"category": "depin", "min_depth_usd": 80000, "max_slippage_bps": 95},
    "MOBILE/SOL": {"category": "depin", "min_depth_usd": 61000, "max_slippage_bps": 115},
    "MEW/SOL": {"category": "meme", "min_depth_usd": 76000, "max_slippage_bps": 130},
    "SAMO/SOL": {"category": "meme", "min_depth_usd": 39000, "max_slippage_bps": 150},
    "FIDA/SOL": {"category": "infra", "min_depth_usd": 52000, "max_slippage_bps": 125},
    "MSOL/SOL": {"category": "lst", "min_depth_usd": 500000, "max_slippage_bps": 35},
    "BSOL/SOL": {"category": "lst", "min_depth_usd": 420000, "max_slippage_bps": 38},
    "USDC/SOL": {"category": "stable", "min_depth_usd": 1200000, "max_slippage_bps": 18},
    "USDT/SOL": {"category": "stable", "min_depth_usd": 880000, "max_slippage_bps": 22},
    "WEN/SOL": {"category": "meme", "min_depth_usd": 67000, "max_slippage_bps": 130},
    "BOME/SOL": {"category": "meme", "min_depth_usd": 92000, "max_slippage_bps": 105},
    "TNSR/SOL": {"category": "nft", "min_depth_usd": 71000, "max_slippage_bps": 125},
}


DEXES = [
    "Raydium",
    "Orca",
    "Phoenix",
    "Meteora",
    "OpenBook",
    "Lifinity",
    "Jupiter",
    "Saber",
    "Aldrin",
    "Cropper",
]


DEX_METADATA = {
    "Raydium": {"type": "amm", "priority": 96, "fee_bps": 25, "enabled": True},
    "Orca": {"type": "clmm", "priority": 94, "fee_bps": 20, "enabled": True},
    "Phoenix": {"type": "orderbook", "priority": 91, "fee_bps": 4, "enabled": True},
    "Meteora": {"type": "dlmm", "priority": 89, "fee_bps": 18, "enabled": True},
    "OpenBook": {"type": "orderbook", "priority": 82, "fee_bps": 5, "enabled": True},
    "Lifinity": {"type": "amm", "priority": 78, "fee_bps": 20, "enabled": True},
    "Jupiter": {"type": "router", "priority": 98, "fee_bps": 0, "enabled": True},
    "Saber": {"type": "stable", "priority": 66, "fee_bps": 4, "enabled": True},
    "Aldrin": {"type": "amm", "priority": 52, "fee_bps": 30, "enabled": True},
    "Cropper": {"type": "amm", "priority": 49, "fee_bps": 30, "enabled": True},
}


INITIAL_VALUES = {
    "total_mev_extracted": 18.47,
    "daily_mev_extracted": 4.23,
    "jito_tips_paid": 2.34,
    "avg_profit_per_bundle": 0.112,
    "bundles_submitted": 187,
    "successful_bundles": 163,
    "dropped_bundles": 14,
    "current_slot": 285174392,
    "mempool_scanned": 1247,
    "network_tps": 2840,
    "rpc_latency": 24,
    "mempool_pressure": 62,
    "route_quality": 84,
    "relay_acceptance": 91,
    "wallet_utilization": 73,
    "priority_fee_level": 44,
    "active_routes": 9,
    "tracked_markets": 38,
}


STRATEGY_STATS = {
    "Sandwich": {"won": 87, "total": 102, "gross": 11.28, "tips": 0.94},
    "Arbitrage": {"won": 34, "total": 41, "gross": 4.74, "tips": 0.39},
    "Backrun": {"won": 22, "total": 28, "gross": 2.91, "tips": 0.25},
    "Liquidation": {"won": 18, "total": 19, "gross": 6.32, "tips": 0.44},
    "Jito Tip Arbitrage": {"won": 2, "total": 3, "gross": 0.18, "tips": 0.03},
    "Latency Capture": {"won": 14, "total": 19, "gross": 1.42, "tips": 0.11},
    "Route Repricing": {"won": 27, "total": 36, "gross": 2.09, "tips": 0.21},
    "Spread Sweep": {"won": 11, "total": 18, "gross": 0.86, "tips": 0.08},
    "Priority Replay": {"won": 8, "total": 15, "gross": 0.64, "tips": 0.09},
    "Slot Edge": {"won": 4, "total": 7, "gross": 0.31, "tips": 0.04},
}


RISK_LIMITS = {
    "max_position_sol": 340.0,
    "max_bundle_tip_sol": 0.08,
    "max_priority_fee_sol": 0.035,
    "max_route_legs": 5,
    "max_slippage_bps": 150,
    "max_price_impact_bps": 180,
    "min_profit_sol": 0.012,
    "min_profit_after_tip_sol": 0.006,
    "min_depth_usd": 35000,
    "min_confidence": 0.58,
    "wallet_cooldown_slots": 3,
    "market_cooldown_slots": 2,
    "bundle_expiry_slots": 5,
    "rpc_slot_lag_limit": 4,
}


SCAN_SETTINGS = {
    "enabled": True,
    "scan_interval_seconds": 2.0,
    "dashboard_refresh_seconds": 2.0,
    "max_transactions_per_cycle": 720,
    "max_routes_per_transaction": 8,
    "max_bundles_in_flight": 6,
    "route_cache_seconds": 7,
    "market_cache_seconds": 4,
    "wallet_refresh_seconds": 15,
    "health_refresh_seconds": 10,
    "log_tail_size": 14,
}


PRIORITY_FEE_SETTINGS = {
    "mode": "adaptive",
    "floor_sol": 0.000012,
    "base_sol": 0.00018,
    "ceiling_sol": 0.035,
    "pressure_multiplier": 1.35,
    "latency_multiplier": 1.12,
    "route_quality_multiplier": 0.92,
    "rebid_threshold_slots": 2,
}


TIP_SETTINGS = {
    "mode": "adaptive",
    "floor_sol": 0.0012,
    "base_sol": 0.0065,
    "ceiling_sol": 0.08,
    "profit_share": 0.18,
    "pressure_share": 0.07,
    "min_landing_probability": 0.61,
    "rebid_multiplier": 1.22,
}


DASHBOARD_FIELDS = [
    "searcher",
    "rpc",
    "slot",
    "tps",
    "mempool_pressure",
    "mempool_scanned",
    "bundles_in_flight",
    "total_mev",
    "daily_mev",
    "tips_paid",
    "avg_profit",
    "uptime",
    "strategy_performance",
    "managed_wallets",
    "recent_activity",
]


EVENT_LABELS = {
    "swap": "Large swap detected",
    "arb": "Cross-DEX spread detected",
    "backrun": "Backrun route prepared",
    "liquidation": "Collateral window opened",
    "tip": "Relay tip opportunity",
    "latency": "Latency edge detected",
    "route": "Route price refreshed",
    "spread": "Spread sweep available",
    "priority": "Priority lane opened",
    "slot": "Leader slot aligned",
}


STATUS_LABELS = {
    "landed": "LANDED",
    "dropped": "DROPPED",
    "queued": "QUEUED",
    "accepted": "ACCEPTED",
    "expired": "EXPIRED",
    "repriced": "REPRICED",
    "prepared": "PREPARED",
}


PROFIT_RANGES = {
    "Sandwich": (0.18, 1.45),
    "Arbitrage": (0.09, 0.62),
    "Backrun": (0.07, 0.44),
    "Liquidation": (0.31, 2.15),
    "Jito Tip Arbitrage": (0.04, 0.18),
    "Latency Capture": (0.05, 0.36),
    "Route Repricing": (0.06, 0.48),
    "Spread Sweep": (0.04, 0.29),
    "Priority Replay": (0.03, 0.24),
    "Slot Edge": (0.02, 0.16),
}


ACTION_TEMPLATES = {
    "Sandwich": [
        "Sandwich route on Raydium {token}",
        "Two-leg sandwich route through Orca {token}",
        "Priority sandwich bundle for {token}",
        "Jupiter-routed sandwich opportunity {token}",
    ],
    "Arbitrage": [
        "Cross-DEX arb Jupiter ↔ Phoenix {token}",
        "Raydium ↔ Orca spread capture {token}",
        "Meteora ↔ OpenBook arb route {token}",
        "Lifinity price mismatch captured {token}",
    ],
    "Backrun": [
        "Backrun route prepared {token}",
        "Post-swap backrun through Jupiter {token}",
        "Backrun against Raydium impact {token}",
        "Liquidity recovery backrun {token}",
    ],
    "Liquidation": [
        "Liquidation hunt {token}",
        "Collateral unwind route {token}",
        "Keeper route prepared {token}",
        "Margin account unwind {token}",
    ],
    "Jito Tip Arbitrage": [
        "Jito tip arb {token}",
        "Relay tip repricing {token}",
        "Tip spread capture {token}",
        "Priority tip rebalance {token}",
    ],
    "Latency Capture": [
        "Latency edge route {token}",
        "Fast-lane quote capture {token}",
        "Low-latency settlement path {token}",
        "Slot timing edge {token}",
    ],
    "Route Repricing": [
        "Route repricing window {token}",
        "Aggregator quote refresh {token}",
        "Route delta capture {token}",
        "Split-route improvement {token}",
    ],
    "Spread Sweep": [
        "Spread sweep route {token}",
        "Orderbook sweep opportunity {token}",
        "Pool spread capture {token}",
        "Depth imbalance route {token}",
    ],
    "Priority Replay": [
        "Priority replay route {token}",
        "Rebroadcast lane opportunity {token}",
        "Priority transaction alignment {token}",
        "Relay lane repricing {token}",
    ],
    "Slot Edge": [
        "Leader slot edge {token}",
        "Slot-local route {token}",
        "Leader schedule alignment {token}",
        "Slot timing capture {token}",
    ],
}


MARKET_WINDOWS = {
    "micro": {"seconds": 5, "min_spread_bps": 4, "min_depth_usd": 25000},
    "short": {"seconds": 15, "min_spread_bps": 8, "min_depth_usd": 50000},
    "medium": {"seconds": 60, "min_spread_bps": 12, "min_depth_usd": 100000},
    "extended": {"seconds": 300, "min_spread_bps": 20, "min_depth_usd": 250000},
}


WALLET_GROUPS = {
    "primary": {"max_weight": 0.42, "cooldown_slots": 2, "enabled": True},
    "secondary": {"max_weight": 0.28, "cooldown_slots": 3, "enabled": True},
    "vault": {"max_weight": 0.18, "cooldown_slots": 5, "enabled": True},
    "backup": {"max_weight": 0.12, "cooldown_slots": 8, "enabled": True},
}


LOG_SETTINGS = {
    "enabled": True,
    "level": "info",
    "rotate": True,
    "max_size_mb": 12,
    "keep_files": 5,
    "write_activity": True,
    "write_wallet_updates": True,
    "write_rpc_health": True,
}


TERMINAL_SETTINGS = {
    "clear_screen": True,
    "show_colors": True,
    "show_wallets": True,
    "show_strategy_stats": True,
    "show_recent_activity": True,
    "show_rpc_health": True,
    "show_market_depth": True,
    "compact_mode": False,
}


PERFORMANCE_TARGETS = {
    "success_rate": 86.0,
    "avg_profit_per_bundle": 0.105,
    "max_rpc_latency_ms": 75,
    "min_tps": 1800,
    "max_bundle_drop_rate": 12.0,
    "min_relay_acceptance": 78.0,
    "min_route_quality": 67.0,
}


def get_enabled_rpc_endpoints():
    return [endpoint for endpoint in RPC_ENDPOINTS if endpoint.get("enabled", False)]


def get_enabled_relayers():
    return [relayer for relayer in RELAYER_ENDPOINTS if relayer.get("enabled", False)]


def get_enabled_dexes():
    return [name for name, meta in DEX_METADATA.items() if meta.get("enabled", False)]


def get_strategy_weight(strategy):
    return STRATEGY_WEIGHTS.get(strategy, 1)


def get_profit_range(strategy):
    return PROFIT_RANGES.get(strategy, (0.03, 0.18))


def get_token_metadata(token):
    return TOKEN_METADATA.get(
        token,
        {"category": "unknown", "min_depth_usd": 50000, "max_slippage_bps": 120},
    )


def get_status_label(status):
    return STATUS_LABELS.get(status, str(status).upper())


def get_action_templates(strategy):
    return ACTION_TEMPLATES.get(strategy, ["Route opportunity {token}"])


def get_market_window(name):
    return MARKET_WINDOWS.get(name, MARKET_WINDOWS["short"])


def get_wallet_group(name):
    return WALLET_GROUPS.get(name, WALLET_GROUPS["secondary"])