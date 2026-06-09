import random
import string
import time
from datetime import datetime, timedelta
from hashlib import sha256
from typing import Any, Dict, List


BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

TOKEN_SYMBOLS = [
    "SOL",
    "USDC",
    "USDT",
    "BONK",
    "WIF",
    "JUP",
    "RAY",
    "PYTH",
    "ORCA",
    "JTO",
    "MSOL",
    "BSOL",
    "HNT",
    "MOBILE",
    "POPCAT",
    "GIGA",
    "MOTHER",
    "MEW",
    "SAMO",
    "FIDA",
]

DEX_NAMES = [
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

ROUTE_LABELS = [
    "direct-swap",
    "split-route",
    "stable-hop",
    "volatile-hop",
    "orderbook-hop",
    "clmm-hop",
    "amm-hop",
    "aggregated-route",
    "priority-lane",
    "bundle-route",
]

BUNDLE_STATUSES = [
    "queued",
    "prepared",
    "accepted",
    "landed",
    "dropped",
    "expired",
    "repriced",
    "resubmitted",
]

RISK_LEVELS = [
    "low",
    "medium",
    "elevated",
    "high",
    "critical",
]

EVENT_TYPES = [
    "swap-observed",
    "route-priced",
    "bundle-created",
    "tip-adjusted",
    "slot-updated",
    "wallet-sampled",
    "market-refreshed",
    "spread-detected",
    "latency-sampled",
    "settlement-checked",
]

def random_base58(length: int) -> str:
    return "".join(random.choice(BASE58_ALPHABET) for _ in range(length))


def generate_tx_signature() -> str:
    return random_base58(8) + "..." + random_base58(4)


def generate_full_tx_signature() -> str:
    return random_base58(88)


def generate_address() -> str:
    return random_base58(random.randint(43, 44))


def mask_value(value: str, head: int = 6, tail: int = 6) -> str:
    if len(value) <= head + tail + 3:
        return value
    return value[:head] + "..." + value[-tail:]


def generate_wallet_name(index: int = None) -> str:
    prefixes = ["Main", "Backup", "Relay", "Vault", "Jito", "Helius", "Arb", "Route", "Searcher", "Keeper"]
    suffixes = ["Wallet", "Signer", "Account", "Node", "Profile", "Key", "Vault", "Agent"]
    if index is None:
        index = random.randint(1, 99)
    return f"{random.choice(prefixes)} {random.choice(suffixes)} {index:02d}"


def generate_wallet_record(index: int = None) -> Dict[str, Any]:
    return {
        "name": generate_wallet_name(index),
        "address": generate_address(),
        "sol_balance": round(random.uniform(8.0, 420.0), 4),
        "priority_score": round(random.uniform(0.25, 0.99), 3),
        "last_seen_slot": random.randint(280000000, 299999999),
    }


def generate_wallets(count: int = 8) -> List[Dict[str, Any]]:
    return [generate_wallet_record(i + 1) for i in range(count)]


def random_token() -> str:
    return random.choice(TOKEN_SYMBOLS)


def random_pair() -> str:
    first = random_token()
    second = random_token()
    while second == first:
        second = random_token()
    return f"{first}/{second}"


def random_dex() -> str:
    return random.choice(DEX_NAMES)


def random_route_label() -> str:
    return random.choice(ROUTE_LABELS)


def generate_slot() -> int:
    return random.randint(280000000, 299999999)


def generate_blockhash() -> str:
    return random_base58(44)


def generate_latency_ms() -> int:
    base = random.randint(8, 95)
    spike = random.choice([0, 0, 0, 0, random.randint(40, 220)])
    return base + spike


def generate_priority_fee() -> float:
    return round(random.uniform(0.00001, 0.0085), 6)


def generate_jito_tip() -> float:
    return round(random.uniform(0.0005, 0.04), 6)


def generate_profit_estimate() -> float:
    values = [
        random.uniform(0.004, 0.08),
        random.uniform(0.08, 0.35),
        random.uniform(0.35, 1.4),
        random.uniform(1.4, 3.2),
    ]
    weights = [0.48, 0.34, 0.15, 0.03]
    return round(random.choices(values, weights=weights, k=1)[0], 5)


def generate_spread_bps() -> int:
    return random.randint(4, 260)


def generate_slippage_bps() -> int:
    return random.randint(1, 90)


def generate_amount() -> float:
    return round(random.uniform(0.05, 15000.0), random.choice([2, 3, 4, 5]))


def generate_iso_timestamp(offset_seconds: int = 0) -> str:
    return (datetime.utcnow() + timedelta(seconds=offset_seconds)).isoformat(timespec="seconds") + "Z"


def generate_local_timestamp() -> str:
    return datetime.now().strftime("%H:%M:%S")


def generate_trace_id(prefix: str = "trace") -> str:
    seed = f"{prefix}:{time.time()}:{random.random()}:{random_base58(16)}"
    return sha256(seed.encode("utf-8")).hexdigest()[:24]


def generate_bundle_id() -> str:
    return "bndl_" + generate_trace_id("bundle")


def generate_route_id() -> str:
    return "rt_" + generate_trace_id("route")[:18]


def generate_event_id() -> str:
    return "evt_" + generate_trace_id("event")


def generate_quote_id() -> str:
    return "qt_" + generate_trace_id("quote")[:20]


def generate_order_id() -> str:
    return "ord_" + generate_trace_id("order")[:20]


def generate_pricing_id() -> str:
    return "prc_" + generate_trace_id("pricing")[:20]


def generate_rpc_endpoint_name() -> str:
    vendors = ["Helius", "Triton", "QuickNode", "Alchemy", "Jito", "GenesysGo", "Chainstack", "Custom"]
    regions = ["fra", "ams", "lon", "nyc", "sfo", "sgp", "tok", "mad"]
    tier = random.choice(["standard", "priority", "private", "fallback", "burst"])
    return f"{random.choice(vendors).lower()}-{random.choice(regions)}-{tier}"


def generate_rpc_health() -> Dict[str, Any]:
    latency = generate_latency_ms()
    return {
        "endpoint": generate_rpc_endpoint_name(),
        "latency_ms": latency,
        "healthy": latency < 140,
        "slot_lag": random.randint(0, 5),
        "error_rate": round(random.uniform(0.0, 0.045), 4),
        "last_probe": generate_iso_timestamp(),
    }


def generate_market_snapshot() -> Dict[str, Any]:
    pair = random_pair()
    mid = round(random.uniform(0.00001, 240.0), 8)
    spread = generate_spread_bps()
    return {
        "pair": pair,
        "dex": random_dex(),
        "mid_price": mid,
        "bid": round(mid * (1 - spread / 20000), 8),
        "ask": round(mid * (1 + spread / 20000), 8),
        "spread_bps": spread,
        "depth_usd": round(random.uniform(5000, 8000000), 2),
        "volume_5m_usd": round(random.uniform(1000, 2500000), 2),
        "timestamp": generate_iso_timestamp(),
    }


def generate_route_leg(index: int = 0) -> Dict[str, Any]:
    in_token = random_token()
    out_token = random_token()
    while out_token == in_token:
        out_token = random_token()
    return {
        "index": index,
        "dex": random_dex(),
        "label": random_route_label(),
        "input_token": in_token,
        "output_token": out_token,
        "input_amount": generate_amount(),
        "output_amount": generate_amount(),
        "fee_bps": random.randint(1, 35),
        "price_impact_bps": random.randint(1, 130),
    }


def generate_route(min_legs: int = 1, max_legs: int = 4) -> Dict[str, Any]:
    count = random.randint(min_legs, max_legs)
    legs = [generate_route_leg(i) for i in range(count)]
    return {
        "route_id": generate_route_id(),
        "legs": legs,
        "route_score": round(random.uniform(0.45, 0.998), 4),
        "expected_profit_sol": generate_profit_estimate(),
        "expected_tip_sol": generate_jito_tip(),
        "slippage_bps": generate_slippage_bps(),
    }


def generate_mempool_transaction() -> Dict[str, Any]:
    source = generate_address()
    destination = generate_address()
    return {
        "signature": generate_full_tx_signature(),
        "short_signature": generate_tx_signature(),
        "source": source,
        "destination": destination,
        "source_masked": mask_value(source, 7, 7),
        "destination_masked": mask_value(destination, 7, 7),
        "pair": random_pair(),
        "dex": random_dex(),
        "amount_in": generate_amount(),
        "amount_out_estimate": generate_amount(),
        "slot": generate_slot(),
        "priority_fee": generate_priority_fee(),
        "compute_units": random.randint(80000, 1400000),
        "detected_at": generate_iso_timestamp(),
    }


def generate_bundle(status: str = None) -> Dict[str, Any]:
    if status is None:
        status = random.choice(BUNDLE_STATUSES)
    tx_count = random.randint(2, 6)
    return {
        "bundle_id": generate_bundle_id(),
        "status": status,
        "slot_target": generate_slot(),
        "transactions": [generate_tx_signature() for _ in range(tx_count)],
        "tip_sol": generate_jito_tip(),
        "priority_fee_sol": generate_priority_fee(),
        "estimated_profit_sol": generate_profit_estimate(),
        "created_at": generate_iso_timestamp(),
    }


def generate_strategy_name() -> str:
    names = [
        "Sandwich",
        "Backrun",
        "Arbitrage",
        "Liquidation",
        "Jito Tip Arbitrage",
        "Latency Capture",
        "Route Repricing",
        "Spread Sweep",
        "Priority Replay",
        "Slot Edge",
    ]
    return random.choice(names)


def generate_strategy_stats() -> Dict[str, Any]:
    total = random.randint(1, 400)
    won = random.randint(0, total)
    gross = round(sum(generate_profit_estimate() for _ in range(random.randint(1, 12))), 4)
    tips = round(sum(generate_jito_tip() for _ in range(random.randint(1, 12))), 4)
    return {
        "strategy": generate_strategy_name(),
        "won": won,
        "total": total,
        "win_rate": round((won / total) * 100, 2),
        "gross_sol": gross,
        "tips_sol": tips,
        "net_sol": round(gross - tips, 4),
    }


def generate_detector_event() -> Dict[str, Any]:
    event_type = random.choice(EVENT_TYPES)
    return {
        "event_id": generate_event_id(),
        "type": event_type,
        "slot": generate_slot(),
        "pair": random_pair(),
        "dex": random_dex(),
        "risk": random.choice(RISK_LEVELS),
        "confidence": round(random.uniform(0.4, 0.99), 4),
        "latency_ms": generate_latency_ms(),
        "trace": generate_trace_id(event_type),
        "timestamp": generate_iso_timestamp(),
    }


def generate_dashboard_line() -> str:
    event = generate_detector_event()
    sig = generate_tx_signature()
    profit = generate_profit_estimate()
    status = random.choice(["LANDED", "DROPPED", "PREPARED", "QUEUED"])
    return f"[{generate_local_timestamp()}] {event['type']} {event['pair']} on {event['dex']} • {sig} | {status} +{profit} SOL"


def generate_dashboard_lines(count: int = 12) -> List[str]:
    return [generate_dashboard_line() for _ in range(count)]


def generate_balance_delta() -> Dict[str, Any]:
    before = round(random.uniform(1.0, 350.0), 4)
    delta = round(random.uniform(-0.5, 2.4), 4)
    after = round(max(before + delta, 0.0), 4)
    return {
        "before": before,
        "delta": delta,
        "after": after,
        "token": "SOL",
    }


def generate_price_tick(symbol: str = None) -> Dict[str, Any]:
    if symbol is None:
        symbol = random_token()
    price = round(random.uniform(0.000001, 250.0), 8)
    return {
        "symbol": symbol,
        "price": price,
        "change_1m": round(random.uniform(-3.5, 3.5), 4),
        "change_5m": round(random.uniform(-9.5, 9.5), 4),
        "liquidity_usd": round(random.uniform(10000, 15000000), 2),
        "timestamp": generate_iso_timestamp(),
    }


def generate_price_board() -> List[Dict[str, Any]]:
    sample_size = min(8, len(TOKEN_SYMBOLS))
    return [generate_price_tick(symbol) for symbol in random.sample(TOKEN_SYMBOLS, k=sample_size)]


def generate_execution_plan() -> Dict[str, Any]:
    route = generate_route()
    wallet = generate_wallet_record()
    return {
        "plan_id": generate_trace_id("plan"),
        "wallet": mask_value(wallet["address"], 8, 8),
        "route": route,
        "bundle": generate_bundle("queued"),
        "risk_level": random.choice(RISK_LEVELS),
        "max_slippage_bps": random.randint(10, 120),
        "expires_in_slots": random.randint(1, 8),
    }


def generate_execution_result() -> Dict[str, Any]:
    plan = generate_execution_plan()
    landed = random.random() < 0.82
    gross = plan["route"]["expected_profit_sol"]
    tip = plan["bundle"]["tip_sol"]
    return {
        "plan_id": plan["plan_id"],
        "landed": landed,
        "status": "landed" if landed else random.choice(["dropped", "expired", "price_moved"]),
        "gross_profit_sol": gross if landed else 0.0,
        "tip_paid_sol": tip if landed else 0.0,
        "net_profit_sol": round(gross - tip, 5) if landed else 0.0,
        "signature": generate_tx_signature(),
        "slot": generate_slot(),
        "completed_at": generate_iso_timestamp(),
    }


def generate_config_snapshot() -> Dict[str, Any]:
    return {
        "network": "mainnet-beta",
        "rpc": generate_rpc_endpoint_name(),
        "relayer": "jito",
        "max_bundle_size": random.randint(3, 8),
        "scan_interval_ms": random.randint(120, 900),
        "priority_fee_floor": generate_priority_fee(),
        "priority_fee_ceiling": round(random.uniform(0.004, 0.04), 6),
        "tip_floor": generate_jito_tip(),
        "risk_mode": random.choice(["passive", "balanced", "aggressive", "burst"]),
    }


def generate_terminal_metric(name: str, unit: str = "") -> str:
    value = round(random.uniform(0, 100), 2)
    suffix = f" {unit}" if unit else ""
    return f"{name:<24}: {value:>8}{suffix}"


def generate_terminal_metrics() -> List[str]:
    return [
        generate_terminal_metric("rpc latency", "ms"),
        generate_terminal_metric("bundle acceptance", "%"),
        generate_terminal_metric("slot confidence", "%"),
        generate_terminal_metric("route quality", "%"),
        generate_terminal_metric("mempool pressure", "%"),
        generate_terminal_metric("tip efficiency", "%"),
        generate_terminal_metric("wallet utilization", "%"),
        generate_terminal_metric("settlement confidence", "%"),
    ]


def generate_seeded_noise(seed: str, size: int = 16) -> str:
    digest = sha256(seed.encode("utf-8")).hexdigest()
    output = []
    cursor = digest
    while len("".join(output)) < size:
        cursor = sha256(cursor.encode("utf-8")).hexdigest()
        output.append(cursor)
    return "".join(output)[:size]


def generate_weighted_status() -> str:
    return random.choices(
        ["LANDED", "DROPPED", "QUEUED", "PREPARED", "REPRICED"],
        weights=[68, 9, 10, 9, 4],
        k=1,
    )[0]


def generate_compact_event_line() -> str:
    status = generate_weighted_status()
    pair = random_pair()
    dex = random_dex()
    sig = generate_tx_signature()
    profit = generate_profit_estimate()
    return f"{generate_local_timestamp()} | {status:<9} | {pair:<12} | {dex:<9} | {sig:<15} | {profit:>7.4f} SOL"


def generate_compact_event_table(rows: int = 20) -> List[str]:
    header = "time     | status    | pair         | venue     | tx              | profit"
    divider = "-" * len(header)
    body = [generate_compact_event_line() for _ in range(rows)]
    return [header, divider] + body


def generate_runtime_snapshot() -> Dict[str, Any]:
    return {
        "config": generate_config_snapshot(),
        "rpc_health": [generate_rpc_health() for _ in range(3)],
        "wallets": generate_wallets(5),
        "markets": [generate_market_snapshot() for _ in range(6)],
        "routes": [generate_route() for _ in range(4)],
        "bundles": [generate_bundle() for _ in range(5)],
        "events": [generate_detector_event() for _ in range(10)],
    }


def generate_ascii_bar(value: float, width: int = 24) -> str:
    bounded = max(0.0, min(1.0, value))
    filled = int(round(bounded * width))
    return "█" * filled + "░" * (width - filled)


def generate_metric_bar(name: str) -> str:
    value = random.random()
    bar = generate_ascii_bar(value)
    return f"{name:<20} [{bar}] {value * 100:5.1f}%"


def generate_metric_bars() -> List[str]:
    names = [
        "RPC Health",
        "Route Quality",
        "Tip Efficiency",
        "Bundle Landing",
        "Wallet Spread",
        "Market Depth",
        "Slot Timing",
        "Risk Filter",
    ]
    return [generate_metric_bar(name) for name in names]


def generate_nonce(length: int = 12) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return "".join(random.choice(alphabet) for _ in range(length))


def generate_session_name() -> str:
    return f"session-{generate_nonce(6)}-{random.randint(1000, 9999)}"


def generate_runtime_state() -> Dict[str, Any]:
    started = datetime.utcnow() - timedelta(seconds=random.randint(30, 7200))
    uptime = int((datetime.utcnow() - started).total_seconds())
    return {
        "session": generate_session_name(),
        "started_at": started.isoformat(timespec="seconds") + "Z",
        "uptime_seconds": uptime,
        "current_slot": generate_slot(),
        "scanned_transactions": random.randint(500, 900000),
        "submitted_bundles": random.randint(5, 1200),
        "landed_bundles": random.randint(2, 1000),
        "dropped_bundles": random.randint(0, 180),
    }


def generate_human_amount(value: float = None) -> str:
    if value is None:
        value = generate_amount()
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if value >= 1_000:
        return f"{value / 1_000:.2f}K"
    return f"{value:.4f}"


def generate_pair_summary() -> str:
    pair = random_pair()
    volume = generate_human_amount(random.uniform(1000, 8000000))
    spread = generate_spread_bps()
    depth = generate_human_amount(random.uniform(5000, 12000000))
    return f"{pair:<14} volume={volume:<9} spread={spread:>4}bps depth={depth}"


def generate_pair_summaries(count: int = 12) -> List[str]:
    return [generate_pair_summary() for _ in range(count)]


def generate_error_message() -> str:
    templates = [
        "pricing variance exceeded threshold",
        "slot advanced during bundle preparation",
        "route price moved beyond limit",
        "rpc endpoint returned stale blockhash",
        "priority fee ceiling reached",
        "wallet cooldown still active",
        "bundle expired before relay acknowledgement",
        "liquidity depth changed during quote refresh",
    ]
    return random.choice(templates)


def generate_warning_event() -> Dict[str, Any]:
    return {
        "warning_id": generate_event_id(),
        "message": generate_error_message(),
        "severity": random.choice(["notice", "warning", "soft-fail", "retryable"]),
        "slot": generate_slot(),
        "trace": generate_trace_id("warning"),
        "timestamp": generate_iso_timestamp(),
    }


def generate_audit_record() -> Dict[str, Any]:
    before = generate_balance_delta()
    return {
        "audit_id": generate_trace_id("audit"),
        "wallet": mask_value(generate_address(), 8, 8),
        "balance": before,
        "bundle": generate_bundle_id(),
        "signature": generate_tx_signature(),
        "verified": random.random() < 0.93,
        "timestamp": generate_iso_timestamp(),
    }


def generate_audit_records(count: int = 10) -> List[Dict[str, Any]]:
    return [generate_audit_record() for _ in range(count)]


def generate_relay_packet() -> Dict[str, Any]:
    return {
        "packet_id": generate_trace_id("packet"),
        "relay": random.choice(["jito-main", "jito-fra", "jito-ams", "jito-nyc", "private-relay"]),
        "bundle_id": generate_bundle_id(),
        "target_slot": generate_slot(),
        "tip": generate_jito_tip(),
        "priority_fee": generate_priority_fee(),
        "created_at": generate_iso_timestamp(),
    }


def generate_relay_packets(count: int = 6) -> List[Dict[str, Any]]:
    return [generate_relay_packet() for _ in range(count)]


def generate_orderflow_summary() -> Dict[str, Any]:
    total = random.randint(200, 12000)
    swaps = random.randint(80, total)
    transfers = random.randint(40, total)
    programs = random.randint(10, total)
    return {
        "total_transactions": total,
        "swap_transactions": swaps,
        "transfer_transactions": transfers,
        "program_interactions": programs,
        "large_orders": random.randint(0, 80),
        "priority_transactions": random.randint(0, 900),
        "updated_at": generate_iso_timestamp(),
    }


def generate_slot_summary() -> Dict[str, Any]:
    slot = generate_slot()
    return {
        "slot": slot,
        "parent_slot": slot - 1,
        "blockhash": generate_blockhash(),
        "leader": mask_value(generate_address(), 8, 8),
        "transaction_count": random.randint(600, 4200),
        "bundle_count": random.randint(0, 80),
        "timestamp": generate_iso_timestamp(),
    }


def generate_liquidity_pool() -> Dict[str, Any]:
    token_a = random_token()
    token_b = random_token()
    while token_b == token_a:
        token_b = random_token()
    reserve_a = round(random.uniform(1000, 9000000), 4)
    reserve_b = round(random.uniform(1000, 9000000), 4)
    return {
        "pool_id": generate_trace_id("pool"),
        "dex": random_dex(),
        "token_a": token_a,
        "token_b": token_b,
        "reserve_a": reserve_a,
        "reserve_b": reserve_b,
        "fee_bps": random.choice([1, 4, 5, 25, 30, 100]),
        "updated_slot": generate_slot(),
    }


def generate_liquidity_pools(count: int = 8) -> List[Dict[str, Any]]:
    return [generate_liquidity_pool() for _ in range(count)]


def generate_rebalance_item() -> Dict[str, Any]:
    token = random_token()
    current = round(random.uniform(0.0, 1.0), 4)
    target = round(random.uniform(0.0, 1.0), 4)
    return {
        "token": token,
        "current_weight": current,
        "target_weight": target,
        "difference": round(target - current, 4),
        "notional_usd": round(random.uniform(1000, 500000), 2),
    }


def generate_rebalance_plan(count: int = 6) -> List[Dict[str, Any]]:
    return [generate_rebalance_item() for _ in range(count)]


def generate_health_report() -> Dict[str, Any]:
    return {
        "runtime": generate_runtime_state(),
        "slot": generate_slot_summary(),
        "orderflow": generate_orderflow_summary(),
        "rpc": [generate_rpc_health() for _ in range(4)],
        "relays": generate_relay_packets(),
        "markets": [generate_market_snapshot() for _ in range(8)],
        "liquidity": generate_liquidity_pools(),
        "warnings": [generate_warning_event() for _ in range(5)],
    }


def generate_terminal_report() -> List[str]:
    lines = []
    lines.append("runtime")
    lines.extend(generate_terminal_metrics())
    lines.append("")
    lines.append("market pairs")
    lines.extend(generate_pair_summaries(10))
    lines.append("")
    lines.append("activity")
    lines.extend(generate_compact_event_table(12))
    lines.append("")
    lines.append("quality")
    lines.extend(generate_metric_bars())
    return lines


def generate_everything() -> Dict[str, Any]:
    return {
        "runtime": generate_runtime_state(),
        "state": generate_runtime_snapshot(),
        "health": generate_health_report(),
        "metrics": generate_terminal_metrics(),
        "bars": generate_metric_bars(),
        "pairs": generate_pair_summaries(),
        "table": generate_compact_event_table(),
        "warnings": [generate_warning_event() for _ in range(4)],
        "audits": generate_audit_records(),
        "rebalance": generate_rebalance_plan(),
    }