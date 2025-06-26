from random import choice

# Environment -------------------------------------------------
class TwoRoomEnvironment:
    def __init__(self):
        self.state = {"A": choice(["clean", "dirty"]),
                      "B": choice(["clean", "dirty"])}
        self.location = "A"                    # start position

    def percept(self):
        return self.location, self.state[self.location]

    def execute(self, action):
        if action == "suck":
            self.state[self.location] = "clean"
        elif action == "right":
            self.location = "B"
        elif action == "left":
            self.location = "A"

    def is_done(self):
        return all(v == "clean" for v in self.state.values())

# Agent -------------------------------------------------------
class VacuumAgent:
    """Simple reflex agent"""
    def act(self, percept):
        location, status = percept
        if status == "dirty":
            return "suck"
        return "right" if location == "A" else "left"

# Simulation --------------------------------------------------
env, agent, steps = TwoRoomEnvironment(), VacuumAgent(), 0
while not env.is_done() and steps < 10:
    action = agent.act(env.percept())
    env.execute(action)
    steps += 1
print(f"Done in {steps} steps → {env.state}")