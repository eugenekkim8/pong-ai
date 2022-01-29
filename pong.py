import math

class Sprite:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    def __str__(self):
        return "(" + self.x + ", " + self.y + ")"

    def contains_x(self, other):
        return (self.x <= other.x <= self.x + self.w)  

    def contains_y(self, other):
        return (self.y <= other.y <= self.y + self.h)

    def collide(self, other):
        return (self.contains_x(other) or other.contains_x(self)) and (self.contains_y(other) or other.contains_y(self))

class Ball(Sprite):
    def __init__(self, x, y, w, h, dx, dy):
        Sprite.__init__(self, x, y, w, h)
        self.dx, self.dy = dx, dy

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def adjust_angle(self, angle_degrees):
        # print(angle_degrees)
        if angle_degrees % 90 == 0:
            raise Exception("Ball can't travel vertically.")
        self.dy = self.dx * math.tan(angle_degrees / 180.0 * math.pi)

class Paddle(Sprite):
    def __init__(self, x, y, w, h, dy):
        Sprite.__init__(self, x, y, w, h)
        self.dy = dy

    def move(self, moveUp):
        self.y += self.dy * (-1 if moveUp else 1)

    def get_post_collision_angle(self, ball, left_side):
        # Assumes that paddle and ball have collided
        other_center_y = ball.y + ball.h / 2
        collision_pt_pct = max(0, min(self.h, other_center_y - self.y)) / self.h
        raw_angle = collision_pt_pct * 100 * 75 / 50 - 75 
        return raw_angle if not left_side else 180 - raw_angle

class Pong:

    # Paddle 1 is automatic, following self.P1_method
    # Paddle 2 takes user input. 

    WIDTH = 160
    HEIGHT = 210

    BALL_SIZE = 10
    BALL_DX = WIDTH / 1.5 / 100

    PADDLE_WIDTH = 10
    PADDLE_HEIGHT = HEIGHT / 6

    PADDLE1_DY = PADDLE2_DY = HEIGHT * 2 / 100

    # Rewards
    HIT_BALL = 1
    WIN_GAME = 20

    # P1 methods
    def follow(self):
        distance_between_centers = self.P1.y + self.P1.h / 2 - self.B.y + self.B.h / 2
        if distance_between_centers > self.P1.dy:
            self.P1.move(moveUp = True)
        elif distance_between_centers < -1 * self.P1.dy:
            self.P1.move(moveUp = False)

    def __init__(self, P1_method = follow):
        self.B = Ball(x = self.WIDTH / 2, y = self.HEIGHT / 2, w = self.BALL_SIZE, h = self.BALL_SIZE, dx = -1 * self.BALL_DX, dy = 0)
        self.P1 = Paddle(x = self.WIDTH * 1 / 10, y = (self.HEIGHT - self.PADDLE_HEIGHT) / 2, w = self.PADDLE_WIDTH, h = self.PADDLE_HEIGHT, dy = self.PADDLE1_DY)
        self.P2 = Paddle(x = self.WIDTH * 9 / 10, y = (self.HEIGHT - self.PADDLE_HEIGHT) / 2, w = self.PADDLE_WIDTH, h = self.PADDLE_HEIGHT, dy = self.PADDLE2_DY)
        self.WALL_U = Sprite(x = 0, y = 0, w = self.WIDTH, h = 0)
        self.WALL_D = Sprite(x = 0, y = self.HEIGHT, w = self.WIDTH, h = 0)
        self.WALL_L = Sprite(x = 0, y = 0, w = 0, h = self.HEIGHT)
        self.WALL_R = Sprite(x = self.WIDTH, y = 0, w = 0, h = self.HEIGHT)
        self.P1_method = P1_method

    def step(self, action):

        """ Returns observation, reward, episode_over """

        obs = self.get_state()
        reward, episode_over = self.check_collisions()

        ### Move ball.
        self.B.move()

        ### Move paddles.
        self.P1_method(self)
        self.act(action)

        return (obs, reward, episode_over)

    def get_state(self):
        return (self.P1.y, self.P2.y, self.B.x, self.B.y, self.B.dx, self.B.dy)

    def check_collisions(self):
        reward, episode_over = 0, False

        # Walls
        if self.B.collide(self.WALL_L):
            reward += self.WIN_GAME # P2 wins
            episode_over = True
        elif self.B.collide(self.WALL_R):
            reward -= self.WIN_GAME # P1 wins
            episode_over = True

        if self.B.collide(self.WALL_U) or self.B.collide(self.WALL_D):
            self.B.dy *= -1

        # Paddles
        if self.B.collide(self.P1):
            self.B.dx *= -1
            self.B.adjust_angle(self.P1.get_post_collision_angle(self.B, left_side = False))
            reward -= self.HIT_BALL
        elif self.B.collide(self.P2):
            self.B.dx *= -1
            self.B.adjust_angle(self.P2.get_post_collision_angle(self.B, left_side = True))
            reward += self.HIT_BALL

        return reward, episode_over

    def act(self, action):
        if action == 'u' and not self.P2.collide(self.WALL_U):
            self.P2.move(moveUp = True)
        elif action == 'd' and not self.P2.collide(self.WALL_D):
            self.P2.move(moveUp = False)

    def render(self):
        print(self.get_state())
        pass

