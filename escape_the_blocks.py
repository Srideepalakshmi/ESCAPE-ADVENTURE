import tkinter as tk
from PIL import Image, ImageTk
import random
import time

# -----------------------
# Game Configurations
# -----------------------
WIDTH = 800
HEIGHT = 600
PLAYER_SPEED = 20
INITIAL_BLOCK_SPEED = 6
LIVES = 3
COIN_SCORE = 5  

# -----------------------
# Game Class
# -----------------------
class EscapeAdventure:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Escape Adventure 🚀")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.configure(bg="#0f172a")

        self.player_img = ImageTk.PhotoImage(Image.open("player.png").resize((70, 70)))
        self.block_img = ImageTk.PhotoImage(Image.open("meteor.png").resize((70, 70)))
        self.bg_img = ImageTk.PhotoImage(Image.open("space_bg.jpg").resize((WIDTH, HEIGHT)))
        self.explosion_img = ImageTk.PhotoImage(Image.open("explosion.png").resize((100, 100)))
        self.heart_img = ImageTk.PhotoImage(Image.open("heart.png").resize((30, 30)))
        self.coin_img = ImageTk.PhotoImage(Image.open("coin.png").resize((40, 40)))

        self.main_menu()

    # -----------------------
    # MAIN MENU
    # -----------------------
    def main_menu(self):
        self.clear()
        frame = tk.Frame(self.root, bg="#0f172a", width=WIDTH, height=HEIGHT)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="🌠 ESCAPE ADVENTURE 🌠",
                 font=("Comic Sans MS", 28, "bold"), fg="#38bdf8", bg="#0f172a").pack(pady=80)

        tk.Button(frame, text="▶ PLAY", width=15, height=2,
                  bg="#38bdf8", fg="white", font=("Arial", 16, "bold"),
                  command=self.start_game).pack(pady=20)

        tk.Button(frame, text="ℹ INSTRUCTIONS", width=15, height=2,
                  bg="#22c55e", fg="white", font=("Arial", 16, "bold"),
                  command=self.instructions).pack(pady=20)

        tk.Button(frame, text="✖ EXIT", width=15, height=2,
                  bg="#ef4444", fg="white", font=("Arial", 16, "bold"),
                  command=self.root.destroy).pack(pady=20)

    # -----------------------
    # INSTRUCTIONS
    # -----------------------
    def instructions(self):
        self.clear()
        frame = tk.Frame(self.root, bg="#1e293b")
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="🕹 HOW TO PLAY 🕹",
                 font=("Comic Sans MS", 24, "bold"), fg="#38bdf8", bg="#1e293b").pack(pady=30)

        tk.Label(frame, text=f"""🌌 Move with Arrow Keys (↑ ↓ ← →)
🌠 Avoid the Meteors Falling from Above
💰 Collect Coins for +{COIN_SCORE} Points
❤️ You Have 3 Lives — Don’t Lose Them!
📈 Level is shown below hearts and updates with score!""",
                 font=("Arial", 16), fg="white", bg="#1e293b", justify="center").pack(pady=20)

        tk.Button(frame, text="⬅ BACK", bg="#22c55e", fg="white",
                  font=("Arial", 16, "bold"), command=self.main_menu).pack(pady=30)

    # -----------------------
    # START GAME
    # -----------------------
    def start_game(self):
        self.clear()
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

       
        self.bg1 = self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
        self.bg2 = self.canvas.create_image(0, -HEIGHT, image=self.bg_img, anchor="nw")

        
        self.player = self.canvas.create_image(WIDTH // 2, HEIGHT - 80, image=self.player_img)

        self.blocks = []
        self.coins = []
        self.running = True
        self.score = 0
        self.lives = LIVES
        self.last_spawn = time.time()
        self.last_coin_spawn = time.time()
        self.last_update = time.time()
        self.level = 1
        self.block_speed = INITIAL_BLOCK_SPEED
        self.spawn_interval = 1.0
        self.coin_interval = 3.0  # spawn coins every 3 seconds

        
        self.score_text = self.canvas.create_text(100, 30, text="Score: 0",
                                                  font=("Arial", 18, "bold"), fill="white")

       
        self.hearts = []
        for i in range(self.lives):
            x_pos = WIDTH - (i + 1) * 40
            heart = self.canvas.create_image(x_pos, 30, image=self.heart_img)
            self.hearts.append(heart)

  
        self.level_text = self.canvas.create_text(WIDTH - 80, 70,
                                                  text="Level 1: Rookie",
                                                  font=("Arial", 16, "bold"), fill="#facc15")

        
        self.root.bind("<Left>", lambda e: self.move_player(-PLAYER_SPEED, 0))
        self.root.bind("<Right>", lambda e: self.move_player(PLAYER_SPEED, 0))
        self.root.bind("<Up>", lambda e: self.move_player(0, -PLAYER_SPEED))
        self.root.bind("<Down>", lambda e: self.move_player(0, PLAYER_SPEED))

        self.update_game()

    # -----------------------
    # MOVE PLAYER
    # -----------------------
    def move_player(self, dx, dy):
        x, y = self.canvas.coords(self.player)
        new_x = min(max(x + dx, 40), WIDTH - 40)
        new_y = min(max(y + dy, 40), HEIGHT - 40)
        self.canvas.coords(self.player, new_x, new_y)

    # -----------------------
    # SPAWN BLOCK
    # -----------------------
    def spawn_block(self):
        x = random.randint(50, WIDTH - 50)
        block = self.canvas.create_image(x, 0, image=self.block_img)
        self.blocks.append(block)

    # -----------------------
    # SPAWN COIN (falling)
    # -----------------------
    def spawn_coin(self):
        x = random.randint(50, WIDTH - 50)
        coin = self.canvas.create_image(x, 0, image=self.coin_img)
        self.coins.append(coin)

    # -----------------------
    # UPDATE GAME LOOP
    # -----------------------
    def update_game(self):
        if not self.running:
            return

        now = time.time()
        scroll_speed = 2

        
        self.canvas.move(self.bg1, 0, scroll_speed)
        self.canvas.move(self.bg2, 0, scroll_speed)
        y1, y2 = self.canvas.coords(self.bg1)[1], self.canvas.coords(self.bg2)[1]
        if y1 >= HEIGHT: self.canvas.coords(self.bg1, 0, y2 - HEIGHT)
        if y2 >= HEIGHT: self.canvas.coords(self.bg2, 0, y1 - HEIGHT)

       
        if now - self.last_spawn > self.spawn_interval:
            self.spawn_block()
            self.last_spawn = now

        
        if now - self.last_coin_spawn > self.coin_interval:
            self.spawn_coin()
            self.last_coin_spawn = now

        
        for block in self.blocks[:]:
            self.canvas.move(block, 0, self.block_speed)
            bx, by = self.canvas.coords(block)
            if by > HEIGHT:
                self.canvas.delete(block)
                self.blocks.remove(block)
            elif self.check_collision(block):
                self.trigger_explosion(bx, by)
                self.lives -= 1
                self.canvas.delete(self.hearts[-1])
                self.hearts.pop()
                self.canvas.delete(block)
                self.blocks.remove(block)
                if self.lives <= 0:
                    self.game_over()
                    return

        
        for coin in self.coins[:]:
            self.canvas.move(coin, 0, self.block_speed - 2)  # coins fall slightly slower
            cx, cy = self.canvas.coords(coin)
            if cy > HEIGHT:
                self.canvas.delete(coin)
                self.coins.remove(coin)
            elif self.check_collision(coin):
                self.score += COIN_SCORE
                self.canvas.delete(coin)
                self.coins.remove(coin)

        
        if now - self.last_update >= 1:
            self.score += 1
            self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
            self.last_update = now
            self.update_level()

        self.root.after(30, self.update_game)

    # -----------------------
    # UPDATE LEVEL
    # -----------------------
    def update_level(self):
        previous_level = self.level
        if self.score < 20:
            self.level = 1
            self.block_speed = INITIAL_BLOCK_SPEED
            self.spawn_interval = 1.0
            level_name = "Rookie"
        elif self.score < 40:
            self.level = 2
            self.block_speed = INITIAL_BLOCK_SPEED + 2
            self.spawn_interval = 0.9
            level_name = "Fighter"
        elif self.score < 60:
            self.level = 3
            self.block_speed = INITIAL_BLOCK_SPEED + 4
            self.spawn_interval = 0.8
            level_name = "Survivor"
        else:
            self.level = 4
            self.block_speed = INITIAL_BLOCK_SPEED + 6
            self.spawn_interval = 0.7
            level_name = "Legend"

        self.canvas.itemconfig(self.level_text, text=f"Level {self.level}: {level_name}")

        if self.level != previous_level:
            self.show_level_name_popup(level_name)

    # -----------------------
    # SHOW LEVEL POPUP
    # -----------------------
    def show_level_name_popup(self, name):
        popup = self.canvas.create_text(WIDTH / 2, HEIGHT / 2 - 150,
                                        text=f"LEVEL {self.level}: {name}",
                                        font=("Arial", 24, "bold"), fill="#facc15")
        self.root.after(1200, lambda: self.canvas.delete(popup))

    # -----------------------
    # EXPLOSION EFFECT
    # -----------------------
    def trigger_explosion(self, x, y):
        explosion = self.canvas.create_image(x, y, image=self.explosion_img)
        self.root.after(400, lambda: self.canvas.delete(explosion))

    # -----------------------
    # COLLISION DETECTION
    # -----------------------
    def check_collision(self, obj):
        px, py = self.canvas.coords(self.player)
        ox, oy = self.canvas.coords(obj)
        distance = ((px - ox) ** 2 + (py - oy) ** 2) ** 0.5
        return distance < 50

    # -----------------------
    # GAME OVER
    # -----------------------
    def game_over(self):
        self.running = False
        self.canvas.create_text(WIDTH / 2, HEIGHT / 2 - 50, text="💀 GAME OVER 💀",
                                fill="#ef4444", font=("Arial", 28, "bold"))
        self.canvas.create_text(WIDTH / 2, HEIGHT / 2, text=f"Your Score: {self.score}",
                                fill="white", font=("Arial", 20, "bold"))

        play_again_btn = tk.Button(self.root, text="Play Again", font=("Arial", 14, "bold"),
                                   bg="#22c55e", fg="white", command=self.start_game)
        self.canvas.create_window(WIDTH / 2, HEIGHT / 2 + 60, window=play_again_btn)

        menu_btn = tk.Button(self.root, text="Main Menu", font=("Arial", 14, "bold"),
                             bg="#38bdf8", fg="white", command=self.main_menu)
        self.canvas.create_window(WIDTH / 2, HEIGHT / 2 + 110, window=menu_btn)

    # -----------------------
    # CLEAR FRAME
    # -----------------------
    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()


# -----------------------
# RUN GAME
# -----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = EscapeAdventure(root)
    root.mainloop()
