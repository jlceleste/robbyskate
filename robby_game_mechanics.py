import tkinter as tk
from PIL import Image, ImageTk
import time
import random
import json
import os

# Setup window
root = tk.Tk()
root.configure(bg="grey") 
root.wm_attributes("-transparentcolor", "grey")  # Transparent background (Windows only)
root.attributes('-topmost', True)
root.overrideredirect(True)
root.bind("<Button-3>", lambda e: root.destroy())  # Right-click to close
window = tk.Toplevel(root)
window.title("Robby Skate")
window.configure(bg='red')
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = 700
window_height = 200
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
window.columnconfigure(0, weight =1)
window.columnconfigure(1, weight =1)
window.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.geometry(f"{screen_width}x{screen_height}+0+{y}")
title = tk.Label(window, text = "RobbySkate", bg="red", font=("Terminal", 50), fg="white")
title.grid(row =0, column = 0, columnspan=2, sticky = "news")
start_button = tk.Button(window, text = "   Start Game", bd =10, bg = "blue",command = lambda:start_game(), font=("Terminal", 15), fg="white")
start_button.grid(row =3, column = 0, columnspan = 2,sticky = "news")
choose = tk.Frame(window, borderwidth=5, bg="blue", relief ='groove')
choose.grid(row =2, column = 0,sticky = "news")
choose.columnconfigure(0, weight=1)
choose.columnconfigure(1, weight=1)
char = tk.Button(choose, text = "Character", bg = "red",command = lambda:choose_character(), bd =10,font=("Terminal", 15), fg="white")
char.grid(row =0, column = 0,sticky = "news")
bg = tk.Button(choose, text = "Background", bg = "red",command = lambda:choose_back(), bd =10,font=("Terminal", 15), fg="white")
bg.grid(row =0, column = 1,sticky = "news")
# Canvas setup
screen_width = root.winfo_screenwidth()
score_file = "scores.json"
with open(score_file, "r") as f:
    scores = json.load(f)
high_score = scores["high_score"]
slushies = scores["slushies"]
hs = tk.Label(window, text = f"high score: {high_score:.2f}", highlightthickness=5, highlightbackground="red",bg="blue", font=("Terminal", 15), fg="white")
hs.grid(row =1, column = 0,sticky = "news")
sl = tk.Label(window, text = f"slushies: {slushies}", highlightthickness=5, highlightbackground="red",bg="blue",font=("Terminal", 15), fg="white")
sl.grid(row =1, column = 1,sticky = "news")
def show_note():
    note = tk.Toplevel(window)
    note.title("Note")
    note.configure(bg="lightyellow")
    note.geometry(f"{200}x{200}+{x+window_width}+{y}")
    note.resizable(False, False)

    tk.Label(note, text="Robby Tip:\nCollect slushies to unlock characters!", 
             bg="lightyellow", font=("Terminal", 12), wraplength=220, justify="left").pack(pady=10, padx=10)
    tk.Button(note, text="Close", command=note.destroy, font=("Terminal", 10), bg="blue", fg="white").pack(pady=5)

# Add this to your layout:
notes_button = tk.Button(window, text="Notes", bg="red", command=show_note, bd=10, font=("Terminal", 15), fg="white")
notes_button.grid(row=2, column=1,sticky = "news")
push_path = 'robby/push.png'
jump_path = 'robby/jump.png'
original_image = Image.open("red.png")
original_image = original_image.resize((32, 40))
red_slushie = ImageTk.PhotoImage(original_image)
original_image = Image.open("blue.png")
original_image = original_image.resize((32, 40))
blue_slushie = ImageTk.PhotoImage(original_image)
original_image = Image.open("green.png")
original_image = original_image.resize((32, 40))
green_slushie = ImageTk.PhotoImage(original_image)



def choose_character():
    global select
    window.withdraw()
    select = tk.Toplevel(root)
    select.title("Choose Character")
    select.configure(bg='red')
    select.geometry(f"{window_width}x{window_height}+{x}+{y}")
    select.wm_attributes("-transparentcolor", "grey")
    render_select()
def choose_back():
    global back
    window.withdraw()
    back = tk.Toplevel(root)
    back.title("Choose Background")
    back.configure(bg='red')
    back.geometry(f"{window_width}x{window_height}+{x}+{y}")
    back.wm_attributes("-transparentcolor", "grey")
    render_back()
        
