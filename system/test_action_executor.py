from payment_simulator import generate_transaction, SYSTEM_STATE
from state_tracker import StateTracker
from agent_system import AgentBrain
from policy_engine import PolicyEngine
from action_executor import ActionExecutor
import time

tracker = StateTracker(window_size=30)
brain = AgentBrain()
policy = PolicyEngine()
executor = ActionExecutor()

# Break HDFC badly
SYSTEM_STATE["HDFC_failure_multiplier"] = 6.0

while True:
    txn = generate_transaction()
    tracker.ingest(txn)

    state = tracker.get_state()
    reasoning = brain.reason(state)
    decision = policy.decide(reasoning)
    result = executor.execute(decision)

    print("\nSYSTEM_STATE:", SYSTEM_STATE)
    print("STATE:", state)
    print("REASONING:", reasoning)
    print("DECISION:", decision)
    print("ACTION RESULT:", result)

    time.sleep(2)
