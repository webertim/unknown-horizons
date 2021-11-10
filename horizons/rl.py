import horizons
from horizons import time
from horizons import constants
from horizons.util.shapes.point import Point
from run_uh import close, setup
from fife import fife
import horizons.globals
import horizons.main


class Environment:

    def __init__(self) -> None:
        self.options = setup()
        self.initial = True
        
        horizons.main.setup(self.options)
        #horizons.main.session.speed_set(176)

    def reset(self):
        if not self.initial:
            horizons.globals.fife.reset()
            self.initial = False
        horizons.globals.fife.setup()

        horizons.globals.fife.quit_requested = False
        horizons.globals.fife.break_requested = False
        

    def render(self):
        try:
            horizons.globals.fife.engine.pump()
        except RuntimeError:
            import sys
            print("Unknown Horizons exited uncleanly via SIGINT")
            self._log.log_warn("Unknown Horizons exited uncleanly via SIGINT")
            sys.exit(1)
        except fife.Exception as e:
            print(e.getMessage())
    
    def build(self, point1, building_id):
        from horizons.entities import Entities
        from horizons.world.building import BuildingClass
        from horizons.gui.mousetools.buildingtool import BuildingTool
        from horizons.world.units.ship import Ship
        building : BuildingClass = Entities.buildings[building_id]
        for ship in horizons.main.session.world.ships:
            if ship.owner == horizons.main.session.world.player:
                playerShip = ship
        bt = BuildingTool(session=horizons.main.session, building=building, ship=playerShip)
        bt.preview_build(point1, point1)
        res = bt.do_build()
        print(res)

    def move(self, point : Point, ship_id):
        import horizons.main
        from horizons.world.units.ship import Ship
        ship : Ship = None
        for ship in horizons.main.session.world.ships:
            print(ship)
            if ship.worldid == ship_id:
                ship.go(point.x, point.y)
    
    def step(self):
        horizons.main.session.speed_unpause()
        time.step()
        horizons.globals.fife.loop()
        horizons.main.session.speed_pause()

    def close(self):
        horizons.globals.fife.quit()
        close(True)

def make() -> Environment:
    return Environment()