def render_select():
    for widget in select.winfo_children():
        widget.destroy()
    buttons=[]
    char_images = []
    sl = tk.Label(select, text = f"slushies: {slushies}", bg="red", font=("Terminal", 15), fg="white")
    sl.grid(row =0, column = 0, columnspan = 2,sticky = "news")
    unlocked_characters = scores["unlocked_characters"]
    for i, (key, value) in enumerate(unlocked_characters.items()):
        if value:
            original_image = Image.open(key +'/icon.png')
            photo = ImageTk.PhotoImage(original_image)
            char_images.append(photo)
            char_button = tk.Button(select, image=photo, command=lambda k=key: save_char(k),
                                bg="red", bd=5)
            char_button.image = photo 
            char_button.grid(row=1, column=i, padx=10)
            char_label = tk.Label(select, text = key,bg = "blue", font=("Terminal", 10), fg="white")
            char_label.grid(row =2, column = i, padx=10, pady=10)
        else:
            original_image = Image.open(key +'/shadow.png')
            photo = ImageTk.PhotoImage(original_image)
            char_images.append(photo)
            char_button = tk.Button(select, image=photo, command=lambda k=key: unlock(k),
                                bg="red", bd=5)
            char_button.image = photo
            char_button.grid(row=1, column=i, padx=10)
            char_label = tk.Label(select, text = "cost: 25",bg = "blue", font=("Terminal", 10), fg="white")
            char_label.grid(row =2, column = i, padx=10,pady=10)
def unlock(which):
    global slushies
    if slushies >= 25:
        scores["unlocked_characters"][which]= True
        slushies = slushies -25
        update_scores()
        render_select()
def save_char(which):
    global push_path, jump_path
    push_path = f"{which}/push.png"
    jump_path = f"{which}/jump.png"
    window.deiconify()
    select.destroy()
def render_back():
    buttons=[]
    char_images = []
    backgrounds = ["houghton","st_clair"]
    for i, background in enumerate(backgrounds):
        original_image = Image.open(background +'/icon.png')
        original_image = original_image.resize((106, 64))
        photo = ImageTk.PhotoImage(original_image)
        char_images.append(photo)
        char_button = tk.Button(back, image=photo, command=lambda k=background: save_back(k),
                            bg="red", bd=5)
        char_button.image = photo 
        char_button.grid(row=1, column=i, padx=10)
        char_label = tk.Label(back, text = background,bg = "blue", font=("Terminal", 10), fg="white")
        char_label.grid(row =2, column = i, padx=10, pady=10)
def save_back(which):
    global back_path, prop_path
    back_path = f"{which}/background.png"
    prop_path = f"{which}/prop.png"
    window.deiconify()
    back.destroy()
###############################################
def load_sprites():
    global rpush, rjump 
    sprite_sheet_pil = Image.open(push_path)
    resized_image = sprite_sheet_pil.resize((256, 384))
    sprite_sheet_image = ImageTk.PhotoImage(resized_image)
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
jumping = False
fps = 60
spf = int(1000/fps)
speed = -10


collision = False
class Slushie:
    def __init__(self, canvas, y_placement, color):
        self.canvas = canvas
        self.color = color
        self.collected = False  # ✅ Track if collected
        self.slushie = character = canvas.create_image(screen_width, y_placement, image=color, anchor="nw")
        #self.slushie = canvas.create_oval(screen_width, y_placement, screen_width + 10, y_placement + 10, fill=color)
        self.move_slushie()

    def check_collision(self):
        global slushie_points, collision, slushie_points_label
        if self.collected or collision:
            return

        char_coords = canvas.bbox(character)
        slu_coords = canvas.bbox(self.slushie)

        if char_coords is None or slu_coords is None:
            return

        if (char_coords[2] > slu_coords[0] and char_coords[0] < slu_coords[2] and
            char_coords[3] > slu_coords[1] and char_coords[1] < slu_coords[3]):
            
            print("Slushie collected!")
            if self.color == blue_slushie:
                slushie_points += 3
            elif self.color == green_slushie:
                slushie_points += 2
            elif self.color == red_slushie:
                slushie_points += 1

            canvas.itemconfig(slushie_points_label, text=slushie_points)
            canvas.delete(self.slushie)
            self.collected = True  

    def move_slushie(self):
        if not self.collected and not collision:
            self.canvas.move(self.slushie, speed, 0)
            self.check_collision()
            self.canvas.after(spf, self.move_slushie)
