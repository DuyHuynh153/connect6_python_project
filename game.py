import pygame
from pygame.locals import QUIT
from common import Point
from logger import MoveLogger
from rules import Referee
from bot import Bot

# Constants
STONE_CHAR = ['.', 'O', 'X']
STONE_NAME = ['', 'White (O)', 'Black (X)']
CHAR_TO_X = {chr(ord('A') + i): i for i in range(19)}
X_TO_CHAR = {i: chr(ord('A') + i) for i in range(19)}

class Connect6GUI:
    def __init__(self, bots):
        pygame.init()
        self.width, self.height = 760, 760
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("TherneConnect6")

        self.board = [[0 for _ in range(19)] for _ in range(19)]
        self.referee = Referee(self.board)
        self.nth_move = 1
        self.current_player = 2  # Black starts
        self.player_moved_count = 1  # At first, Black can only move once
        self.logger = MoveLogger()

        self.bots = [None] + bots  # To align index with player variable

        self.cell_size = self.width // 19  # Adjust cell size based on window size

        self.draw_board()
        self.bot_move()

    def draw_board(self):
        self.screen.fill((255, 255, 255))

        for x in range(19):
            for y in range(19):
                left, top = x * self.cell_size, y * self.cell_size
                stone = self.board[y][x]
                if stone != 0:
                    pygame.draw.circle(
                        self.screen,
                        (0, 0, 0) if stone == 1 else (255, 255, 255),
                        (left + self.cell_size // 2, top + self.cell_size // 2),
                        self.cell_size // 2 - 2
                    )

        # Draw grid lines
        for x in range(19):
            pygame.draw.line(self.screen, (0, 0, 0), (x * self.cell_size, 0), (x * self.cell_size, self.height), 1)
        for y in range(19):
            pygame.draw.line(self.screen, (0, 0, 0), (0, y * self.cell_size), (self.width, y * self.cell_size), 1)

        # Draw move information
        font = pygame.font.Font(None, 36)
        move_text = font.render(f"Move: {self.nth_move}", True, (0, 0, 0))
        player_text = font.render(f"{STONE_NAME[self.current_player]}'s turn", True, (0, 0, 0))
        self.screen.blit(move_text, (10, 10))
        self.screen.blit(player_text, (10, 50))

        pygame.display.flip()

    def bot_move(self):
        if self.bots[self.current_player] is not None:
            x, y = self.bots[self.current_player].move(self.board, self.nth_move)
            self.place_stone(x, y)

    def place_stone(self, x, y):
        self.board[y][x] = self.current_player
        self.logger.log(x, y, self.current_player)
        self.referee.update(x, y, self.current_player)

        self.nth_move += 1
        self.player_moved_count += 1
        if self.player_moved_count == 2:
            self.nth_move += 1
            self.player_moved_count = 0
            self.current_player = 2 if self.current_player == 1 else 1

        self.draw_board()

    def check_winner(self):
        won_player = self.referee.determine()
        if won_player is not None:
            winner_name = STONE_NAME[won_player]
            winner_bot = self.bots[won_player]
            self.display_winner(winner_name, winner_bot)

    def display_winner(self, winner_name, winner_bot):
        font = pygame.font.Font(None, 48)
        winner_text = font.render(
            f"{winner_name} ({winner_bot.bot_kind}) won!!", True, (0, 0, 0)
        )
        self.screen.blit(winner_text, (self.width // 2 - 200, self.height // 2 - 24))
        pygame.display.flip()
        self.logger.log_winner(winner_bot.player)
        self.logger.save_to_file()

    def run_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.bot_move()
            self.check_winner()

        pygame.quit()


class Player(Bot):
    """Player class remains the same as in your original code."""


if __name__ == '__main__':
    print('Welcome to TherneConnect6')
    print('Choose player slot (1=Player 2=AI)')

    black_choice = input('Black (1 or 2): ')
    white_choice = input('White (1 or 2): ')

    white_bot = Player(1) if white_choice == '1' else AIBot(1)
    black_bot = Player(2) if black_choice == '1' else AIBot(2)

    game = Connect6GUI([white_bot, black_bot])
    game.run_game()
