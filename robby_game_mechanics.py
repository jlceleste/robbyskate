import tkinter as tk
from PIL import Image, ImageTk
import time
import random

# Setup window
root = tk.Tk()
root.configure(bg="grey") 
root.wm_attributes("-transparentcolor", "grey")  # Transparent background (Windows only)
root.attributes('-topmost', True)
root.overrideredirect(True)
root.bind("<Button-3>", lambda e: root.destroy())  # Right-click to close
window = tk.Toplevel(root)
window.title("Robby Game")
window.configure(bg='red')
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = 300
window_height = 150
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
window.geometry(f"{window_width}x{window_height}+{x}+{y}")
title = tk.Label(window, text = "Game", bg = "blue", font=("Modern No. 20", 50), fg="white")
title.grid(row =0, column = 0, columnspan=3, sticky = "news")
start_button = tk.Button(window, text = "Start Game", bg = "blue",command = lambda:start_game(), font=("Modern No. 20", 10), fg="white")
start_button.grid(row =1, column = 1)
choose = tk.Button(window, text = "Choose Character", bg = "blue",command = lambda:choose_character(), font=("Modern No. 20", 10), fg="white")
choose.grid(row =1, column = 0)
# Canvas setup
screen_width = root.winfo_screenwidth()
canvas_height = 150
def choose_character():
    global select
    window.withdraw()
    select = tk.Toplevel(root)
    select.title("Choose Character")
    select.configure(bg='red')
    select.geometry(f"{window_width}x{window_height}+{x}+{y}")
    paths ={"robby":"robby/icon.png"}
    buttons=[]
    char_images = [] 
    for i, (key, value) in enumerate(paths.items()):
        original_image = Image.open(value)
        resized_image = original_image.resize((100, 100))
        photo = ImageTk.PhotoImage(resized_image)
        char_images.append(photo)

        char_button = tk.Button(select, image=photo, command=lambda k=key: save_char(k),
                                bg="white", bd=0)
        char_button.grid(row=0, column=i, padx=10, pady=10)
def save_char(which):
    global push_path, jump_path
    push_path = f"{which}/push.png"
    jump_path = f"{which}/jump.png"
    window.deconify()
    select.destroy()
###############################################
sprite_sheet_pil = Image.open(push_path)
resized_image = sprite_sheet_pil.resize((256, 384))
sprite_sheet_image = ImageTk.PhotoImage(resized_image)
current_image_index =0
rpush = []
sprite_size = 128
sprite_count = 5
sprites_added = 0

for i in range(3):  # rows
    for j in range(2):  # columns
        if sprites_added >= sprite_count:
            break
        sprite_x = j * sprite_size
        sprite_y = i * sprite_size
        cropped_sprite_pil = resized_image.crop((
            sprite_x, sprite_y, sprite_x + sprite_size, sprite_y + sprite_size
        ))
        cropped_sprite_tk = ImageTk.PhotoImage(cropped_sprite_pil)
        rpush.append(cropped_sprite_tk)
        sprites_added += 1
current_image = rpush[0]
item = rpush[0]
rpush.extend([item]*10)

#############################################
sprite_sheet_pil = Image.open(jump_path)
resized_image = sprite_sheet_pil.resize((384, 384))
sprite_sheet_image = ImageTk.PhotoImage(resized_image)
rjump = []
sprite_size = 128
sprite_count = 8
sprites_added = 0

for i in range(3):  # rows
    for j in range(3):  # columns
        if sprites_added >= sprite_count:
            break
        sprite_x = j * sprite_size
        sprite_y = i * sprite_size
        cropped_sprite_pil = resized_image.crop((
            sprite_x, sprite_y, sprite_x + sprite_size, sprite_y + sprite_size
        ))
        cropped_sprite_tk = ImageTk.PhotoImage(cropped_sprite_pil)
        rjump.append(cropped_sprite_tk)
        sprites_added += 1
#################################################
# Physics variables
gravity = 1
dy = 0
dy_top=0
ground = 150
jumping = False
fps = 60
spf = int(1000/fps)
speed = -10
slushie_points = 0