class Obstacle:
    def __init__(self, canvas):
        self.canvas = canvas
        self.obstacle = canvas.create_rectangle(screen_width, canvas_height-10, screen_width + 10, canvas_height , fill='pink', width=0)
        self.move_obstacle()

    def check_collision(self):
        global collision
        if collision:
            return
        char_coords = canvas.bbox(character)
        obs_coords = canvas.bbox(self.obstacle)

        if (char_coords[2] > obs_coords[0] and char_coords[0] < obs_coords[2] and
            char_coords[3] > obs_coords[1] and char_coords[1] < obs_coords[3]):
            canvas.pack_forget ()
            print("💥 Collision detected!")
            collision =True
            #canvas.itemconfig(character, image=death)
            # root.destroy()  # Uncomment to stop game on collision

    def move_obstacle(self):
        self.canvas.move(self.obstacle, speed, 0)
        obs_coords = self.canvas.coords(self.obstacle)

        self.check_collision()
        self.canvas.after(spf, self.move_obstacle)
        
class Prop:
    def __init__(self, canvas):
        self.canvas = canvas
        original_image = Image.open(prop_path)
        #original_image = original_image.resize((384, 384))
        photo = ImageTk.PhotoImage(resized_image)
        self.prop = canvas.create_image(screen_width, y_placement, image=photo, anchor="nw")
        self.move_prop()

    def move_prop(self):
        self.canvas.move(self.prop, speed/2, 0)
        prop_coords = self.canvas.coords(self.prop)
        self.canvas.after(spf, self.move_prop)

# Jumping logic
def start_jump(event=None):
    global dy, jumping, dy_top
    coords = canvas.bbox(character)
    if not jumping and coords[3] >= ground:
        canvas.itemconfig(character, image=rjump[1])
        dy = -18
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
    global character, start_time, canvas, current_image_index, ground, collision, slushie_points_label, slushie_points, canvas_height,ground
    if 'canvas' in globals() and canvas.winfo_exists():
        canvas.destroy()
    canvas_width = screen_width
    print(screen_width)
    canvas_height = 300
    x = (screen_width // 2) - (canvas_width // 2)
    y = (screen_height // 2) - (canvas_height // 2)
    slushie_points = 0
    current_image_index =0
    load_sprites()
    ground = canvas_height
    print(ground)
    window.withdraw()
    print(screen_width)
    canvas = tk.Canvas(root, width=screen_width, height=canvas_height, bg="white", bd=0, highlightthickness=0)
    canvas.pack()
    canvas.focus_force()
    original_image = Image.open(back_path)
    original_image = original_image.resize((screen_width, 300))
    background = ImageTk.PhotoImage(original_image)
    background= canvas.create_image(0, canvas_height, image=st_clair, anchor="sw")
    slushie_points_label = canvas.Label(0, 0, text= f'slushie points: {slushie_points}',
                       font=("Terminal", 16, "bold"), fill="blue", anchor="nw", bg='red',fg='white')
    start_time  = time.time()
    collision = False
    difficulty = 0.1
    character = canvas.create_image(100, canvas_height-128, image=rpush[0], anchor="nw")  # starting position
    print(canvas.bbox(character))
    skate()
    run_game()
def run_game():
    global elapsed_time, collision
    if not collision:
        elapsed_time = time.time() - start_time
        difficulty = min(0.25  + 0.7 * elapsed_time / 300, 0.7)
        if random.choices([1, 0], weights=[difficulty, 1 - difficulty], k=1)[0] == 1:
            O = Obstacle(canvas)
        if random.choices([1, 0], weights=[0.2, 0.8], k=1)[0] == 1:
            p = Prop(canvas)
        if random.choices([1, 0], weights=[difficulty, 1 - difficulty], k=1)[0] == 1:
            col = random.choice([red_slushie,green_slushie, blue_slushie])
            s = Slushie(canvas,50,col)
        print(difficulty)
        root.after(1000, run_game)
    else:
        stop_game()
def stop_game():
    global slushies, high_score, scores, canvas, hs, sl, slushie_points
    slushies += slushie_points
    if elapsed_time > high_score:
        high_score = elapsed_time
    update_scores()
    hs.config(text=f"high score: {high_score:.2f}")
    sl.config(text=f"slushies: {slushies}")
    window.deiconify()
    canvas.pack_forget()
def update_scores():
    global slushies, high_score, scores
    scores["slushies"] = slushies
    scores["high_score"] = high_score
    with open(score_file, "w") as f:
        json.dump(scores, f)

root.mainloop()