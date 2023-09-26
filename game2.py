import pygame

pygame.init()

WIDTH = 650
HEIGHT = 700

# Define some colors
BACKGROUND_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
BLACK = (0, 0, 0)
WHITE = (222, 222, 222)

GRID_SIZE = 19
CELL_SIZE = WIDTH // GRID_SIZE
CIRCLE_RADIUS = CELL_SIZE // 3.3  # Radius of the circle

# Initialize move history list
move_history = []

# List to store the clicked points
clicked_points = []

# List to store the colors of the clicked points
clicked_colors = []

# Variable to keep track of the current player's turn
current_player = 'black'  # Start with red player

# Function to draw the game board
def draw_board(screen):
    screen.fill(BACKGROUND_COLOR)

    for x in range(CELL_SIZE, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (x, 0), (x, HEIGHT), 2)

    for y in range(CELL_SIZE, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, y), (WIDTH, y), 2)

# Function to draw the move history table
def draw_move_history(screen):
    # Define the position and size of the move history table
    table_x = WIDTH
    table_y = 0
    table_width = 150
    table_height = HEIGHT

    # Draw the table background
    pygame.draw.rect(screen, WHITE, (table_x, table_y, table_width, table_height))

    # Draw the move history text
    font = pygame.font.Font(None, 36)
    text_color = BLACK
    row_height = 40
    for i, move in enumerate(move_history):
        text = font.render(move, True, text_color)
        text_rect = text.get_rect()
        text_rect.x = table_x + 10
        text_rect.y = table_y + 10 + i * row_height
        screen.blit(text, text_rect)

# Function to check if the mouse click is near an intersection point
def is_near_intersection(mouse_x, mouse_y, threshold=5):
    # Calculate the row and column based on the mouse position
    row = mouse_y // CELL_SIZE
    col = mouse_x // CELL_SIZE

    # Calculate the exact intersection point
    intersection_x = col * CELL_SIZE
    intersection_y = row * CELL_SIZE

    # Check if the mouse click is within the threshold range of the intersection point
    return (
        abs(mouse_x - intersection_x) < threshold
        and abs(mouse_y - intersection_y) < threshold
    )

# Function to draw a circle at the clicked position
def draw_circle(screen, x, y, radius, color):
    pygame.draw.circle(screen, color, (x, y), radius)

def check_for_win(color):
    # Check for horizontal win
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE - 5):
            if all(
                clicked_colors[row * GRID_SIZE + col + i] == color
                for i in range(6)
                if row * GRID_SIZE + col + i < len(clicked_colors)
            ):
                return True

    # Check for vertical win
    for col in range(GRID_SIZE):
        for row in range(GRID_SIZE - 5):
            if all(
                clicked_colors[(row + i) * GRID_SIZE + col] == color
                for i in range(6)
                if (row + i) * GRID_SIZE + col < len(clicked_colors)
            ):
                return True

    # Check for diagonal win (from top-left to bottom-right)
    for row in range(GRID_SIZE - 5):
        for col in range(GRID_SIZE - 5):
            if all(
                clicked_colors[(row + i) * GRID_SIZE + col + i] == color
                for i in range(6)
                if (row + i) * GRID_SIZE + col + i < len(clicked_colors)
            ):
                return True

    # Check for diagonal win (from top-right to bottom-left)
    for row in range(GRID_SIZE - 5):
        for col in range(5, GRID_SIZE):
            if all(
                clicked_colors[(row + i) * GRID_SIZE + col - i] == color
                for i in range(6)
                if (row + i) * GRID_SIZE + col - i < len(clicked_colors)
            ):
                return True

    return False




# Create the game window
screen = pygame.display.set_mode((WIDTH + 150, HEIGHT))  # Adjust the width for the move history table
pygame.display.set_caption("Connect 6")


# Initialize turn counters for both players
red_player_turns = 0
black_player_turns = 0

# Maximum number of turns allowed for each player
max_turns_per_player = 2

# Place one black stone at the center at the beginning
center_x = 9 * CELL_SIZE
center_y = 9 * CELL_SIZE
clicked_points.append((center_x, center_y))
clicked_colors.append('black')
black_player_turns += 1


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Get the mouse coordinates
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Check if the click is near an intersection point
            if is_near_intersection(mouse_x, mouse_y):
                # Calculate the grid coordinates based on the mouse position
                row = mouse_y // CELL_SIZE
                col = mouse_x // CELL_SIZE

                # Determine the color of the circle based on the current player's turn
                circle_color = 'red' if current_player == 'red' else 'black'
            is_colored = False
            for point in clicked_points:
                if point[0] == col * CELL_SIZE and point[1] == row * CELL_SIZE:
                    is_colored = True
                    break
            if not is_colored :
                clicked_points.append((col * CELL_SIZE,row * CELL_SIZE))
                clicked_colors.append(circle_color)
                print(f"Cliked at Row:{row}, Col:{col}")
                
                if current_player == 'red':
                    red_player_turns += 1
                else:
                    black_player_turns += 1
                if (current_player == 'red' and red_player_turns >= 2) or \
                    (current_player == 'black' and black_player_turns >= 2):
                        current_player == 'black' if current_player == 'red' else 'red'
                        red_player_turns = 0
                        black_player_turns = 0
                

                # # Add the clicked point to the list
                # clicked_points.append((col * CELL_SIZE, row * CELL_SIZE))

                # # Add the color of the circle to the color list
                # clicked_colors.append(circle_color)

                # # Print the grid coordinates to the console
                # print(f"Clicked at Row: {row}, Col: {col}")

                # # Increment the turn counter for the current player
                # if current_player == 'red':
                #     red_player_turns += 1
                # else:
                #     black_player_turns += 1

                # # Check if the current player has taken their maximum allowed turns (2 turns)
                # if (current_player == 'red' and red_player_turns >= 2) or \
                #    (current_player == 'black' and black_player_turns >= 2):
                #     # Switch to the other player's turn
                #     current_player = 'black' if current_player == 'red' else 'red'
                #     # Reset the turn counters for both players
                #     red_player_turns = 0
                #     black_player_turns = 0

    screen.fill(BACKGROUND_COLOR)  # Clear the screen
    # Draw the game board and move history table
    draw_board(screen)
    draw_move_history(screen)

    # Draw circles at the clicked points with respective colors
    for (x, y), color in zip(clicked_points, clicked_colors):
        draw_circle(screen, x, y, CIRCLE_RADIUS, color)

    pygame.display.update()

# Quit Pygame
pygame.quit()
