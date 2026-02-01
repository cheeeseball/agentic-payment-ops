from collections import defaultdict, deque
import time

class StateTracker:
    def __init__(self, window_size=50):
        self.window_size = window_size
        self.transactions = deque(maxlen=window_size)
        self.metrics = defaultdict(dict)

    def ingest(self, txn):
        self.transactions.append(txn)
        self._recompute_metrics()

    def _recompute_metrics(self):
        issuer_stats = defaultdict(lambda: {"total": 0, "failed": 0, "latency": []})

        for txn in self.transactions:
            issuer = txn["issuer"]
            issuer_stats[issuer]["total"] += 1
            if txn["status"] == "FAILED":
                issuer_stats[issuer]["failed"] += 1
            issuer_stats[issuer]["latency"].append(txn["latency_ms"])

        for issuer, stats in issuer_stats.items():
            total = stats["total"]
            failed = stats["failed"]
            avg_latency = sum(stats["latency"]) / total

            self.metrics[issuer] = {
                "failure_rate": failed / total,
                "avg_latency": avg_latency,
                "total_txns": total
            }

    def get_state(self):
        return dict(self.metrics)
