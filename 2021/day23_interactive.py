from typing import Optional, Tuple
import tcod
import numpy as np

colors = {
    "A": (100,75,0),
    "B": (176,141,87),
    "C": (175,99,62),
    "D": (198,177,131),
}
costs = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}
# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # Unicode codepoint.
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", np.bool),  # True if this tile can be walked over.
        ("transparent", np.bool),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
    ]
)


def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, dark), dtype=tile_dt)

floor = new_tile(
    walkable=True, transparent=True, dark=(ord("."), (255, 255, 255), (0, 0, 0)),
)
empty = new_tile(
    walkable=False, transparent=True, dark=(ord(" "), (255, 255, 255), (0, 0, 0)),

)
wall = new_tile(
    walkable=False, transparent=False, dark=(ord("#"), (255, 255, 255), (0, 0, 0)),
)
WIDTH, HEIGHT = 13, 7  # Console width and height in tiles.
FLAGS = tcod.context.SDL_WINDOW_RESIZABLE | tcod.context.SDL_WINDOW_MAXIMIZED

def main() -> None:
    """Script entry point."""
    # Load the font, a 32 by 8 tile font with libtcod's old character layout.
    tileset = tcod.tileset.load_tilesheet(
        "font.png", 32, 8, tcod.tileset.CHARMAP_TCOD,
    )
    # Create the main console.
    console = tcod.Console(WIDTH, HEIGHT, order="F")
    event_handler = EventHandler() 
    # Create a window based on this console and tileset.
    entities = [
        Entity(3,2,'B',colors["B"]),
        Entity(3,3,'D',colors["D"]),
        Entity(3,4,'D',colors["D"]),
        Entity(3,5,'D',colors["D"]),
        Entity(5,2,'B',colors["B"]),
        Entity(5,3,'C',colors["C"]),
        Entity(5,4,'B',colors["B"]),
        Entity(5,5,'A',colors["A"]),
        Entity(7,2,'C',colors["C"]),
        Entity(7,3,'B',colors["B"]),
        Entity(7,4,'A',colors["A"]),
        Entity(7,5,'A',colors["A"]),
        Entity(9,2,'D',colors["D"]),
        Entity(9,3,'A',colors["A"]),
        Entity(9,4,'C',colors["C"]),
        Entity(9,5,'C',colors["C"]),
    ]
    game_map = GameMap(WIDTH, HEIGHT)
    engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player_index=0)
    state = np.zeros(shape=(WIDTH,HEIGHT),dtype=tcod.console.Console.DTYPE,order="F",)
    with tcod.context.new(  # New window for a console of size columns×rows.
        columns=console.width, rows=console.height, tileset=tileset, sdl_window_flags=FLAGS,
    ) as context:
        while True:  # Main loop, runs until SystemExit is raised.
            engine.render(console=console, context=context)
            events = tcod.event.wait()
            engine.handle_events(events, context)


class Action:
    pass

class EscapeAction(Action):
    pass

class SelectAction(Action):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Select at {self.x} {self.y}"

class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

class UndoAction(Action):
    pass


class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.K_UP:
            action = MovementAction(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = MovementAction(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = MovementAction(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = MovementAction(dx=1, dy=0)
        elif key == tcod.event.K_SPACE:
            action = UndoAction()
        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        # No valid key was pressed
        return action
    
    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> None:
        print(event)
        action = SelectAction(*event.tile)
        return action

class Entity:
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy


class Engine:
    def __init__(self, entities, event_handler: EventHandler, game_map, player_index: int):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player_index = player_index
        self.player = entities[player_index]
        self.player.color = (0, 255, 0)
        self.actions = []

    def handle_events(self, events, context) -> None:
        for event in events:
            context.convert_event(event)
            action = self.event_handler.dispatch(event)

            if action is None:
                    continue
            if isinstance(action, MovementAction):
                if self.game_map.tiles["walkable"][self.player.x + action.dx, self.player.y + action.dy]:
                    self.player.move(dx=action.dx, dy=action.dy)
                    self.actions.append((self.player_index, action, costs[self.player.char]))
                    print(sum(e[2] for e in self.actions))
            if isinstance(action, UndoAction):
                if self.actions:
                    last_active, last_action, _ = self.actions.pop()
                    self.entities[last_active].move(dx=-last_action.dx, dy=-last_action.dy)
                    print(self.actions)
                else:
                    print("Can't undo!")
            if isinstance(action, SelectAction):
                print(action)
                print(action.x)
                for i, e in enumerate(self.entities):
                    if action.x == e.x and action.y == e.y:
                        self.player.color = colors[self.player.char]
                        self.player_index = i
                        self.player = e
                        e.color = (0,255,0)
                        break
            if isinstance(action, EscapeAction):
                raise SystemExit()

    def render(self, console, context) -> None:
        self.game_map.render(console)
        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()


class GameMap:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=empty, order="F")

        self.tiles[0:self.width, 0] = wall
        self.tiles[1:self.width-1,1] = floor
        self.tiles[0,1] = wall
        self.tiles[self.width-1,1] = wall
        self.tiles[0:3,2] = wall
        self.tiles[self.width-3:self.width,2] = wall
        self.tiles[3,2:6] = floor
        self.tiles[5,2:6] = floor
        self.tiles[7,2:6] = floor
        self.tiles[9,2:6] = floor
        self.tiles[2,2:7] = wall
        self.tiles[4,2:7] = wall
        self.tiles[6,2:7] = wall
        self.tiles[8,2:7] = wall
        self.tiles[10,2:7] = wall
        self.tiles[3:self.width-3,6] = wall

    
    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]


if __name__ == "__main__":
    main()