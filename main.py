import tkinter as tk
import random

# Configurations
GAME_WIDTH = 700
GAME_HEIGHT = 500
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#1E1E1E"
TEXT_COLOR = "#FFFFFF"
MENU_BACKGROUND = "#333333"
BUTTON_COLOR = "#444444"
BUTTON_TEXT_COLOR = "#FFFFFF"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, int(GAME_WIDTH/SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT/SPACE_SIZE)-1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def start_game():
    global score, direction, snake, food, SPEED
    score = 0
    direction = 'down'
    
    canvas.delete(tk.ALL)
    label.config(text="Score:{}".format(score))
    
    snake = Snake()
    food = Food()

    next_turn(snake, food)

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == 'up':
        y -= SPACE_SIZE
    elif direction == 'down':
        y += SPACE_SIZE
    elif direction == 'left':
        x -= SPACE_SIZE
    elif direction == 'right':
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction

    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    canvas.delete(tk.ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas', 70), text="GAME OVER", fill=TEXT_COLOR, tag="gameover")
    window.after(5000, show_menu)

def show_menu():
    canvas.pack_forget()
    label.pack_forget()
    settings_frame.pack_forget()
    menu_frame.pack(fill='both', expand=True)

def show_settings():
    menu_frame.pack_forget()
    settings_frame.pack(fill='both', expand=True)

def save_settings():
    global SPEED
    speed_value = speed_var.get()
    SPEED = int(500 / speed_value)  # Example: SPEED=100 for speed_value=5
    show_menu()

def start_button_click():
    menu_frame.pack_forget()
    label.pack()
    canvas.pack()
    start_game()

def show_rules():
    canvas.delete(tk.ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas', 20), text="Use arrow keys to move the snake.\nEat food to grow.\nDon't collide with walls or yourself!", fill=TEXT_COLOR, tag="rules")
    window.after(5000, show_menu)

window = tk.Tk()
window.title("Snake")
window.resizable(False, False)

score = 0
direction = 'down'
SPEED = 100

label = tk.Label(window, text="Score:{}".format(score), font=('consolas', 40), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)

canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)

menu_frame = tk.Frame(window, bg=MENU_BACKGROUND)
menu_title = tk.Label(menu_frame, text="Snake Game", font=('consolas', 50), fg=TEXT_COLOR, bg=MENU_BACKGROUND)
menu_title.pack(pady=20)

start_button = tk.Button(menu_frame, text="Start Game", font=('consolas', 20), bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, command=start_button_click)
start_button.pack(pady=10)

rules_button = tk.Button(menu_frame, text="Rules", font=('consolas', 20), bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, command=show_rules)
rules_button.pack(pady=10)

settings_button = tk.Button(menu_frame, text="Settings", font=('consolas', 20), bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, command=show_settings)
settings_button.pack(pady=10)

exit_button = tk.Button(menu_frame, text="Exit", font=('consolas', 20), bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, command=window.quit)
exit_button.pack(pady=10)

settings_frame = tk.Frame(window, bg=MENU_BACKGROUND)
settings_title = tk.Label(settings_frame, text="Settings", font=('consolas', 50), fg=TEXT_COLOR, bg=MENU_BACKGROUND)
settings_title.pack(pady=20)

speed_label = tk.Label(settings_frame, text="Speed:", font=('consolas', 20), fg=TEXT_COLOR, bg=MENU_BACKGROUND)
speed_label.pack(pady=10)
speed_var = tk.IntVar(value=5)
speed_scale = tk.Scale(settings_frame, from_=1, to=10, orient='horizontal', variable=speed_var, font=('consolas', 20), bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, troughcolor=TEXT_COLOR)
speed_scale.pack(pady=10)

save_button = tk.Button(settings_frame, text="Save", font=('consolas', 20), bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, command=save_settings)
save_button.pack(pady=10)

menu_frame.pack(fill='both', expand=True)

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

window.mainloop()
