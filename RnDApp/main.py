import tkinter as tk
from tkinter import messagebox
import random, threading, time, pyttsx3, pygame, os, hashlib

# ---------------- CONFIGURATION ----------------
DEFAULT_WORK_DURATION = 20 * 60      # default 20 min
DEFAULT_BREAK_DURATION = 60          # default 1 min
WARNING_BEFORE_LOCK = 10             # seconds before lock
MUSIC_FILE = "relax.mp3"
PASSWORD_FILE = "password.txt"

# ---------------- EXERCISES ----------------
exercises = [
    "Blink your eyes slowly 10 times.",
    "Rub your palms together and place them over your eyes.",
    "Rotate your shoulders forward and backward 10 times.",
    "Roll your wrists slowly.",
    "Take 5 deep breaths — in through the nose, out through the mouth.",
    "Look up, down, left, and right — stretch your eyes.",
    "Massage your forehead gently.",
    "Sit straight — align your back and relax your shoulders."
]

# ---------------- QUOTES ----------------
quotes = [
    "Your health is more important than the screen.",
    "Take care of your eyes — they serve you for life.",
    "A short break improves long-term focus.",
    "Relax now, focus better later.",
    "Good posture, good productivity."
]

# ---------------- SPEECH ENGINE ----------------
engine = pyttsx3.init()
engine.setProperty('rate', 175)

def speak_async(text):
    threading.Thread(target=lambda: (engine.say(text), engine.runAndWait()), daemon=True).start()

# ---------------- MUSIC ----------------
def play_music():
    try:
        pygame.mixer.init()
        if os.path.exists(MUSIC_FILE):
            pygame.mixer.music.load(MUSIC_FILE)
            pygame.mixer.music.play(-1)
    except Exception as e:
        print("Music error:", e)

def stop_music():
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()

# ---------------- PASSWORD UTILS ----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_password(password):
    with open(PASSWORD_FILE, "w") as f:
        f.write(hash_password(password))

def verify_password(password):
    if not os.path.exists(PASSWORD_FILE):
        return False
    with open(PASSWORD_FILE, "r") as f:
        stored = f.read().strip()
    return stored == hash_password(password)

def is_first_time_user():
    return not os.path.exists(PASSWORD_FILE)

