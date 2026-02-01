from payment_simulator import SYSTEM_STATE

class ActionExecutor:
    def execute(self, decision):
        action = decision["action"]

        if action == "DO_NOTHING":
            return "No action taken."

        if action.startswith("REROUTE_"):
            issuer = action.split("_")[1]
            key = f"{issuer}_failure_multiplier"
            old = SYSTEM_STATE[key]
            SYSTEM_STATE[key] = max(0.5, old * 0.5)
            return f"Rerouted traffic from {issuer}. {old} → {SYSTEM_STATE[key]}"

        if action.startswith("REDUCE_RETRIES_"):
            issuer = action.split("_")[2]
            key = f"{issuer}_failure_multiplier"
            old = SYSTEM_STATE[key]
            SYSTEM_STATE[key] = max(0.7, old * 0.7)
            return f"Reduced retries for {issuer}. {old} → {SYSTEM_STATE[key]}"

        if action.startswith("REQUEST_HUMAN_APPROVAL_"):
            issuer = action.split("_")[3]
            return f"Human approval requested to block {issuer}"

        if action == "ALERT_HUMAN":
            return "Alert sent to human ops team."

        # HARD FAIL SAFE
        return f"⚠️ Unsupported action from LLM: {action}"
