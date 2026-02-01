class LearningLoop:
    def __init__(self):
        self.history = []  # memory

    def compute_reward(self, state):
        total_success = 0
        total_latency = 0
        count = 0

        for issuer, metrics in state.items():
            success_rate = 1 - metrics["failure_rate"]
            total_success += success_rate
            total_latency += metrics["avg_latency"]
            count += 1

        avg_success = total_success / count
        avg_latency = total_latency / count

        reward = avg_success - (avg_latency / 5000)
        return round(reward, 3)

    def remember(self, state, action, reward):
        self.history.append({
            "state": state,
            "action": action,
            "reward": reward
        })

    def should_rollback(self):
        if len(self.history) < 3:
            return False

        last_three = self.history[-3:]
        rewards = [x["reward"] for x in last_three]

        # If reward consistently dropping → rollback
        return rewards[2] < rewards[1] < rewards[0]
