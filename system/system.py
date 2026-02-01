# from payment_simulator import generate_transaction, SYSTEM_STATE
# from state_tracker import StateTracker
# from agent_system import AgentSystem
# from policy_engine import PolicyEngine
# from action_executor import ActionExecutor
# from learning_loop import LearningLoop
# import time
# import traceback

# import psycopg2

# def get_db_connection():
#     return psycopg2.connect(
#         host="localhost",
#         database="FirmPay",
#         user="postgres",
#         password="imaad@376"
#     )

# tracker = StateTracker(window_size=50)
# brain = AgentSystem()
# policy = PolicyEngine()
# executor = ActionExecutor()
# learner = LearningLoop()

# # Break system initially
# SYSTEM_STATE["HDFC_failure_multiplier"] = 6.0
# SYSTEM_STATE["ICICI_failure_multiplier"] = 1.0
# SYSTEM_STATE["SBI_failure_multiplier"] = 8.0
# SYSTEM_STATE["BOI_failure_multiplier"] = 1.0
# SYSTEM_STATE["AXIS_failure_multiplier"] = 4.0
# SYSTEM_STATE["INDUSIND_failure_multiplier"] = 1.0

# print("Starting Autonomous Payment Agent...\n")

# cycle = 0
# last_good_state = None

# def get_failure_multipliers():
#     conn = get_db_connection()
#     cur = conn.cursor()

#     cur.execute("SELECT name, system_multiplier FROM banks;")
#     rows = cur.fetchall()

#     cur.close()
#     conn.close()

#     return {name: multiplier for name, multiplier in rows}

# while True:
#     try:
#         cycle += 1
#         print(f"\n--- CYCLE {cycle} ---")

#         # 1. OBSERVE
#         try:
#             txn = generate_transaction()
#             tracker.ingest(txn)
#         except Exception as e:
#             print("❌ ERROR in simulator or tracker:", e)
#             traceback.print_exc()
#             time.sleep(1)
#             continue

#         # 2. PERCEPTION
#         try:
#             state = tracker.get_state()
#             if not state:
#                 raise ValueError("Empty state")
#         except Exception as e:
#             print("❌ ERROR getting state:", e)
#             traceback.print_exc()
#             time.sleep(3)
#             continue

#         # 3. REASON (LLM)
#         try:
#             reasoning = brain.reason(state)
#             if "recommended_actions" not in reasoning:
#                 raise ValueError("Invalid LLM output structure")
#         except Exception as e:
#             print("❌ ERROR in LLM reasoning:", e)
#             traceback.print_exc()
#             reasoning = {
#                 "recommended_actions": [
#                     {"action": "DO_NOTHING", "reason": "LLM failure"}
#                 ]
#             }

#         # 4. DECIDE
#         try:
#             decision = policy.decide(reasoning)
#             if "action" not in decision:
#                 raise ValueError("Invalid policy decision")
#         except Exception as e:
#             print("❌ ERROR in policy engine:", e)
#             traceback.print_exc()
#             decision = {"action": "DO_NOTHING"}

#         # 5. ACT
#         try:
#             result = executor.execute(decision)
#         except Exception as e:
#             print("❌ ERROR in action executor:", e)
#             traceback.print_exc()
#             result = "Action failed"

#         # 6. LEARN
#         try:
#             reward = learner.compute_reward(state)
#             learner.remember(state, decision["action"], reward)
#         except Exception as e:
#             print("❌ ERROR in learning loop:", e)
#             traceback.print_exc()
#             reward = 0

#         # LOGGING
#         multipliers = get_failure_multipliers()
#         print("FAILURE_MULTIPLIERS (from DB):", multipliers)

#         print("STATE:", state)
#         print("REASONING:", reasoning)
#         print("DECISION:", decision)
#         print("ACTION:", result)
#         print("REWARD:", reward)

#         # 7. SAFETY: ROLLBACK
#         try:
#             if learner.should_rollback():
#                 print("⚠️  ROLLING BACK: system degrading")
#                 SYSTEM_STATE.update(last_good_state)
#         except:
#             pass

#         # Save last good state
#         if reward > 0:
#             last_good_state = SYSTEM_STATE.copy()

#         time.sleep(2)

#     except KeyboardInterrupt:
#         print("\n🛑 AI Agent stopped by Ops Engineer.")
#         break

#     except Exception as e:
#         print("FATAL LOOP ERROR (recovering):", e)
#         traceback.print_exc()
#         time.sleep(1)


# system/system.py

print("Running main system loop")
from state_tracker import StateTracker
from agent_system import AgentSystem
from policy_engine import PolicyEngine
from action_executor import ActionExecutor
from learning_loop import LearningLoop
import psycopg2
import traceback
import time

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="FirmPay",
        user="postgres",
        password="imaad@376"
    )

def get_draft_transactions():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM drafts ORDER BY created_at ASC;")
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()

    drafts = [dict(zip(colnames, row)) for row in rows]
    return drafts



# 🔥 THIS IS THE ONLY REAL CHANGE
def run_agent_on_drafts():
    tracker = StateTracker(window_size=50)
    brain = AgentSystem()
    policy = PolicyEngine()
    executor = ActionExecutor()
    learner = LearningLoop()

    print("\n🚀 Starting Agent on Draft Payments...\n")

    drafts = get_draft_transactions()
    print(f"Loaded {len(drafts)} draft transactions.\n")

    cycle = 0

    for txn in drafts:
        try:
            cycle += 1
            print(f"\n--- PROCESSING TXN {cycle} ---")

            # 1. OBSERVE
            tracker.ingest(txn)

            # 2. PERCEPTION
            state = tracker.get_state()

            # 3. REASON
            reasoning = brain.reason(state)

            # 4. DECIDE
            decision = policy.decide(reasoning)

            # 5. ACT
            result = executor.execute(decision)

            # 6. LEARN
            reward = learner.compute_reward(state)
            learner.remember(state, decision["action"], reward)
            
            save_to_transactions(txn)
            delete_from_drafts(txn["txn_id"])

            # LOG
            print("TXN:", txn["txn_id"], txn["bank_name"])
            print("STATE:", state)
            print("REASONING:", reasoning)
            print("DECISION:", decision)
            print("ACTION:", result)
            print("REWARD:", reward)

            time.sleep(1.5)

        except Exception as e:
            print("❌ ERROR processing transaction:", e)
            traceback.print_exc()

    print("\n✅ All draft payments processed.")
    
def save_to_transactions(txn):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO transactions
        (txn_id, bank_name, amount, method, status, error_code, latency_ms)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (
        txn["txn_id"],
        txn["bank_name"],
        txn["amount"],
        txn["method"],
        txn["status"],
        txn["error_code"],
        txn["latency_ms"]
    ))

    conn.commit()
    cur.close()
    conn.close()


def delete_from_drafts(txn_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM drafts WHERE txn_id = %s", (txn_id,))
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    run_agent_on_drafts()