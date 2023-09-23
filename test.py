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

# Define the boundaries of the Connect 6 table
TABLE_LEFT = CELL_SIZE
TABLE_RIGHT = WIDTH - CELL_SIZE
TABLE_TOP = CELL_SIZE
TABLE_BOTTOM = HEIGHT - CELL_SIZE

# Initialize move history list
move_history = []

# List to store the clicked points
clicked_points = []

# List to store the colors of the clicked points
clicked_colors = []

# Variables to store the types of players (human or AI)
player1_type = 'human'  # Default to human player for Player 1
player2_type = 'human'  # Default to human player for Player 2

# Placeholder function for the AI player's move
def ai_player_move():
    pass  # Implement the AI logic here

# Variable to keep track of the current player's turn
current_player = 'red'  # Start with red player

# Function to draw the game board
def draw_board(screen):
    screen.fill(BACKGROUND_COLOR)

    for x in range(CELL_SIZE, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (x, TABLE_TOP), (x, TABLE_BOTTOM), 1)

    for y in range(CELL_SIZE, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (TABLE_LEFT, y), (TABLE_RIGHT, y), 1)

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

# Function to check if the mouse click is within the Connect 6 table
def is_within_table(mouse_x, mouse_y):
    return (
        TABLE_LEFT < mouse_x < TABLE_RIGHT
        and TABLE_TOP < mouse_y < TABLE_BOTTOM
    )

# Function to check if the mouse click is near an intersection point
def is_near_intersection(mouse_x, mouse_y, threshold=5):
    if not is_within_table(mouse_x, mouse_y):
        return False

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

# Create the game window
screen = pygame.display.set_mode((WIDTH + 150, HEIGHT))  # Adjust the width for the move history table
pygame.display.set_caption("Connect 6")

# Function to display player type selection
def player_type_selection():
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.Font(None, 36)
    text_color = BLACK
    text1 = font.render("Player 1: Choose Type (H)uman / (A)I", True, text_color)
    text2 = font.render("Player 2: Choose Type (H)uman / (A)I", True, text_color)
    text1_rect = text1.get_rect()
    text2_rect = text2.get_rect()
    text1_rect.center = (WIDTH // 2, HEIGHT // 4)
    text2_rect.center = (WIDTH // 2, HEIGHT // 4 + 50)
    screen.blit(text1, text1_rect)
    screen.blit(text2, text2_rect)
    pygame.display.flip()

player_type_selection()

# Player type selection loop
player1_selected = False
player2_selected = False
while not (player1_selected and player2_selected):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if not player1_selected:
                if event.key == pygame.K_h:
                    player1_type = 'human'
                    player1_selected = True
                elif event.key == pygame.K_a:
                    player1_type = 'ai'
                    player1_selected = True
            elif not player2_selected:
                if event.key == pygame.K_h:
                    player2_type = 'human'
                    player2_selected = True
                elif event.key == pygame.K_a:
                    player2_type = 'ai'
                    player2_selected = True

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check for left mouse button click
            # Get the mouse coordinates
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Check if the click is within the Connect 6 table
            if is_within_table(mouse_x, mouse_y) and is_near_intersection(mouse_x, mouse_y):
                # Calculate the grid coordinates based on the mouse position
                row = mouse_y // CELL_SIZE
                col = mouse_x // CELL_SIZE

                # Determine the color of the circle based on the current player's turn
                circle_color = 'red' if current_player == 'red' else 'black'

                # Add the clicked point to the list
                clicked_points.append((col * CELL_SIZE, row * CELL_SIZE))

                # Print the grid coordinates to the console
                print(f"Clicked at Row: {row}, Col: {col}")

                # Switch to the other player's turn
                current_player = 'black' if current_player == 'red' else 'red'

                # If player 2 is AI, call the AI player function
                if current_player == 'black' and player2_type == 'ai':
                    ai_player_move()  # Implement AI logic here

    # Perform game logic here

    # Draw the game board and move history table
    draw_board(screen)
    draw_move_history(screen)

    # Draw circles at the clicked points with respective colors
    for (x, y), color in zip(clicked_points, clicked_colors):
        draw_circle(screen, x, y, 10, color)

    pygame.display.flip()

pygame.quit()
