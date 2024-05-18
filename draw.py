import pygame as pg
import pygame.freetype
from pong import Pong, StepCondition


WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PAD_WIDTH = 5


def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    pong = Pong(WIDTH, HEIGHT)
    font = pg.freetype.Font("./F77MinecraftRegular-0VYv.ttf", 24)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        keys = pg.key.get_pressed()
        if keys[pg.K_q]:
            running = False

        if keys[pg.K_w]:
            pong.play1(-1)
        if keys[pg.K_s]:
            pong.play1(1)
        if keys[pg.K_UP] or keys[pg.K_k]:
            pong.play2(-1)
        if keys[pg.K_DOWN] or keys[pg.K_j]:
            pong.play2(1)

        screen.fill((0, 0, 0))
        pg.draw.rect(screen, WHITE, pg.Rect(0, 0, WIDTH, HEIGHT), 1)
        pg.draw.circle(screen, WHITE, pong.ball_pos, pong.ball_radius)
        pg.draw.rect(screen, WHITE, pg.Rect(0, pong.p1_pos, PAD_WIDTH, pong.pad_size))
        pg.draw.rect(
            screen,
            WHITE,
            pg.Rect(WIDTH - PAD_WIDTH, pong.p2_pos, PAD_WIDTH, pong.pad_size),
        )
        pg.draw.line(screen, WHITE, [WIDTH / 2, 0], [WIDTH / 2, HEIGHT])
        font.render_to(
            screen,
            (WIDTH / 2 - WIDTH / 6, HEIGHT / 6),
            f"{pong.p1_score}",
            (255, 255, 255),
        )
        font.render_to(
            screen,
            (WIDTH / 2 + WIDTH / 6, HEIGHT / 6),
            f"{pong.p2_score}",
            (255, 255, 255),
        )
        pg.display.flip()

        match pong.step():
            case StepCondition.Player1Win:
                pong.set_random_ball()
                pg.time.delay(500)
            case StepCondition.Player2Win:
                pong.set_random_ball()
                pg.time.delay(500)

        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    main()
