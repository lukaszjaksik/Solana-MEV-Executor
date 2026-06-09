import json
import os
import random
import time
from datetime import datetime
from hashlib import sha256
from typing import Any, Dict, List, Optional, Tuple


class WalletManager:
    def __init__(self, wallet_file: str = "wallet.json"):
        self.wallet_file = wallet_file
        self.wallets = []
        self.wallet_balances = {}
        self.wallet_index = {}
        self.wallet_activity = {}
        self.wallet_groups = {}
        self.last_loaded_at = None
        self.last_updated_at = None
        self.load_wallets()

    def mask_address(self, address: str) -> str:
        if not address:
            return ""
        if len(address) <= 24:
            return address
        return address[:8] + "..." + address[-8:]

    def load_wallets(self):
        if not os.path.exists(self.wallet_file):
            print("\033[91mERROR: wallet.json not found!\033[0m")
            print("Please create wallet.json in the same folder as main.py")
            exit(1)

        try:
            with open(self.wallet_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.wallets = data.get("wallets", [])
            if not isinstance(self.wallets, list):
                self.wallets = []

            self.wallet_balances = {}
            self.wallet_index = {}
            self.wallet_activity = {}
            self.wallet_groups = {}

            for idx, wallet in enumerate(self.wallets):
                self._normalize_wallet(wallet, idx)
                address = wallet["address"]
                self.wallet_balances[address] = wallet.get(
                    "sol_balance",
                    round(random.uniform(80, 320), 4),
                )
                self.wallet_index[address] = idx
                self.wallet_activity[address] = []
                self.wallet_groups[address] = wallet.get("group", self._derive_group(idx))

            self.last_loaded_at = time.time()
            self.last_updated_at = self.last_loaded_at

        except Exception as e:
            print(f"\033[91mError loading wallet.json: {e}\033[0m")
            exit(1)

    def _normalize_wallet(self, wallet: Dict[str, Any], index: int):
        if "name" not in wallet or not wallet["name"]:
            wallet["name"] = f"Wallet {index + 1:02d}"

        if "address" not in wallet or not wallet["address"]:
            wallet["address"] = self._generate_address(index)

        if "sol_balance" not in wallet:
            wallet["sol_balance"] = round(random.uniform(80, 320), 4)

        if "enabled" not in wallet:
            wallet["enabled"] = True

        if "priority" not in wallet:
            wallet["priority"] = max(1, 100 - index * 5)

        if "group" not in wallet:
            wallet["group"] = self._derive_group(index)

    def _derive_group(self, index: int) -> str:
        if index == 0:
            return "primary"
        if index == 1:
            return "secondary"
        if index == 2:
            return "vault"
        return "backup"

    def _generate_address(self, index: int) -> str:
        alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        seed = f"{index}:{time.time()}:{random.random()}"
        digest = sha256(seed.encode("utf-8")).hexdigest()
        rng = random.Random(digest)
        return "".join(rng.choice(alphabet) for _ in range(44))

    def reload(self):
        self.load_wallets()

    def save_wallets(self) -> bool:
        try:
            output = {"wallets": []}
            for wallet in self.wallets:
                address = wallet["address"]
                item = dict(wallet)
                item["sol_balance"] = round(self.wallet_balances.get(address, 0.0), 4)
                output["wallets"].append(item)

            with open(self.wallet_file, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2)

            self.last_updated_at = time.time()
            return True
        except Exception:
            return False

    def get_wallet_count(self) -> int:
        return len(self.wallets)

    def has_wallets(self) -> bool:
        return len(self.wallets) > 0

    def get_enabled_wallets(self) -> List[Dict[str, Any]]:
        return [wallet for wallet in self.wallets if wallet.get("enabled", True)]

    def get_wallet_by_address(self, address: str) -> Optional[Dict[str, Any]]:
        index = self.wallet_index.get(address)
        if index is None:
            return None
        if index < 0 or index >= len(self.wallets):
            return None
        return self.wallets[index]

    def get_wallet_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        name_lower = name.lower()
        for wallet in self.wallets:
            if wallet.get("name", "").lower() == name_lower:
                return wallet
        return None

    def get_primary_wallet(self) -> Optional[Dict[str, Any]]:
        enabled = self.get_enabled_wallets()
        if not enabled:
            return None
        return sorted(enabled, key=lambda item: item.get("priority", 0), reverse=True)[0]

    def get_random_wallet(self) -> Optional[Dict[str, Any]]:
        enabled = self.get_enabled_wallets()
        if not enabled:
            return None
        return random.choice(enabled)

    def get_weighted_wallet(self) -> Optional[Dict[str, Any]]:
        enabled = self.get_enabled_wallets()
        if not enabled:
            return None

        weights = []
        for wallet in enabled:
            address = wallet["address"]
            balance = self.wallet_balances.get(address, 0.0)
            priority = wallet.get("priority", 1)
            weight = max(balance, 0.01) * max(priority, 1)
            weights.append(weight)

        return random.choices(enabled, weights=weights, k=1)[0]

    def get_wallet_balance(self, address: str) -> float:
        return round(self.wallet_balances.get(address, 0.0), 4)

    def get_total_balance(self) -> float:
        total = sum(self.wallet_balances.values())
        return round(total, 4)

    def get_average_balance(self) -> float:
        if not self.wallet_balances:
            return 0.0
        return round(self.get_total_balance() / len(self.wallet_balances), 4)

    def get_min_balance_wallet(self) -> Optional[Dict[str, Any]]:
        if not self.wallets:
            return None
        return min(self.wallets, key=lambda wallet: self.wallet_balances.get(wallet["address"], 0.0))

    def get_max_balance_wallet(self) -> Optional[Dict[str, Any]]:
        if not self.wallets:
            return None
        return max(self.wallets, key=lambda wallet: self.wallet_balances.get(wallet["address"], 0.0))

    def set_wallet_balance(self, address: str, balance: float):
        if address in self.wallet_index:
            self.wallet_balances[address] = round(max(balance, 0.0), 4)
            self._touch_wallet(address, "balance_set", balance)
            self.last_updated_at = time.time()

    def adjust_wallet_balance(self, address: str, delta: float):
        if address not in self.wallet_index:
            return
        current = self.wallet_balances.get(address, 0.0)
        next_balance = round(max(current + delta, 0.0), 4)
        self.wallet_balances[address] = next_balance
        self._touch_wallet(address, "balance_adjusted", delta)
        self.last_updated_at = time.time()

    def add_profit_to_random_wallet(self, profit: float):
        target = self.get_weighted_wallet()
        if target:
            address = target["address"]
            self.wallet_balances[address] = round(self.wallet_balances.get(address, 0.0) + profit, 4)
            self._touch_wallet(address, "profit_added", profit)
            self.last_updated_at = time.time()

    def remove_cost_from_random_wallet(self, cost: float) -> Optional[str]:
        target = self.get_weighted_wallet()
        if not target:
            return None

        address = target["address"]
        current = self.wallet_balances.get(address, 0.0)
        self.wallet_balances[address] = round(max(current - cost, 0.0), 4)
        self._touch_wallet(address, "cost_removed", cost)
        self.last_updated_at = time.time()
        return address

    def transfer_balance(self, source_address: str, target_address: str, amount: float) -> bool:
        if source_address not in self.wallet_index:
            return False
        if target_address not in self.wallet_index:
            return False
        if amount <= 0:
            return False

        source_balance = self.wallet_balances.get(source_address, 0.0)
        if source_balance < amount:
            return False

        self.wallet_balances[source_address] = round(source_balance - amount, 4)
        self.wallet_balances[target_address] = round(self.wallet_balances.get(target_address, 0.0) + amount, 4)
        self._touch_wallet(source_address, "transfer_out", amount)
        self._touch_wallet(target_address, "transfer_in", amount)
        self.last_updated_at = time.time()
        return True

    def rebalance_wallets(self, min_balance: float = 25.0) -> List[Dict[str, Any]]:
        actions = []
        if len(self.wallets) < 2:
            return actions

        high = self.get_max_balance_wallet()
        low = self.get_min_balance_wallet()
        if not high or not low:
            return actions

        high_address = high["address"]
        low_address = low["address"]
        high_balance = self.wallet_balances.get(high_address, 0.0)
        low_balance = self.wallet_balances.get(low_address, 0.0)

        if low_balance >= min_balance:
            return actions

        amount = round(min((high_balance - min_balance) * 0.25, min_balance - low_balance), 4)
        if amount <= 0:
            return actions

        moved = self.transfer_balance(high_address, low_address, amount)
        if moved:
            actions.append(
                {
                    "source": self.mask_address(high_address),
                    "target": self.mask_address(low_address),
                    "amount": amount,
                    "timestamp": self._timestamp(),
                }
            )

        return actions

    def enable_wallet(self, address: str) -> bool:
        wallet = self.get_wallet_by_address(address)
        if not wallet:
            return False
        wallet["enabled"] = True
        self._touch_wallet(address, "enabled", 1)
        return True

    def disable_wallet(self, address: str) -> bool:
        wallet = self.get_wallet_by_address(address)
        if not wallet:
            return False
        wallet["enabled"] = False
        self._touch_wallet(address, "disabled", 1)
        return True

    def rename_wallet(self, address: str, name: str) -> bool:
        wallet = self.get_wallet_by_address(address)
        if not wallet:
            return False
        wallet["name"] = name
        self._touch_wallet(address, "renamed", 1)
        return True

    def set_wallet_group(self, address: str, group: str) -> bool:
        wallet = self.get_wallet_by_address(address)
        if not wallet:
            return False
        wallet["group"] = group
        self.wallet_groups[address] = group
        self._touch_wallet(address, "group_changed", 1)
        return True

    def get_wallet_group(self, address: str) -> str:
        return self.wallet_groups.get(address, "secondary")

    def get_wallets_by_group(self, group: str) -> List[Dict[str, Any]]:
        result = []
        for wallet in self.wallets:
            address = wallet["address"]
            if self.wallet_groups.get(address, wallet.get("group", "secondary")) == group:
                result.append(wallet)
        return result

    def get_group_balances(self) -> Dict[str, float]:
        groups = {}
        for wallet in self.wallets:
            address = wallet["address"]
            group = self.get_wallet_group(address)
            groups[group] = groups.get(group, 0.0) + self.wallet_balances.get(address, 0.0)

        for group in list(groups.keys()):
            groups[group] = round(groups[group], 4)

        return groups

    def _touch_wallet(self, address: str, action: str, value: float):
        if address not in self.wallet_activity:
            self.wallet_activity[address] = []

        self.wallet_activity[address].append(
            {
                "action": action,
                "value": value,
                "balance": self.wallet_balances.get(address, 0.0),
                "timestamp": self._timestamp(),
            }
        )

        if len(self.wallet_activity[address]) > 50:
            self.wallet_activity[address] = self.wallet_activity[address][-50:]

    def _timestamp(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_wallet_activity(self, address: str, limit: int = 10) -> List[Dict[str, Any]]:
        activity = self.wallet_activity.get(address, [])
        return activity[-limit:]

    def get_all_activity(self, limit: int = 25) -> List[Dict[str, Any]]:
        events = []
        for address, items in self.wallet_activity.items():
            for item in items:
                entry = dict(item)
                entry["address"] = self.mask_address(address)
                events.append(entry)

        events.sort(key=lambda item: item.get("timestamp", ""))
        return events[-limit:]

    def get_wallet_summary(self, address: str) -> Optional[Dict[str, Any]]:
        wallet = self.get_wallet_by_address(address)
        if not wallet:
            return None

        balance = self.wallet_balances.get(address, 0.0)
        activity = self.wallet_activity.get(address, [])
        return {
            "name": wallet.get("name", ""),
            "address": address,
            "masked_address": self.mask_address(address),
            "group": self.get_wallet_group(address),
            "enabled": wallet.get("enabled", True),
            "priority": wallet.get("priority", 0),
            "balance": round(balance, 4),
            "activity_count": len(activity),
            "last_activity": activity[-1] if activity else None,
        }

    def get_portfolio_summary(self) -> Dict[str, Any]:
        balances = list(self.wallet_balances.values())
        enabled_count = len(self.get_enabled_wallets())
        total = round(sum(balances), 4)
        average = round(total / len(balances), 4) if balances else 0.0
        minimum = round(min(balances), 4) if balances else 0.0
        maximum = round(max(balances), 4) if balances else 0.0

        return {
            "wallet_count": len(self.wallets),
            "enabled_count": enabled_count,
            "disabled_count": len(self.wallets) - enabled_count,
            "total_balance": total,
            "average_balance": average,
            "minimum_balance": minimum,
            "maximum_balance": maximum,
            "groups": self.get_group_balances(),
            "last_loaded_at": self.last_loaded_at,
            "last_updated_at": self.last_updated_at,
        }

    def format_wallet_table(self) -> List[str]:
        lines = []
        header = f"{'Name':<20} {'Group':<12} {'Address':<24} {'Balance':>12} {'Status':>10}"
        lines.append(header)
        lines.append("-" * len(header))

        for wallet in self.wallets:
            address = wallet["address"]
            name = wallet.get("name", "")
            group = self.get_wallet_group(address)
            masked = self.mask_address(address)
            balance = self.wallet_balances.get(address, 0.0)
            status = "enabled" if wallet.get("enabled", True) else "disabled"
            lines.append(f"{name:<20} {group:<12} {masked:<24} {balance:>12.4f} {status:>10}")

        return lines

    def print_wallet_table(self):
        for line in self.format_wallet_table():
            print(line)

    def export_public_state(self) -> Dict[str, Any]:
        return {
            "wallets": [
                {
                    "name": wallet.get("name", ""),
                    "address": self.mask_address(wallet.get("address", "")),
                    "group": self.get_wallet_group(wallet.get("address", "")),
                    "balance": self.wallet_balances.get(wallet.get("address", ""), 0.0),
                    "enabled": wallet.get("enabled", True),
                    "priority": wallet.get("priority", 0),
                }
                for wallet in self.wallets
            ],
            "summary": self.get_portfolio_summary(),
        }

    def export_private_state(self) -> Dict[str, Any]:
        return {
            "wallets": [
                {
                    "name": wallet.get("name", ""),
                    "address": wallet.get("address", ""),
                    "group": self.get_wallet_group(wallet.get("address", "")),
                    "balance": self.wallet_balances.get(wallet.get("address", ""), 0.0),
                    "enabled": wallet.get("enabled", True),
                    "priority": wallet.get("priority", 0),
                }
                for wallet in self.wallets
            ],
            "summary": self.get_portfolio_summary(),
            "activity": self.wallet_activity,
        }

    def import_balances(self, balances: Dict[str, float]) -> int:
        updated = 0
        for address, balance in balances.items():
            if address in self.wallet_index:
                self.wallet_balances[address] = round(max(float(balance), 0.0), 4)
                self._touch_wallet(address, "balance_imported", float(balance))
                updated += 1

        if updated:
            self.last_updated_at = time.time()

        return updated

    def estimate_allocation(self, amount: float) -> List[Dict[str, Any]]:
        enabled = self.get_enabled_wallets()
        if not enabled or amount <= 0:
            return []

        total_balance = sum(self.wallet_balances.get(wallet["address"], 0.0) for wallet in enabled)
        if total_balance <= 0:
            share = round(amount / len(enabled), 4)
            return [
                {
                    "address": self.mask_address(wallet["address"]),
                    "amount": share,
                    "weight": round(1 / len(enabled), 4),
                }
                for wallet in enabled
            ]

        plan = []
        for wallet in enabled:
            address = wallet["address"]
            balance = self.wallet_balances.get(address, 0.0)
            weight = balance / total_balance
            plan.append(
                {
                    "address": self.mask_address(address),
                    "amount": round(amount * weight, 4),
                    "weight": round(weight, 4),
                }
            )

        return plan

    def select_wallet_for_amount(self, amount: float) -> Optional[Dict[str, Any]]:
        candidates = []
        for wallet in self.get_enabled_wallets():
            address = wallet["address"]
            balance = self.wallet_balances.get(address, 0.0)
            if balance >= amount:
                candidates.append(wallet)

        if not candidates:
            return None

        candidates.sort(
            key=lambda wallet: (
                self.wallet_balances.get(wallet["address"], 0.0),
                wallet.get("priority", 0),
            )
        )
        return candidates[0]

    def reserve_amount(self, amount: float) -> Optional[Dict[str, Any]]:
        wallet = self.select_wallet_for_amount(amount)
        if not wallet:
            return None

        address = wallet["address"]
        self.adjust_wallet_balance(address, -amount)
        return {
            "wallet": wallet,
            "address": address,
            "masked_address": self.mask_address(address),
            "reserved": round(amount, 4),
            "remaining": self.wallet_balances.get(address, 0.0),
        }

    def release_amount(self, address: str, amount: float) -> bool:
        if address not in self.wallet_index:
            return False
        self.adjust_wallet_balance(address, amount)
        return True

    def apply_profit_distribution(self, profit: float, weights: Optional[Dict[str, float]] = None) -> List[Dict[str, Any]]:
        if profit <= 0:
            return []

        enabled = self.get_enabled_wallets()
        if not enabled:
            return []

        if not weights:
            weights = {}
            for wallet in enabled:
                address = wallet["address"]
                weights[address] = max(wallet.get("priority", 1), 1)

        weight_sum = sum(weights.get(wallet["address"], 0.0) for wallet in enabled)
        if weight_sum <= 0:
            weight_sum = len(enabled)
            weights = {wallet["address"]: 1 for wallet in enabled}

        results = []
        for wallet in enabled:
            address = wallet["address"]
            share = weights.get(address, 0.0) / weight_sum
            amount = round(profit * share, 4)
            if amount <= 0:
                continue
            self.adjust_wallet_balance(address, amount)
            results.append(
                {
                    "address": self.mask_address(address),
                    "amount": amount,
                    "share": round(share, 4),
                }
            )

        return results

    def build_balance_snapshot(self) -> Dict[str, Any]:
        snapshot = {
            "created_at": self._timestamp(),
            "total": self.get_total_balance(),
            "wallets": [],
        }

        for wallet in self.wallets:
            address = wallet["address"]
            snapshot["wallets"].append(
                {
                    "name": wallet.get("name", ""),
                    "address": self.mask_address(address),
                    "group": self.get_wallet_group(address),
                    "balance": self.wallet_balances.get(address, 0.0),
                    "enabled": wallet.get("enabled", True),
                }
            )

        return snapshot

    def validate_wallets(self) -> Tuple[bool, List[str]]:
        errors = []
        seen = set()

        for index, wallet in enumerate(self.wallets):
            name = wallet.get("name", "")
            address = wallet.get("address", "")

            if not name:
                errors.append(f"wallet {index + 1} has no name")

            if not address:
                errors.append(f"wallet {index + 1} has no address")

            if address in seen:
                errors.append(f"duplicate address {self.mask_address(address)}")

            seen.add(address)

            balance = self.wallet_balances.get(address, 0.0)
            if balance < 0:
                errors.append(f"wallet {self.mask_address(address)} has negative balance")

        return len(errors) == 0, errors

    def compact_state_line(self) -> str:
        summary = self.get_portfolio_summary()
        return (
            f"wallets={summary['wallet_count']} "
            f"enabled={summary['enabled_count']} "
            f"total={summary['total_balance']:.4f} SOL "
            f"avg={summary['average_balance']:.4f} SOL"
        )