# import random
# import time
# import uuid

# # This is the WORLD STATE (agent can change this)
# SYSTEM_STATE = {
#     "HDFC_failure_multiplier": 1.0,
#     "ICICI_failure_multiplier": 1.0,
#     "SBI_failure_multiplier": 1.0
# }

# ISSUERS = ["HDFC", "ICICI", "SBI"]
# METHODS = ["UPI", "CARD", "WALLET"]
# ERRORS = ["BANK_TIMEOUT", "NETWORK_ERROR", "INSUFFICIENT_FUNDS", None]

# BASE_FAIL_RATE = 0.1  # 10% baseline

# def generate_transaction():
#     issuer = random.choice(ISSUERS)

#     txn = {
#         "txn_id": str(uuid.uuid4())[:8],
#         "issuer": issuer,
#         "method": random.choice(METHODS),
#         "amount": random.randint(100, 5000),
#         "latency_ms": random.randint(100, 5000),
#         "status": "SUCCESS",
#         "error_code": None,
#         "timestamp": time.time()
#     }

#     # Issuer-specific failure logic
#     multiplier = SYSTEM_STATE[f"{issuer}_failure_multiplier"]
#     fail_chance = BASE_FAIL_RATE * multiplier

#     if random.random() < fail_chance:
#         txn["status"] = "FAILED"
#         txn["error_code"] = random.choice(ERRORS[:-1])

#     return txn

# if __name__ == "__main__":
#     print("Starting payment simulator...\n")

#     # Break HDFC initially for testing
#     SYSTEM_STATE["HDFC_failure_multiplier"] = 6.0
#     SYSTEM_STATE["ICICI_failure_multiplier"] = 1.0
#     SYSTEM_STATE["SBI_failure_multiplier"] = 8.0
#     SYSTEM_STATE["BOI_failure_multiplier"] = 1.0
#     SYSTEM_STATE["AXIS_failure_multiplier"] = 4.0
#     SYSTEM_STATE["INDUSIND_failure_multiplier"] = 1.0

#     while True:
#         txn = generate_transaction()
#         print(txn)
#         time.sleep(1)


import random
import uuid
import psycopg2

# DB connection
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="FirmPay",
        user="postgres",
        password="imaad@376"
    )

ISSUERS = ["HDFC", "ICICI", "SBI", "BOI", "AXIS", "INDUSIND"]
METHODS = ["UPI", "CARD", "WALLET"]

def generate_transaction():
    return {
        "txn_id": str(uuid.uuid4())[:8],
        "bank_name": random.choice(ISSUERS),
        "amount": random.randint(100, 5000),
        "method": random.choice(METHODS),
        "status": "DRAFT",
        "error_code": None,
        "latency_ms": random.randint(100, 5000),
    }

def generate_32_and_push_to_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # Clear previous drafts (for demo reset)
    cur.execute("DELETE FROM drafts;")

    for _ in range(32):
        txn = generate_transaction()
        cur.execute("""
            INSERT INTO drafts 
            (txn_id, bank_name, amount, method, status, error_code, latency_ms)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
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

    print("✅ 32 draft payments inserted into DB.")

if __name__ == "__main__":
    generate_32_and_push_to_db()
