from payment_simulator import generate_transaction
from state_tracker import StateTracker
from agent_system import AgentBrain
from policy_engine import PolicyEngine
import time

tracker = StateTracker(window_size=30)
brain = AgentBrain()
policy = PolicyEngine()

while True:
    txn = generate_transaction()
    tracker.ingest(txn)

    state = tracker.get_state()
    reasoning = brain.reason(state)
    decision = policy.decide(reasoning)

    print("\nSTATE:", state)
    print("REASONING:", reasoning)
    print("DECISION:", decision)

    time.sleep(2)
