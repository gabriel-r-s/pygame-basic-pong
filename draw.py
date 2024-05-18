from dataclasses import dataclass
import pygame as pg
from pong import Pong, StepCondition
import math
import random


def main():
    WIDTH = 800
    HEIGHT = 600
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    initial_angle = random.uniform(-0.25 * math.pi, 0.25 * math.pi)
    if random.getrandbits(1):
        initial_angle = -initial_angle
    pong = Pong(
        bounds=[WIDTH, HEIGHT],
        p1_pos=HEIGHT / 2,
        p2_pos=HEIGHT / 2,
        ball_pos=[WIDTH / 2, HEIGHT / 2],
        ball_vel=[math.cos(initial_angle), math.sin(initial_angle)],
        ball_speed=5.0,
        ball_radius=7.0,
        pad_size=HEIGHT / 5,
        pad_speed=10,
    )

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            pong.play1(-1)
        if keys[pg.K_s]:
            pong.play1(1)
        if keys[pg.K_UP]:
            pong.play2(-1)
        if keys[pg.K_DOWN]:
            pong.play2(1)

        screen.fill((0, 0, 0))
        pg.draw.rect(screen, WHITE, pg.Rect(0, 0, WIDTH, HEIGHT), 1)
        pg.draw.circle(screen, WHITE, pong.ball_pos, pong.ball_radius)
        pg.draw.rect(screen, WHITE, pg.Rect(0, pong.p1_pos, 5, pong.pad_size))
        pg.draw.rect(screen, WHITE, pg.Rect(WIDTH - 5, pong.p2_pos, 5, pong.pad_size))
        pg.display.flip()

        match pong.step():
            case StepCondition.Player1Win:
                print("Player 1 Wins!")
                running = False
            case StepCondition.Player2Win:
                print("Player 2 Wins!")
                running = False

        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    main()
