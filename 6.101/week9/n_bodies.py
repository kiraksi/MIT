# 6.101 recitation: n-bodies gravity simulation
# 19 April 2023

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __abs__(self):
        return (self.x**2 + self.y**2) **0.5
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
                    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
                    
    def __mul__(self, k):   # self * k
        assert isinstance(k, (int, float))
        return Vector(self.x * k, self.y * k)
                    
    def __rmul__(self, k):  # k * self
        return self * k
                    
    def __truediv__(self, k):
        assert isinstance(k, (int, float))
        return Vector(self.x / k, self.y / k)
                    
    @property
    def direction(self):
        return self / abs(self)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    
class Body:
    G = 6.67e-11

    def __init__(self, mass, position, velocity=Vector(0,0)):
        self.mass = mass
        self.position = position
        self.velocity = velocity

    def force_from(self, other):
        r = other.position - self.position
        r_hat = r.direction
        return self.G * self.mass * other.mass * r_hat / abs(r)**2

    def move(self, force, dt):
        acceleration = force / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt


class System:
    def __init__(self, bodies):
        self.bodies = bodies

    def step(self, dt):
        # add up all the forces per body
        forces_by_body = [
            # list of pairs (body, total force on body)
            (body, sum((body.force_from(other) for other in self.bodies if body != other), 
                       start=Vector(0,0)) )
                for body in self.bodies
        ]

        # apply the forces
        for body,force in forces_by_body:
            body.move(force, dt)


def run(selection, dark=True):
    examples = {
        'two_stable': [
            Body(1e25, Vector(0,0.91e9), Vector(200, 0)),
            Body(1e25, Vector(0,-0.91e9), Vector(-200, 0)),
        ],

        'two_erratic': [
            Body(1e25, Vector(0,0.91e9), Vector(200, 0)),
            Body(1e25, Vector(0,-0.91e9), Vector(-200, 0)),
        ],

        'three': [
            Body(1e25, Vector(0,0.91e9), Vector(400, 0)),
            Body(1e25, Vector(0,-0.91e9), Vector(-400, 0)),
            Body(5e8, Vector(0,0), Vector(25, 0)),
        ],

        'four': [
            Body(1e25, Vector(0,0.91e9), Vector(400, 0)),
            Body(1e25, Vector(0,-0.91e9), Vector(-400, 0)),
            Body(5e8, Vector(50,0), Vector(25, 0)),
            Body(5e8, Vector(-50,0), Vector(-25, 0)),
        ],

        'seven_stable': [
            Body(1e25, Vector(0,0.91e9), Vector(400, 0)),
            Body(1e25, Vector(0,-0.91e9), Vector(-400, 0)),
            Body(5e8, Vector(1e5,0), Vector(25, 25)),
            Body(5e8, Vector(-1e5,0), Vector(-25, -25)),
            Body(1e20, Vector(1e8,1e8), Vector(0, 100)),
            Body(1e20, Vector(-1e8,-1e8), Vector(0, -100)),
            Body(1e10, Vector(0,0), Vector(0, 0)),
        ],

        'seven_erratic': [
            Body(1e25, Vector(0,0.91e9), Vector(400, 0)),
            Body(1e25, Vector(0,-0.91e9), Vector(-400, 0)),
            Body(5e8, Vector(1e5,0), Vector(25, 25)),
            Body(5e8, Vector(-1e5,0), Vector(-25, -25)),
            Body(1e20, Vector(1e8,1e8), Vector(0, 150)),
            Body(1e20, Vector(-1e8,-1e8), Vector(0, -100)),
            Body(1e10, Vector(0,0), Vector(0, 0)),
        ],

        'two_from_rest': [
            Body(1e25, Vector(1e8,1e8), Vector(0, 0)),
            Body(1e25, Vector(-1e8,-1e8), Vector(0, 0)),
        ],
    }

    import pygame
    import sys
    import time

    class GraphicalSimulation(System):
        """
        Like the simulation, but also displays things to the screen
        """
        size = 1024
        colors = [
            (255, 0, 0),
            (0, 0, 255),
            (66, 52, 0),
            (152, 152, 152),
            (0, 255, 255),
            (255, 150, 0),
            (255, 0, 255),
        ]
        background = 'white'

        def __init__(self, bodies, screen_limit):
            System.__init__(self, bodies)
            self.screen_limit = screen_limit
            self.screen = pygame.display.set_mode((self.size, self.size))


        def draw(self):
            self.screen.fill(self.background)
            for b, c in zip(self.bodies, self.colors):
                x = self.size//2 + (b.position.x/self.screen_limit)*self.size//2
                y = self.size//2 + (b.position.y/self.screen_limit)*self.size//2
                pygame.draw.circle(self.screen, c, (x, y), 10)
            pygame.display.flip()

        def step(self, dt):
            System.step(self, dt)
            self.draw()


    if dark:
        GraphicalSimulation.background = 'black'
        GraphicalSimulation.colors = [(255-r, 255-g, 255-b)
            for r,g,b in GraphicalSimulation.colors]
        #sys.argv = [arg for arg in sys.argv if '-d' != arg != '--dark']

    # if len(sys.argv) < 2:
    #     print('Pass an example name as a command-line argument.')
    #     sys.exit(1)

    # selection = sys.argv[1]
    if selection not in examples:
        print('Example not found.')
        return

    #dt = 2_000
    dt = 10_000
    sim = GraphicalSimulation(examples[selection], 2e9)

    # Unexplained magic using the pygame library
    pygame.init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        sim.step(dt)
        time.sleep(0.0001)


run('three')
#run('four')
#run('two_from_rest')
