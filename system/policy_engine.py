class PolicyEngine:
    def decide(self, reasoning_output):
        actions = reasoning_output.get("recommended_actions", [])

        if not actions:
            return {
                "action": "DO_NOTHING",
                "reason": "No actions recommended by agent",
                "risk_level": "NONE"
            }

        # Take the first recommended action from LLM
        top_action = actions[0]

        return {
            "action": top_action["action"],
            "reason": top_action.get("reason", ""),
            "risk_level": "LOW"
        }
