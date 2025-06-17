import curses
import random
import time

# Setup the screen
screen = curses.initscr()
curses.curs_set(0)
height, width = 20, 60
win = curses.newwin(height, width, 0, 0)
win.keypad(1)
win.timeout(100)
win.border()

# Setup score and highscore
score = 0
# Load high score from file (create if missing)
try:
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())
except:
    highscore = 0

# Initiate snake and food
snake = [[5, 10], [5, 9], [5, 8]]
while True:
    food = [random.randint(1, height - 2), random.randint(1, width - 2)]
    if food not in snake:
        break
win.addch(food[0], food[1], 'O')

# Initiate direction
key = curses.KEY_RIGHT

while True:
    win.border()
    win.addstr(0, 6, f' Score: {score} ')
    win.addstr(0, width - 20, f' High Score: {highscore} ')
    next_key = win.getch()
    key = key if next_key == -1 else next_key

    # Calculate new head
    head = [snake[0][0], snake[0][1]]
    if key == curses.KEY_DOWN:
        head[0] += 1
    if key == curses.KEY_UP:
        head[0] -= 1
    if key == curses.KEY_LEFT:
        head[1] -= 1
    if key == curses.KEY_RIGHT:
        head[1] += 1

    snake.insert(0, head)

    # Collision
    if (
        head[0] in [0, height] or
        head[1] in [0, width] or
        head in snake[1:]
    ):
        if score > highscore:
            with open("highscore.txt", "w") as f:
                f.write(str(score))
    # Display Game Over and Final Score
        win.addstr(height // 2 - 2, width // 2 - 5, "GAME OVER")
        win.addstr(height // 2 - 1, width // 2 - 7, f"Final Score: {score}")
        win.refresh()
        time.sleep(2)
    # Close the window
        curses.endwin()
        quit()

    # Eating food
    if head == food:
    # Update the score
        score += 1
    # Generate new food that is NOT inside the snake
        while True:
            new_food = [random.randint(1, height - 2), random.randint(1, width - 2)]
            if new_food not in snake:
                food = new_food
                break

        win.addch(food[0], food[1], 'O')
    else:
        tail = snake.pop()
        win.addch(tail[0], tail[1], ' ')
    # Draw snake
    win.addch(snake[0][0], snake[0][1], '*')