collision = False
class Slushie:
    def __init__(self, canvas, y_placement, color):
        self.canvas = canvas
        self.slushie=canvas.create_oval(screen_width,y_placement,screen_width+10,y_placement+10, fill=color)
        self.move_slushie()
        self.color=color
        
    def check_collision(self):
        global slushie_points
        char_coords = canvas.bbox(character)
        slu_coords = canvas.bbox(self.slushie)
        if (char_coords[2] > slu_coords[0] and char_coords[0] < slu_coords[2] and
            char_coords[3] > slu_coords[1] and char_coords[1] < slu_coords[3]):
            print("slushie")
            if self.color == 'blue':
                slushie_points += 3
            elif self.color == 'green':
                slushie_points += 2
            elif self.color == 'red':
                slushie_points += 1
            canvas.itemconfig(slushie_points_label, text=slushie_points)
            canvas.delete(self.slushie)
                
    def move_slushie(self):
        self.canvas.move(self.slushie, speed, 0)
        slu_coords = self.canvas.coords(self.slushie)
        self.check_collision()
        self.canvas.after(spf, self.move_slushie)
class Obstacle:
    def __init__(self, canvas):
        self.canvas = canvas
        self.obstacle = canvas.create_rectangle(screen_width, canvas_height-10, screen_width + 10, 110 , fill='pink', width=0)
        self.move_obstacle()

    def check_collision(self):
        global collision
        char_coords = canvas.bbox(character)
        obs_coords = canvas.bbox(self.obstacle)

        if (char_coords[2] > obs_coords[0] and char_coords[0] < obs_coords[2] and
            char_coords[3] > obs_coords[1] and char_coords[1] < obs_coords[3]):
            print("💥 Collision detected!")
            collision =True
            # root.destroy()  # Uncomment to stop game on collision

    def move_obstacle(self):
        self.canvas.move(self.obstacle, speed, 0)
        obs_coords = self.canvas.coords(self.obstacle)

        self.check_collision()
        self.canvas.after(spf, self.move_obstacle)

# Jumping logic
def start_jump(event=None):
    global dy, jumping, dy_top
    coords = canvas.bbox(character)
    if not jumping and coords[3] >= ground:
        canvas.itemconfig(character, image=rjump[1])
        dy = -20
        dy_top=dy *-1
        jumping = True
        jump()

def jump():
    global dy, jumping, dy_top
    dy += gravity
    canvas.move(character, 0, dy)
    if dy == int(dy_top * 2/3 *-1):
        canvas.itemconfig(character, image=rjump[2])
    if dy == int(dy_top * 1/3 *-1):
        canvas.itemconfig(character, image=rjump[3])
    if dy == 0:
        canvas.itemconfig(character, image=rjump[4])
    if dy == int(dy_top * 1/3):
        canvas.itemconfig(character, image=rjump[5])
    if dy == int(dy_top * 2/3):
        canvas.itemconfig(character, image=rjump[6])
    if dy == dy_top:
        canvas.itemconfig(character, image=rjump[7])
    coords = coords = canvas.bbox(character)
    if coords[3] >= ground: 
        canvas.coords(character, coords[0], ground - 128)
        dy = 0
        jumping = False
    else:
        canvas.after(spf, jump)
def skate(event=None):
    global current_image_index, current_image, character
    if not jumping:
        current_image_index = (current_image_index + 1) % len(rpush)
        current_image = rpush[current_image_index]
        canvas.itemconfig(character, image=current_image)
    canvas.after(100, skate)
# Key bind
root.bind("<space>", start_jump)
def start_game():
    global character, start_time, canvas
    window   .destroy()
    canvas = tk.Canvas(root, width=screen_width, height=canvas_height, bg="white", bd=0, highlightthickness=0)
    canvas.pack()
    slushie_points_label = canvas.create_text(0, 0, text=slushie_points,
                       font=("Arial", 16, "bold"), fill="blue", anchor="nw")
    start_time = time.time()
    collsion = False
    difficulty = 0.1
    character = canvas.create_image(100, canvas_height-128, image=current_image, anchor="nw")  # starting position
    skate()
    run_game()
def run_game():
    if not collision:
        elapsed_time = time.time() - start_time
        difficulty = min(0.1 + 0.7 * elapsed_time / 300, 0.7)
        if random.choices([1, 0], weights=[difficulty, 1 - difficulty], k=1)[0] == 1:
            O = Obstacle(canvas)
        print(difficulty)
        root.after(1000, run_game)
    else:
        stop_game()

# Start game
#O = Obstacle(canvas)
#s = Slushie(canvas,270,'blue' )
#s = Slushie(c   anvas,270,'red' )

root.mainloop()