# ---------------- MAIN APP ----------------
class FocusMateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FocusMate: Smart Work–Break Assistant")
        self.root.configure(bg="black")
        self.root.geometry("800x500")
        self.root.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.current_frame = None
        self.running = True
        self.work_duration = DEFAULT_WORK_DURATION
        self.break_duration = DEFAULT_BREAK_DURATION

        if is_first_time_user():
            self.show_password_setup_screen()
        else:
            self.show_start_screen()

    def disable_event(self, event=None):
        pass

    def show_frame(self, frame):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame
        self.current_frame.pack(expand=True, fill="both")

    # ---------------- START SCREEN ----------------
    def show_start_screen(self):
        frame = tk.Frame(self.root, bg="#000814")
        self.show_frame(frame)

        tk.Label(frame, text="🌙 FocusMate",
                 font=("Helvetica", 48, "bold"), fg="#00FFFF", bg="#000814").pack(pady=50)

        tk.Label(frame, text="Smart Work–Break Assistant",
                 font=("Helvetica", 24), fg="#00FFAA", bg="#000814").pack(pady=10)

        # Work & Break duration input
        tk.Label(frame, text="Work Duration (minutes):", fg="white", bg="#000814", font=("Helvetica", 16)).pack(pady=(40, 5))
        work_entry = tk.Entry(frame, font=("Helvetica", 16), justify="center", width=10)
        work_entry.insert(0, str(DEFAULT_WORK_DURATION // 60))
        work_entry.pack()

        tk.Label(frame, text="Break Duration (minutes):", fg="white", bg="#000814", font=("Helvetica", 16)).pack(pady=(20, 5))
        break_entry = tk.Entry(frame, font=("Helvetica", 16), justify="center", width=10)
        break_entry.insert(0, str(DEFAULT_BREAK_DURATION // 60))
        break_entry.pack()

        def start_session():
            try:
                work_min = int(work_entry.get())
                break_min = int(break_entry.get())
                if work_min <= 0 or break_min <= 0:
                    raise ValueError
                self.work_duration = work_min * 60
                self.break_duration = break_min * 60
                self.start_work_phase()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid positive numbers.")

        tk.Button(frame, text="Start Work Session", command=start_session,
                  font=("Helvetica", 20, "bold"), bg="#00AAFF", fg="white", width=20).pack(pady=30)

        tk.Button(frame, text="Change Password", command=self.show_change_password_screen,
                  font=("Helvetica", 16), bg="#111111", fg="white", width=20).pack(pady=10)

        tk.Button(frame, text="Exit", command=self.root.destroy,
                  font=("Helvetica", 16), bg="#FF3333", fg="white", width=20).pack(pady=10)

    # ---------------- PASSWORD SETUP ----------------
    def show_password_setup_screen(self):
        frame = tk.Frame(self.root, bg="#000814")
        self.show_frame(frame)

        tk.Label(frame, text="🔐 Set Your FocusMate Password",
                 font=("Helvetica", 24, "bold"), fg="#00FFFF", bg="#000814").pack(pady=30)

        entry1 = tk.Entry(frame, show="*", font=("Helvetica", 18), justify="center", width=20)
        entry1.pack(pady=10)
        tk.Label(frame, text="Enter Password", fg="white", bg="#000814").pack()

        entry2 = tk.Entry(frame, show="*", font=("Helvetica", 18), justify="center", width=20)
        entry2.pack(pady=10)
        tk.Label(frame, text="Confirm Password", fg="white", bg="#000814").pack()

        def set_password():
            p1, p2 = entry1.get(), entry2.get()
            if len(p1) < 4:
                messagebox.showerror("Error", "Password must be at least 4 characters long.")
                return
            if p1 != p2:
                messagebox.showerror("Error", "Passwords do not match.")
                return
            save_password(p1)
            messagebox.showinfo("Success", "Password set successfully!")
            self.show_start_screen()

        tk.Button(frame, text="Save & Continue", command=set_password,
                  font=("Helvetica", 18, "bold"), bg="#00AAFF", fg="white").pack(pady=30)

    # ---------------- CHANGE PASSWORD ----------------
    def show_change_password_screen(self):
        frame = tk.Frame(self.root, bg="#000814")
        self.show_frame(frame)

        tk.Label(frame, text="🔑 Change Password",
                 font=("Helvetica", 28, "bold"), fg="#00FFFF", bg="#000814").pack(pady=40)

        old_pw = tk.Entry(frame, show="*", font=("Helvetica", 18), justify="center", width=20)
        old_pw.pack(pady=10)
        tk.Label(frame, text="Enter Old Password", fg="white", bg="#000814").pack()

        new_pw = tk.Entry(frame, show="*", font=("Helvetica", 18), justify="center", width=20)
        new_pw.pack(pady=10)
        tk.Label(frame, text="Enter New Password", fg="white", bg="#000814").pack()

        confirm_pw = tk.Entry(frame, show="*", font=("Helvetica", 18), justify="center", width=20)
        confirm_pw.pack(pady=10)
        tk.Label(frame, text="Confirm New Password", fg="white", bg="#000814").pack()

        def change_pw():
            if not verify_password(old_pw.get()):
                messagebox.showerror("Error", "Old password incorrect.")
                return
            if new_pw.get() != confirm_pw.get():
                messagebox.showerror("Error", "Passwords do not match.")
                return
            if len(new_pw.get()) < 4:
                messagebox.showerror("Error", "Password too short.")
                return
            save_password(new_pw.get())
            messagebox.showinfo("Success", "Password changed successfully!")
            self.show_start_screen()

        tk.Button(frame, text="Change Password", command=change_pw,
                  font=("Helvetica", 18, "bold"), bg="#00AAFF", fg="white").pack(pady=30)

        tk.Button(frame, text="Back", command=self.show_start_screen,
                  font=("Helvetica", 14), bg="#222", fg="white").pack()

    # ---------------- WORK PHASE ----------------
    def start_work_phase(self):
        self.root.attributes("-fullscreen", False)
        frame = tk.Frame(self.root, bg="black")
        self.show_frame(frame)

        window_width, window_height = 300, 180
        screen_width = self.root.winfo_screenwidth()
        x_position = screen_width - window_width - 20
        y_position = 20
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.attributes("-topmost", True)

        self.root.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.root.bind("<Alt-F4>", self.disable_event)
        self.root.bind("<Escape>", self.disable_event)

        tk.Label(frame, text="💻 WORK TIME – STAY FOCUSED",
                 font=("Helvetica", 14, "bold"), fg="#00FFAA", bg="black").pack(pady=10)
        self.timer_label = tk.Label(frame, font=("Consolas", 36, "bold"),
                                    fg="#00FFFF", bg="black")
        self.timer_label.pack(pady=10)
        tk.Label(frame, text="(Cannot be closed)",
                 font=("Helvetica", 10), fg="gray", bg="black").pack(pady=5)

        speak_async("Work time started. Stay focused.")
        self.countdown(self.work_duration, self.start_warning_phase)

    # ---------------- WARNING PHASE ----------------
    def start_warning_phase(self):
        self.root.attributes("-fullscreen", True)
        frame = tk.Frame(self.root, bg="#111111")
        self.show_frame(frame)

        tk.Label(frame, text="⚠️ Break Incoming Soon!",
                 font=("Helvetica", 48, "bold"), fg="#FFD700", bg="#111111").pack(pady=80)
        tk.Label(frame, text="Save your work. Screen will lock soon.",
                 font=("Helvetica", 28), fg="white", bg="#111111").pack(pady=20)

        self.timer_label = tk.Label(frame, font=("Consolas", 72, "bold"),
                                    fg="#FFA500", bg="#111111")
        self.timer_label.pack(pady=40)

        speak_async("Screen will lock soon. Please save your work.")
        self.countdown(WARNING_BEFORE_LOCK, self.start_break_phase)

    # ---------------- BREAK PHASE ----------------
    def start_break_phase(self):
        self.root.attributes("-fullscreen", True)
        frame = tk.Frame(self.root, bg="black")
        self.show_frame(frame)

        quote = random.choice(quotes)
        tk.Label(frame, text="🔒 SCREEN LOCKED – TAKE A BREAK",
                 font=("Helvetica", 48, "bold"), fg="white", bg="black").pack(pady=60)

        self.exercise_label = tk.Label(frame, text="", font=("Helvetica", 32, "bold"),
                                       fg="#FFA500", bg="black", wraplength=1200, justify="center")
        self.exercise_label.pack(pady=30)

        self.quote_label = tk.Label(frame, text=quote, font=("Helvetica", 26, "italic"),
                                    fg="#00FFAA", bg="black", wraplength=1000, justify="center")
        self.quote_label.pack(pady=40)

        self.timer_label = tk.Label(frame, font=("Consolas", 64, "bold"),
                                    fg="#00FFFF", bg="black")
        self.timer_label.pack(pady=40)

        tk.Button(frame, text="ABORT", font=("Helvetica", 24, "bold"),
                  bg="#FF3333", fg="white", width=10, command=self.show_password_window).pack(pady=40)

        speak_async("Time for a break. Relax and rest your eyes.")
        play_music()
        self.exercise_index = 0
        self.exercise_duration = self.break_duration // len(exercises)
        self.rotate_exercises()
        self.countdown(self.break_duration, self.end_break_phase)

    # ---------------- ROTATE EXERCISES ----------------
    def rotate_exercises(self):
        if not self.running:
            return
        if self.exercise_index < len(exercises):
            exercise = exercises[self.exercise_index]
            self.exercise_label.config(text=exercise)
            speak_async(exercise)
            self.exercise_index += 1
            self.root.after(self.exercise_duration * 1000, self.rotate_exercises)

    # ---------------- PASSWORD WINDOW ----------------
    def show_password_window(self):
        # Remove topmost so dialog appears above fullscreen
        self.root.attributes("-topmost", False)
        pw_window = tk.Toplevel(self.root)
        pw_window.title("Enter Password")
        pw_window.geometry("350x200")
        pw_window.configure(bg="#111111")
        pw_window.grab_set()
        pw_window.focus_force()
        pw_window.attributes("-topmost", True)

        tk.Label(pw_window, text="Enter Password to Exit:",
                 fg="white", bg="#111111", font=("Helvetica", 16)).pack(pady=15)
        pw_entry = tk.Entry(pw_window, show="*", font=("Helvetica", 16), justify="center")
        pw_entry.pack(pady=10)
        feedback_label = tk.Label(pw_window, text="", bg="#111111", fg="red", font=("Helvetica", 12))
        feedback_label.pack(pady=5)

        def check_password():
            if verify_password(pw_entry.get()):
                pw_window.destroy()
                stop_music()
                speak_async("Access granted. Exiting now.")
                self.running = False
                self.root.destroy()
            else:
                feedback_label.config(text="❌ Incorrect password! Try again.")

        def on_close():
            pw_window.destroy()
            self.root.attributes("-topmost", True)

        pw_window.protocol("WM_DELETE_WINDOW", on_close)

        tk.Button(pw_window, text="Submit", command=check_password,
                  font=("Helvetica", 14, "bold"), bg="#00AAFF", fg="white").pack(pady=15)

    # ---------------- END BREAK ----------------
    def end_break_phase(self):
        stop_music()
        speak_async("Break over. Time to get back to work.")
        self.start_work_phase()

    # ---------------- COUNTDOWN ----------------
    def countdown(self, duration, callback):
        def update():
            mins, secs = divmod(duration, 60)
            self.timer_label.config(text=f"{mins:02}:{secs:02}")
            if duration > 0 and self.running:
                self.root.after(1000, lambda: self.countdown(duration - 1, callback))
            else:
                callback()
        update()

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    print("FocusMate starting...")
    root = tk.Tk()
    app = FocusMateApp(root)
    root.mainloop()
