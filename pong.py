from dataclasses import dataclass
from enum import Enum, auto


class StepCondition(Enum):
    Player1Win = -2
    Player1Hit = -1
    Continue = 0
    Player2Hit = 1
    Player2Win = 2


@dataclass
class Pong:
    bounds: list
    p1_pos: float
    p2_pos: float
    ball_pos: list
    ball_vel: list
    ball_speed: float
    pad_size: float
    pad_speed: float

    # -1 = cima, 1 = baixo
    def play1(self, up_down):
        self.p1_pos += up_down * self.pad_speed
        self.p1_pos = max(0, min(self.p1_pos, self.bounds[1] - self.pad_size))

    # -1 = cima, 1 = baixo
    def play2(self, up_down):
        self.p2_pos += up_down * self.pad_speed
        self.p2_pos = max(0, min(self.p2_pos, self.bounds[1] - self.pad_size))

    def step(self) -> StepCondition:
        self.ball_pos[0] += self.ball_vel[0] * self.ball_speed
        self.ball_pos[1] += self.ball_vel[1] * self.ball_speed

        if not (0.0 <= self.ball_pos[1] <= self.bounds[1]):
            self.ball_vel[1] = -self.ball_vel[1]

        if self.ball_pos[0] < 0.0:
            self.ball_vel[0] = -self.ball_vel[0]
            if self.p1_pos <= self.ball_pos[1] <= (self.p1_pos + self.pad_size):
                return StepCondition.Player1Hit
            else:
                return StepCondition.Player2Win

        if self.ball_pos[0] > self.bounds[0]:
            self.ball_vel[0] = -self.ball_vel[0]
            if self.p2_pos <= self.ball_pos[1] <= (self.p2_pos + self.pad_size):
                return StepCondition.Player2Hit
            else:
                return StepCondition.Player1Win
