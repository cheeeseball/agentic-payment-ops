from payment_simulator import generate_transaction
from state_tracker import StateTracker
from agent_system import AgentBrain
import time

tracker = StateTracker(window_size=30)
brain = AgentBrain()

while True:
    txn = generate_transaction()
    tracker.ingest(txn)

    state = tracker.get_state()
    reasoning = brain.reason(state)

    print("\nSTATE:", state)
    print("REASONING:", reasoning)

    time.sleep(2)
