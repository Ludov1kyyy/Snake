import pygame
from sys import exit
from random import randint

pygame.init()

CELL_SIZE = CELL_NUM = 20
WINSIZE = CELL_SIZE * CELL_NUM
FONT = pygame.font.Font(None, 30)

BLACK_COLOR = (24, 24, 24)
WHITE_COLOR = (200, 200, 200)
GREEN_COLOR = (60, 239, 59)
RED_COLOR = (241, 79, 80)

def display_text(info, pos, win, point="center"):
    info_surf = FONT.render(str(info), True, WHITE_COLOR)
    info_rect = info_surf.get_rect()

    if point == "topleft":
        info_rect.topleft = pos
    if point == "center":
        info_rect.center = pos

    win.blit(info_surf, info_rect)

def grid(win):
    for pos_x in range(0, WINSIZE, CELL_SIZE):
        for pos_y in range(0, WINSIZE, CELL_SIZE):
            block = pygame.Rect((pos_x, pos_y), (CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(win, BLACK_COLOR, block, 1)

class Block:
    def __init__(self, pos, color):
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = pos)

class Snake:
    def __init__(self):
        self.body = [pygame.math.Vector2(5, 10),
                     pygame.math.Vector2(4, 10),
                     pygame.math.Vector2(3, 10)]

        self.move = pygame.math.Vector2()
        self.score = 0
        self.dead = False

        self.MOVE = pygame.USEREVENT + 1
        pygame.time.set_timer(self.MOVE, 100)

    def draw(self, win):
        for pos in self.body:
            if pos.x > CELL_NUM - 1:
                pos.x = 0
            if pos.x < 0:
                pos.x = CELL_NUM - 1
            if pos.y > CELL_NUM - 1:
                pos.y = 0
            if pos.y < 0:
                pos.y = CELL_NUM - 1

            pos_x = int(pos.x * CELL_SIZE)
            pos_y = int(pos.y * CELL_SIZE)

            snake = Block((pos_x, pos_y), GREEN_COLOR)
            win.blit(snake.image, snake.rect)

    def input(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_RIGHT] and self.move.x != -1:
            self.move.x = 1
            self.move.y = 0
        if key[pygame.K_LEFT] and self.move.x != 1 and self.move:
            self.move.x = -1
            self.move.y = 0
        if key[pygame.K_UP] and self.move.y != 1:
            self.move.x = 0
            self.move.y = -1
        if key[pygame.K_DOWN] and self.move.y != -1:
            self.move.x = 0
            self.move.y = 1

    def movement(self):
        if not self.dead and self.move:
            body = self.body[:-1]
            body.insert(0, body[0] + self.move)
            self.body = body[:]

    def grow(self):
        body = self.body[:]
        body.insert(0, body[0] + self.move)
        self.body = body[:]

    def collision(self):
        for pos in self.body[1:]:
            if self.body[0] == pos:
                self.dead = True

    def reset(self):
        self.body = [pygame.math.Vector2(5, 10),
                     pygame.math.Vector2(4, 10),
                     pygame.math.Vector2(3, 10)]

        self.move = pygame.math.Vector2()
        self.score = 0
        self.dead = False

    def update(self):
        self.input()
        self.collision()

class Apple:
    def __init__(self, snake):
        self.snake = snake
        self.sprite = Block(self.get_pos(), RED_COLOR)

    def draw(self, win):
        win.blit(self.sprite.image, self.sprite.rect)

    def get_pos(self):
        while True:
            pos_x = int(randint(0, CELL_NUM - 1))
            pos_y = int(randint(0, CELL_NUM - 1))

            if self.is_occupied((pos_x, pos_y)):
                continue
            else:
                return (pos_x * CELL_SIZE, pos_y * CELL_SIZE)

    def is_occupied(self, sprite_pos):
        for pos in self.snake.body:
            if sprite_pos == pos:
                return True
        return False

    def eaten(self):
        if self.snake.body[0] * CELL_SIZE == self.sprite.rect.topleft:
            self.reset_pos()
            self.snake.grow()
            self.snake.score += 1

    def reset_pos(self):
        self.sprite.rect.topleft = self.get_pos()

class State:
    def __init__(self):
        self.state = "open"

        self.snake = Snake()
        self.apple = Apple(self.snake)

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                if self.state == "open":
                    if event.key == pygame.K_RETURN:
                        self.state = "main"
                if self.state == "over":
                    if event.key == pygame.K_RETURN:
                        self.reset()
            if event.type == self.snake.MOVE:
                self.snake.movement()

    def open(self, win):
        win.fill(BLACK_COLOR)
        display_text("Press ENTER to play", (WINSIZE // 2, WINSIZE // 2), win)

    def main(self, win):
        self.snake.update()
        self.apple.eaten()
        
        win.fill(BLACK_COLOR)
        self.apple.draw(win)
        self.snake.draw(win)
        grid(win)

        display_text(f"Score: {self.snake.score}", (5, 5), win, "topleft")

        if self.snake.dead:
            self.state = "over"

    def over(self, win):
        win.fill(BLACK_COLOR)
        self.apple.draw(win)
        self.snake.draw(win)
        grid(win)

        display_text("You Lost!", (WINSIZE // 2, WINSIZE // 2 - 30), win)
        display_text(f"Score: {self.snake.score}", (WINSIZE // 2, WINSIZE // 2), win)
        display_text("Press ENTER to play again", (WINSIZE // 2, WINSIZE // 2 + 30), win)

    def reset(self):
        self.snake.reset()
        self.apple.reset_pos()
        self.state = "main"

    def run(self, win):
        self.event()

        if self.state == "open":
            self.open(win)
        if self.state == "main":
            self.main(win)
        if self.state == "over":
            self.over(win)

class Game:
    def __init__(self):
        self.win = pygame.display.set_mode((WINSIZE, WINSIZE))
        pygame.display.set_caption("Snake")
        self.state = State()

    def run(self):
        while True:
            self.state.run(self.win)
            pygame.display.update()

game = Game()
game.run()
