import random, sys
from game_utils import *


class GameItem:
    symbol = "?"
    color = "white"
    alive = True

    def __init__(self, position):
        self.position = position

    def update(self, game):
        pass

    def render(self):
        print_at_location(*self.position, self.symbol, self.color)


class Wall(GameItem):
    symbol = "#"


class Sock(GameItem):
    symbol = "s"
    color_points = {"blue": 3, "green": 2, "red": 1}

    def __init__(self, position, color, ttl):
        GameItem.__init__(self, position)
        self.color = color
        self.value = self.color_points[color]
        self.ttl = ttl

    def update(self, game):
        self.ttl -= 1
        if self.ttl <= 0:
            self.alive = False


class MobileGameItem(GameItem):
    movement_deltas = {
        "UP": (-1, 0),
        "DOWN": (1, 0),
        "LEFT": (0, -1),
        "RIGHT": (0, 1),
        None: (0, 0),
    }
    opposites = {
        "UP": "DOWN",
        "LEFT": "RIGHT",
        "RIGHT": "LEFT",
        "DOWN": "UP",
        None: None,
    }

    def __init__(self, position, time_between_moves):
        GameItem.__init__(self, position)
        self.time_between_moves = time_between_moves
        self.direction = None

    def update(self, game):
        if game.round_number % self.time_between_moves == 0:
            delta = self.movement_deltas[self.direction]
            new_position = tuple(i + j for i, j in zip(self.position, delta))
            if not game.objects_at(new_position, Wall):
                self.position = new_position


class Player(MobileGameItem):
    symbol = "@"

    def __init__(self, position, time_between_moves):
        MobileGameItem.__init__(self, position, time_between_moves)
        self.score = 0

    def update(self, game):
        MobileGameItem.update(self, game)

        socks_here = game.objects_at(self.position, Sock)
        for sock in socks_here:
            self.score += sock.value
            sock.alive = False


class Human(Player):
    def update(self, game):
        self.color = random.choice(list(color_map))
        for region, key in game.keys:
            if key in self.movement_deltas:
                if key == self.opposites[self.direction]:
                    self.direction = None
                else:
                    self.direction = key
        Player.update(self, game)


class Bot(Player):
    color = "magenta"

    def update(self, game):
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        Player.update(self, game)


class SmartBot(Bot):
    def update(self, game):
        socks = [item for item in game.all_objects if isinstance(item, Sock)]
        self.direction = None
        if socks:
            sock_deltas = [
                tuple(i - j for i, j in zip(self.position, sock.position))
                for sock in socks
            ]
            closest = min(sock_deltas, key=lambda x: sum(abs(i) for i in x))
            if abs(closest[0]) > abs(closest[1]):
                if closest[0] < 0:
                    self.direction = "DOWN"
                elif closest[0] > 0:
                    self.direction = "UP"
            else:
                if closest[1] < 0:
                    self.direction = "RIGHT"
                elif closest[1] > 0:
                    self.direction = "LEFT"
        Player.update(self, game)


FPS = 8


class Game:
    def __init__(self, height, width, time_limit=30*FPS):
        self.height = height
        self.width = width
        self.time_limit = time_limit

        self.all_objects = []
        for r in range(1, height + 1):
            self.all_objects.append(Wall((r, 1)))
            self.all_objects.append(Wall((r, width)))
        for c in range(2, width):
            self.all_objects.append(Wall((1, c)))
            self.all_objects.append(Wall((height, c)))

        self.player = Human((height - 1, 2), 1)
        self.bot = Bot((2, width - 1), 1)
        #self.bot = SmartBot((2, width - 1), 1)

        self.all_objects.append(self.player)
        self.all_objects.append(self.bot)

    def objects_at(self, position, instance_of=object):
        return [
            thing
            for thing in self.all_objects
            if thing.position == position and isinstance(thing, instance_of)
        ]

    def _maybe_add_sock(self):
        if random.random() < 0.2:
            row = random.randint(2, self.height - 1)
            col = random.randint(2, self.width - 1)
            color = random.choice(["red", "green", "blue"])
            ttl = random.randint(5, 50)
            self.all_objects.append(Sock((row, col), color, ttl))

    def update(self):
        self._maybe_add_sock()

        for e in self.all_objects:
            e.update(self)

        self.all_objects = [e for e in self.all_objects if e.alive]

    def unrender(self):
        for e in self.all_objects:
            if not isinstance(e, Wall):
                print_at_location(*e.position, " ", "white")

    def render(self):
        print_at_location(self.height + 1, 0, f"You: {self.player.score}")
        print_at_location(self.height + 2, 0, f"Bot: {self.bot.score}")
        print_at_location(self.height + 3, 0, f"Time: {self.time_limit - self.round_number}")
        for e in self.all_objects:
            e.render()

    def run(self):
        clear_screen()
        with keystrokes(sys.stdin) as keyb:
            for i in range(self.time_limit):
                self.round_number = i
                self.keys = keyb.regioned_keys()
                self.unrender()
                self.update()
                self.render()
                time.sleep(1 / FPS)

        if self.player.score > self.bot.score:
            text = "A WINNER IS YOU!"
            color = "green"
        else:
            text = "LOST :("
            color = "red"
        print_at_location(self.height + 4, 0, text, color)

        input("Press Enter to continue")


if __name__ == "__main__":
    Game(20, 20, 30 * FPS).run()
