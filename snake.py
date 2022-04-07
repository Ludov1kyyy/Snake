# Snake by @Ludov1kyyyy

import pygame
from sys import exit
from random import randint

pygame.init()

CELL_SIZE = CELL_NUM = 20
WINSIZE = CELL_SIZE * CELL_NUM
FONT = pygame.font.Font("font/PoetsenOne-Regular.ttf", 25)

BLACK_COLOR = (24, 24, 24)
WHITE_COLOR = (200, 200, 200)
GREEN_COLOR = (0, 220, 0)
RED_COLOR = (220, 0, 0)

class Text:
    def __init__(self, info, pos, point="center"):
        info_surf = FONT.render(str(info), True, WHITE_COLOR)

        if point == "topleft":
            info_rect = info_surf.get_rect(topleft = pos)
        if point == "center":
            info_rect = info_surf.get_rect(center = pos)

        win = pygame.display.get_surface()
        win.blit(info_surf, info_rect)

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
            pos_x = int(pos.x * CELL_SIZE)
            pos_y = int(pos.y * CELL_SIZE)

            if pos.x > CELL_NUM - 1:
                pos.x = 0
            if pos.x < 0:
                pos.x = CELL_NUM - 1
            if pos.y > CELL_NUM - 1:
                pos.y = 0
            if pos.y < 0:
                pos.y = CELL_NUM - 1

            block = Block((pos_x, pos_y), GREEN_COLOR)

            win.blit(block.image, block.rect)

    def input(self):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.move.x != -1:
            self.move.x = 1
            self.move.y = 0
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.move.x != 1 and self.move:
            self.move.x = -1
            self.move.y = 0
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.move.y != 1:
            self.move.x = 0
            self.move.y = -1
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.move.y != -1:
            self.move.x = 0
            self.move.y = 1

    def movement(self):
        if self.move and not self.dead:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.move)
            self.body = body_copy[:]

    def grow(self):
        body_copy = self.body[:]
        body_copy.insert(0, body_copy[0] + self.move)
        self.body = body_copy[:]

    def collision(self):
        for pos in self.body[1:]:
            if self.body[0] == pos:
                self.dead = True

    def display_score(self, win):
        Text(f"Score: {self.score}", (5, 5), "topleft")

    def reset(self):
        self.body = [pygame.math.Vector2(5, 10),
                     pygame.math.Vector2(4, 10),
                     pygame.math.Vector2(3, 10)]

        self.move = pygame.math.Vector2()
        self.score = 0
        self.dead = False

class Fruit:
    def __init__(self, snake):
        self.snake = snake
        self.fruit = Block(self.get_pos(), RED_COLOR)

    def draw(self, win):
        win.blit(self.fruit.image, self.fruit.rect)

    def get_pos(self):
        while True:
            pos_x = int(randint(0, CELL_NUM - 1) * CELL_SIZE)
            pos_y = int(randint(0, CELL_NUM - 1) * CELL_SIZE)

            if self.is_occupied((pos_x, pos_y)):
                continue
            else:
                return (pos_x, pos_y)

    def is_occupied(self, position):
        for pos in self.snake.body:
            if pos * CELL_SIZE == position:
                return True
        return False

    def eaten(self):
        if self.snake.body[0] * CELL_SIZE == self.fruit.rect.topleft:
            self.reset()
            self.snake.grow()
            self.snake.score += 1

    def reset(self):
        self.fruit.rect.topleft = self.get_pos()

class Game:
    def __init__(self):
        self.win = pygame.display.set_mode((WINSIZE, WINSIZE))
        pygame.display.set_caption("Snake")
        self.state = "main"

        self.snake = Snake()
        self.fruit = Fruit(self.snake)

    def grid(self):
        for pos_x in range(0, WINSIZE, CELL_SIZE):
            for pos_y in range(0, WINSIZE, CELL_SIZE):
                block = Block((pos_x, pos_y), RED_COLOR)
                pygame.draw.rect(self.win, BLACK_COLOR, block, 1)

    def display_reset(self):
        Text("You Lost!", (WINSIZE // 2, WINSIZE // 2 - 30))
        Text(f"Score: {self.snake.score}", (WINSIZE // 2, WINSIZE // 2))
        Text("Press ENTER to play again!", (WINSIZE // 2, WINSIZE // 2 + 30))

    def main(self):
        self.fruit.eaten()
        self.snake.input()
        self.snake.collision()

        self.win.fill(BLACK_COLOR)
        self.fruit.draw(self.win)
        self.snake.draw(self.win)
        self.grid()
        self.snake.display_score(self.win)

        if self.snake.dead:
            self.state = "reset"

    def reset(self):
        self.win.fill(BLACK_COLOR)
        self.fruit.draw(self.win)
        self.snake.draw(self.win)
        self.grid()
        self.display_reset()

    def game_state(self):
        if self.state == "main":
            self.main()
        if self.state == "reset":
            self.reset()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    if self.state == "reset":
                        if event.key == pygame.K_RETURN:
                            self.snake.reset()
                            self.fruit.reset()
                            self.state = "main"
                if event.type == self.snake.MOVE:
                    self.snake.movement()

            self.game_state()

            pygame.display.update()

game = Game()
game.run()
