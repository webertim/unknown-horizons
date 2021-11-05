import horizons

class Gym:

    def __init__(self) -> None:
        pass

    def render(self):
        horizons.globals.fife.engine.pump()

    def step(self, action):
        pass