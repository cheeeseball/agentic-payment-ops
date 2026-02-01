from payment_simulator import generate_transaction
from state_tracker import StateTracker
import time

tracker = StateTracker(window_size=20)

while True:
    txn = generate_transaction()
    tracker.ingest(txn)
    print(tracker.get_state())
    time.sleep(1)
