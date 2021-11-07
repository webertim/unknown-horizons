import horizons
from horizons import time
from run_uh import close, setup


class Environment:

    def __init__(self) -> None:
        self.options = setup()
        self.initial = True
        import horizons.main
        horizons.main.setup(self.options)
        horizons.main.session.speed_set(176)

    def reset(self):
        import horizons.main

        import horizons.globals
        if not self.initial:
            horizons.globals.fife.reset()
            self.initial = False
        horizons.globals.fife.setup()

        horizons.globals.fife.quit_requested = False
        horizons.globals.fife.break_requested = False
        

    def render(self):
        pass
    
    def step(self):
        import horizons.globals
        import horizons.main
        horizons.main.session.speed_unpause()
        time.step()
        horizons.globals.fife.loop()
        horizons.main.session.speed_pause()

    def close(self):
        import horizons.globals
        horizons.globals.fife.quit()
        close(True)

def make() -> Environment:
    return Environment()