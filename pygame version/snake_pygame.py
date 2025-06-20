import pygame
import random
import time
import os

# Initialize Pygame
pygame.init()

# Window setup
block_size = 20
grid_width = 30
grid_height = 20
width = grid_width * block_size
height = grid_height * block_size
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# Font and clock
font = pygame.font.SysFont("Arial", 24)
clock = pygame.time.Clock()

# Load high score
score = 0
highscore = 0
if os.path.exists("highscore.txt"):
    with open("highscore.txt") as f:
        try:
            highscore = int(f.read())
        except:
            highscore = 0

# Snake and food setup
snake = [[100, 100]]
dx, dy = block_size, 0
food = [random.randint(0, grid_width - 1) * block_size,
        random.randint(0, grid_height - 1) * block_size]

def generate_food():
    while True:
        fx = random.randint(0, grid_width - 1) * block_size
        fy = random.randint(0, grid_height - 1) * block_size
        food_pos = [fx, fy]
        if food_pos not in snake:
            return food_pos

# Game loop
running = True
while running:
    clock.tick(10)  # Adjust speed here (FPS)
    
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -block_size, 0
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = block_size, 0
            elif event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -block_size
            elif event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, block_size

    # Move the snake
    new_head = [snake[0][0] + dx, snake[0][1] + dy]
    snake.insert(0, new_head)

    # Check food collision
    if new_head == food:
        score += 1
        food = generate_food()
    else:
        snake.pop()

    # Check collisions
    if (new_head in snake[1:] or
        new_head[0] < 0 or new_head[0] >= width or
        new_head[1] < 0 or new_head[1] >= height):
        
        # Save new high score if needed
        if score > highscore:
            with open("highscore.txt", "w") as f:
                f.write(str(score))
        # Display Game Over message
        win.fill(BLACK)
        game_over_msg = font.render("GAME OVER", True, RED)
        final_score_msg = font.render(f"Final Score: {score}", True, WHITE)
        win.blit(game_over_msg, (width // 2 - 80, height // 2 - 20))
        win.blit(final_score_msg, (width // 2 - 90, height // 2 + 10))
        pygame.display.update()
        time.sleep(2)
        running = False
        break

    # Draw everything
    win.fill(BLACK)
    pygame.draw.rect(win, WHITE, (0, 0, width, height), 2)  # border
    for segment in snake:
        pygame.draw.rect(win, GREEN, (*segment, block_size, block_size))
        pygame.draw.rect(win, RED, (*food, block_size, block_size))

    # Draw scores
    score_text = font.render(f"Score: {score}", True, WHITE)
    highscore_text = font.render(f"High Score: {highscore}", True, WHITE)
    win.blit(score_text, (10, 10))
    win.blit(highscore_text, (width - 200, 10))

    pygame.display.update()

pygame.quit()
