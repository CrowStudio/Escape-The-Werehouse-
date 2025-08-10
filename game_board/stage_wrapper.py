import pygame
from game_board.stages.stage_1 import StageOne

class StageWrapper:
    def __init__(self):
        self.stages = [StageOne()]
        self.current_stage_index = 0
        self.current_stage = self.stages[self.current_stage_index]

    def __getattr__(self, name):
        # Delegate attribute or method access to the current stage
        return getattr(self.current_stage, name)