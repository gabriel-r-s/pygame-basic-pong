import math
import random
from enum import Enum, auto


class StepCondition(Enum):
    Player1Score = -2
    Player1Hit = -1
    Continue = 0
    Player2Hit = 1
    Player2Score = 2


class Pong:
    def __init__(self, width, height):
        self.reflect_angle = math.pi * 3.5 / 12
        self.bounds = [width, height]
        self.p1_pos = height / 2
        self.p2_pos = height / 2
        self.p1_score = 0
        self.p2_score = 0
        self.ball_speed = width / 110
        self.ball_radius = width / 100
        self.pad_size = height / 6
        self.pad_speed = height / 60
        self.set_random_ball()
        self.condition = StepCondition.Continue

    def set_random_ball(self):
        pos = [self.bounds[0] / 2, self.bounds[1] / 2]
        initial_angle = random.uniform(math.pi / 6, math.pi / 4)
        vel = [math.cos(initial_angle), math.sin(initial_angle)]
        rand = random.getrandbits(1)
        if rand & 1:
            pos[0] += self.bounds[0] / 6
            vel[0] *= -1
        else:
            pos[0] -= self.bounds[0] / 6
        if rand & 2:
            vel[1] *= -1

        self.ball_pos = pos
        self.ball_vel = vel

    # -1 = cima, 1 = baixo
    def play1(self, up_down):
        self.p1_pos += up_down * self.pad_speed
        self.p1_pos = max(0, min(self.p1_pos, self.bounds[1] - self.pad_size))

    # -1 = cima, 1 = baixo
    def play2(self, up_down):
        self.p2_pos += up_down * self.pad_speed
        self.p2_pos = max(0, min(self.p2_pos, self.bounds[1] - self.pad_size))

    def step(self) -> StepCondition:
        if self.condition == StepCondition.Player1Score or self.condition == StepCondition.Player2Score:
            self.set_random_ball()
        else:
            self.ball_pos[0] += self.ball_vel[0] * self.ball_speed
            self.ball_pos[1] += self.ball_vel[1] * self.ball_speed

        if self.ball_vel[0] < 0.0 and self.ball_pos[0] - self.ball_radius / 2 <= 0.0:
            paddle_top = self.p1_pos - self.ball_radius / 2
            paddle_bottom = self.p1_pos + self.pad_size + self.ball_radius / 2
            self.ball_pos[0] = self.ball_radius / 2
            if paddle_top <= self.ball_pos[1] <= paddle_bottom:
                hit_rel_pos = (self.ball_pos[1] - self.p1_pos) / self.pad_size
                ang = hit_rel_pos * 2 * self.reflect_angle - self.reflect_angle
                self.ball_vel = [math.cos(ang), math.sin(ang)]
                self.condition = StepCondition.Player1Hit
                return
            else:
                self.p2_score += 1
                self.set_random_ball()
                self.condition = StepCondition.Player2Score
                return

        if self.ball_vel[0] > 0.0 and self.ball_pos[0] + self.ball_radius / 2 >= self.bounds[0]:
            paddle_top = self.p2_pos - self.ball_radius / 2
            paddle_bottom = self.p2_pos + self.pad_size + self.ball_radius / 2
            self.ball_pos[0] = self.bounds[0] - self.ball_radius / 2
            if paddle_top <= self.ball_pos[1] <= paddle_bottom:
                hit_rel_pos = (self.ball_pos[1] - self.p2_pos) / self.pad_size
                ang = hit_rel_pos * 2 * self.reflect_angle - self.reflect_angle
                self.ball_vel = [-math.cos(ang), math.sin(ang)]
                self.condition = StepCondition.Player2Hit
                return
            else:
                self.p1_score += 1
                self.set_random_ball()
                self.condition = StepCondition.Player1Score
                return

        if self.ball_pos[1] - self.ball_radius / 2 < 0.0 and self.ball_vel[1] < 0.0:
            self.ball_vel[1] *= -1.0
        elif self.ball_pos[1] + self.ball_radius / 2 > self.bounds[1] and self.ball_vel[1] > 0.0:
            self.ball_vel[1] *= -1.0

        self.condition = StepCondition.Continue
