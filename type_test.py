import tkinter as tk
from tkinter import ttk, font
import time
import json
import os
import random
from datetime import datetime

# ── Word banks by difficulty ──────────────────────────────────────────────────
WORD_BANKS = {
    "Easy": [
        "the quick brown fox jumps over the lazy dog",
        "she sells seashells by the seashore every day",
        "pack my box with five dozen liquor jugs now",
        "how much wood would a woodchuck chuck if it could",
        "all good things must come to an end someday",
        "a stitch in time saves nine good needles",
        "the early bird always catches the worm in spring",
        "look before you leap into every new adventure",
        "practice makes perfect so keep going every single day",
        "better late than never when you arrive at last",
    ],
    "Medium": [
        "programming is the art of telling another human what one wants the computer to do",
        "the greatest glory in living lies not in never falling but in rising every time we fall",
        "the way to get started is to quit talking and begin doing what you love",
        "your time is limited so do not waste it living someone else's life every day",
        "if life were predictable it would cease to be life and be without flavor entirely",
        "if you look at what you have in life you will always have more than enough",
        "if you set your goals ridiculously high and it is a failure you will fail above everyone",
        "life is not measured by the number of breaths we take but by the moments that take our breath",
        "many of life's failures are people who did not realize how close they were to success",
        "you have brains in your head and feet in your shoes you can steer yourself any direction",
    ],
    "Hard": [
        "the implementation of asynchronous programming paradigms requires careful consideration of concurrency and thread synchronization mechanisms",
        "polymorphism in object-oriented programming allows methods to be overridden in derived classes enabling more flexible and extensible code architecture",
        "cryptographic hash functions produce fixed-size digests from arbitrary-length inputs making collision resistance a fundamental security property",
        "quantum entanglement describes a phenomenon where two particles become correlated such that measurement of one instantly influences the other regardless of distance",
        "the Fibonacci sequence demonstrates exponential growth patterns found throughout nature including spiral arrangements in sunflowers and nautilus shells",
        "microservices architecture decomposes monolithic applications into loosely coupled independently deployable services communicating through well-defined interfaces",
        "the Byzantine Generals Problem illustrates the challenges of achieving consensus in distributed systems where components may fail or send conflicting messages",
        "gradient descent optimization iteratively adjusts model parameters in the direction that minimizes the loss function across the training dataset",
        "the CAP theorem states that distributed data stores can provide only two of three guarantees: consistency availability and partition tolerance",
        "recursive algorithms solve problems by breaking them into smaller subproblems of the same type until reaching a base case that can be solved directly",
    ],
}

SCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scores.json")

# ── Colour palette ─────────────────────────────────────────────────────────────
BG       = "#0f0f14"
SURFACE  = "#1a1a24"
CARD     = "#22222f"
ACCENT   = "#7c6af7"
ACCENT2  = "#a78bfa"
SUCCESS  = "#34d399"
ERROR    = "#f87171"
NEUTRAL  = "#94a3b8"
TEXT     = "#e2e8f0"
MUTED    = "#475569"
CURSOR_C = "#f59e0b"

# ──────────────────────────────────────────────────────────────────────────────

def load_scores():
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return []

def save_score(entry: dict):
    scores = load_scores()
    scores.append(entry)
    scores.sort(key=lambda x: x["wpm"], reverse=True)
    with open(SCORE_FILE, "w") as f:
        json.dump(scores, f, indent=2)

# ──────────────────────────────────────────────────────────────────────────────

class TypingTestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("⌨  TypeRacer Pro")
        self.geometry("900x680")
        self.minsize(780, 600)
        self.configure(bg=BG)
        self.resizable(True, True)

        self._setup_fonts()
        self._state_reset()

        self.container = tk.Frame(self, bg=BG)
        self.container.pack(fill="both", expand=True, padx=0, pady=0)

        self.frames = {}
        for Page in (HomePage, TestPage, ResultPage, LeaderboardPage):
            frame = Page(self.container, self)
            self.frames[Page.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.show("HomePage")

    def _setup_fonts(self):
        self.fn_title  = font.Font(family="Courier New", size=26, weight="bold")
        self.fn_mono   = font.Font(family="Courier New", size=16)
        self.fn_input  = font.Font(family="Courier New", size=16)
        self.fn_label  = font.Font(family="Courier New", size=11)
        self.fn_stat   = font.Font(family="Courier New", size=22, weight="bold")
        self.fn_btn    = font.Font(family="Courier New", size=12, weight="bold")
        self.fn_small  = font.Font(family="Courier New", size=10)

    def _state_reset(self):
        self.difficulty  = "Medium"
        self.target_text = ""
        self.start_time  = None
        self.wpm         = 0
        self.accuracy    = 0
        self.errors      = 0

    def show(self, name: str, **kwargs):
        frame = self.frames[name]
        if hasattr(frame, "on_show"):
            frame.on_show(**kwargs)
        frame.tkraise()

# ──────────────────────────────────────────────────────────────────────────────

class HomePage(tk.Frame):
    def __init__(self, parent, app: TypingTestApp):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        # ── title ──
        tk.Label(self, text="⌨  TypeRacer Pro", font=self.app.fn_title,
                 bg=BG, fg=ACCENT2).pack(pady=(60, 4))
        tk.Label(self, text="measure · improve · dominate",
                 font=self.app.fn_label, bg=BG, fg=MUTED).pack(pady=(0, 40))

        # ── difficulty selector ──
        card = tk.Frame(self, bg=SURFACE, padx=36, pady=28)
        card.pack(padx=80, pady=10, fill="x")

        tk.Label(card, text="SELECT DIFFICULTY", font=self.app.fn_label,
                 bg=SURFACE, fg=MUTED).pack(anchor="w", pady=(0, 10))

        btn_row = tk.Frame(card, bg=SURFACE)
        btn_row.pack(fill="x")

        self.diff_var = tk.StringVar(value="Medium")
        self.diff_buttons = {}
        for level, col in [("Easy", SUCCESS), ("Medium", ACCENT2), ("Hard", ERROR)]:
            b = tk.Button(btn_row, text=level, font=self.app.fn_btn,
                          bg=CARD, fg=col, activebackground=col,
                          activeforeground=BG, relief="flat", bd=0,
                          padx=24, pady=10,
                          command=lambda l=level: self._select_diff(l))
            b.pack(side="left", padx=(0, 8))
            self.diff_buttons[level] = b

        self._select_diff("Medium")

        # ── action buttons ──
        tk.Button(self, text="▶  Start Test", font=self.app.fn_btn,
                  bg=ACCENT, fg="white", activebackground=ACCENT2,
                  activeforeground="white", relief="flat", bd=0,
                  padx=40, pady=14, cursor="hand2",
                  command=self._start).pack(pady=(30, 8))

        tk.Button(self, text="🏆  Leaderboard", font=self.app.fn_btn,
                  bg=CARD, fg=ACCENT2, activebackground=SURFACE,
                  activeforeground=ACCENT2, relief="flat", bd=0,
                  padx=40, pady=14, cursor="hand2",
                  command=lambda: self.app.show("LeaderboardPage")).pack(pady=4)

    def _select_diff(self, level: str):
        self.diff_var.set(level)
        self.app.difficulty = level
        colors = {"Easy": SUCCESS, "Medium": ACCENT2, "Hard": ERROR}
        for l, b in self.diff_buttons.items():
            is_sel = (l == level)
            b.configure(bg=colors[l] if is_sel else CARD,
                        fg=BG if is_sel else colors[l],
                        relief="flat")

    def _start(self):
        words = WORD_BANKS[self.app.difficulty]
        self.app.target_text = random.choice(words)
        self.app.show("TestPage")

# ──────────────────────────────────────────────────────────────────────────────

class TestPage(tk.Frame):
    def __init__(self, parent, app: TypingTestApp):
        super().__init__(parent, bg=BG)
        self.app   = app
        self._timer_id = None
        self._build()

    def _build(self):
        # ── top bar ──
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=30, pady=(20, 0))

        tk.Button(top, text="← Back", font=self.app.fn_small,
                  bg=BG, fg=MUTED, activebackground=BG,
                  activeforeground=TEXT, relief="flat", bd=0,
                  cursor="hand2", command=self._go_home).pack(side="left")

        self.diff_lbl = tk.Label(top, text="", font=self.app.fn_small,
                                 bg=BG, fg=ACCENT2)
        self.diff_lbl.pack(side="right")

        # ── stats row ──
        stats = tk.Frame(self, bg=SURFACE)
        stats.pack(fill="x", padx=30, pady=(16, 0), ipady=12)

        self.wpm_var  = tk.StringVar(value="0")
        self.acc_var  = tk.StringVar(value="100%")
        self.time_var = tk.StringVar(value="0s")

        for label, var, col in [("WPM", self.wpm_var, ACCENT2),
                                 ("ACCURACY", self.acc_var, SUCCESS),
                                 ("TIME", self.time_var, CURSOR_C)]:
            cell = tk.Frame(stats, bg=SURFACE)
            cell.pack(side="left", expand=True)
            tk.Label(cell, textvariable=var, font=self.app.fn_stat,
                     bg=SURFACE, fg=col).pack()
            tk.Label(cell, text=label, font=self.app.fn_small,
                     bg=SURFACE, fg=MUTED).pack()

        # ── target text display ──
        txt_card = tk.Frame(self, bg=CARD, padx=20, pady=18)
        txt_card.pack(fill="x", padx=30, pady=(20, 0))

        self.text_canvas = tk.Canvas(txt_card, bg=CARD, bd=0, highlightthickness=0,
                                     height=80)
        self.text_canvas.pack(fill="x")

        # ── input box ──
        inp_frame = tk.Frame(self, bg=SURFACE, padx=16, pady=14)
        inp_frame.pack(fill="x", padx=30, pady=(12, 0))

        self.input_var = tk.StringVar()
        self.input_var.trace_add("write", self._on_type)

        self.entry = tk.Entry(inp_frame, textvariable=self.input_var,
                              font=self.app.fn_input, bg=SURFACE, fg=TEXT,
                              insertbackground=CURSOR_C, relief="flat", bd=0,
                              selectbackground=ACCENT)
        self.entry.pack(fill="x")

        # ── separator ──
        tk.Frame(self, bg=ACCENT, height=2).pack(fill="x", padx=30)

        # ── hint ──
        tk.Label(self, text="Start typing to begin  ·  Backspace to correct",
                 font=self.app.fn_small, bg=BG, fg=MUTED).pack(pady=(10, 0))

        # ── progress bar ──
        self.progress_var = tk.DoubleVar(value=0)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("T.Horizontal.TProgressbar",
                        troughcolor=CARD, background=ACCENT,
                        thickness=6, borderwidth=0)
        self.pb = ttk.Progressbar(self, variable=self.progress_var,
                                  maximum=100, style="T.Horizontal.TProgressbar")
        self.pb.pack(fill="x", padx=30, pady=(12, 0))

        # ── restart button ──
        tk.Button(self, text="↺  New Prompt", font=self.app.fn_btn,
                  bg=CARD, fg=NEUTRAL, activebackground=SURFACE,
                  activeforeground=TEXT, relief="flat", bd=0,
                  padx=20, pady=8, cursor="hand2",
                  command=self._new_prompt).pack(pady=(20, 0))

    # ── lifecycle ──────────────────────────────────────────────────────────────

    def on_show(self, **_):
        self._reset()

    def _reset(self):
        if self._timer_id:
            self.after_cancel(self._timer_id)
            self._timer_id = None

        self.app.start_time = None
        self.elapsed        = 0
        self.input_var.set("")
        self.wpm_var.set("0")
        self.acc_var.set("100%")
        self.time_var.set("0s")
        self.progress_var.set(0)
        self.diff_lbl.configure(text=f"[ {self.app.difficulty} ]")

        self._draw_text("")
        self.entry.focus_set()

    def _new_prompt(self):
        words = WORD_BANKS[self.app.difficulty]
        self.app.target_text = random.choice(words)
        self._reset()

    def _go_home(self):
        if self._timer_id:
            self.after_cancel(self._timer_id)
            self._timer_id = None
        self.app.show("HomePage")

    # ── typing logic ───────────────────────────────────────────────────────────

    def _on_type(self, *_):
        typed  = self.input_var.get()
        target = self.app.target_text

        # start timer on first keystroke
        if typed and self.app.start_time is None:
            self.app.start_time = time.time()
            self._tick()

        self._draw_text(typed)
        self._update_stats(typed)

        # completion check
        if typed == target:
            self._finish(typed)

    def _tick(self):
        if self.app.start_time is None:
            return
        self.elapsed = int(time.time() - self.app.start_time)
        self.time_var.set(f"{self.elapsed}s")
        self._timer_id = self.after(500, self._tick)

    def _update_stats(self, typed: str):
        target = self.app.target_text
        if not typed or self.app.start_time is None:
            return

        elapsed = time.time() - self.app.start_time
        minutes = elapsed / 60 if elapsed > 0 else 1e-9

        words_typed = len(typed.split())
        wpm = int(words_typed / minutes)
        self.wpm_var.set(str(wpm))

        correct = sum(1 for a, b in zip(typed, target) if a == b)
        acc = int(correct / max(len(typed), 1) * 100)
        self.acc_var.set(f"{acc}%")

        progress = len(typed) / max(len(target), 1) * 100
        self.progress_var.set(min(progress, 100))

    # ── text canvas rendering ──────────────────────────────────────────────────

    def _draw_text(self, typed: str):
        c      = self.text_canvas
        target = self.app.target_text
        c.delete("all")

        c.update_idletasks()
        cw = c.winfo_width() or 820

        char_w  = 10   # approx px per Courier char at size 16
        max_col = max(cw // char_w - 2, 20)

        # word-wrap target
        words   = target.split()
        lines   = []
        cur_line = ""
        for w in words:
            test = (cur_line + " " + w).strip()
            if len(test) <= max_col:
                cur_line = test
            else:
                if cur_line:
                    lines.append(cur_line)
                cur_line = w
        if cur_line:
            lines.append(cur_line)

        # map line/col -> flat char index
        flat_idx = 0
        y = 18
        for line in lines:
            x = 14
            for ch in line:
                if flat_idx < len(typed):
                    colour = SUCCESS if typed[flat_idx] == ch else ERROR
                elif flat_idx == len(typed):
                    colour = CURSOR_C  # cursor position highlight
                else:
                    colour = NEUTRAL
                c.create_text(x, y, text=ch, font=self.app.fn_mono,
                              fill=colour, anchor="nw")
                x        += char_w
                flat_idx += 1
            flat_idx += 1  # space
            y        += 28

        c.configure(height=max(y + 4, 60))

    # ── finish ────────────────────────────────────────────────────────────────

    def _finish(self, typed: str):
        if self._timer_id:
            self.after_cancel(self._timer_id)
            self._timer_id = None

        target  = self.app.target_text
        elapsed = time.time() - (self.app.start_time or time.time())
        minutes = elapsed / 60 if elapsed > 0 else 1e-9

        words_typed     = len(typed.split())
        self.app.wpm    = int(words_typed / minutes)

        correct          = sum(1 for a, b in zip(typed, target) if a == b)
        self.app.accuracy = int(correct / max(len(typed), 1) * 100)
        self.app.errors  = sum(1 for a, b in zip(typed, target) if a != b)

        entry = {
            "wpm":        self.app.wpm,
            "accuracy":   self.app.accuracy,
            "errors":     self.app.errors,
            "difficulty": self.app.difficulty,
            "time_sec":   round(elapsed, 1),
            "date":       datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        save_score(entry)
        self.app.show("ResultPage")

# ──────────────────────────────────────────────────────────────────────────────

class ResultPage(tk.Frame):
    def __init__(self, parent, app: TypingTestApp):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        self.inner = tk.Frame(self, bg=BG)
        self.inner.place(relx=0.5, rely=0.5, anchor="center")

    def on_show(self, **_):
        for w in self.inner.winfo_children():
            w.destroy()

        tk.Label(self.inner, text="🎉  Test Complete!", font=self.app.fn_title,
                 bg=BG, fg=ACCENT2).pack(pady=(0, 6))

        diff_colors = {"Easy": SUCCESS, "Medium": ACCENT2, "Hard": ERROR}
        col = diff_colors.get(self.app.difficulty, ACCENT2)
        tk.Label(self.inner, text=f"[ {self.app.difficulty} ]",
                 font=self.app.fn_label, bg=BG, fg=col).pack(pady=(0, 24))

        # ── stat cards ──
        cards_row = tk.Frame(self.inner, bg=BG)
        cards_row.pack(pady=(0, 20))

        stats = [
            ("WPM",      str(self.app.wpm),      ACCENT2),
            ("ACCURACY", f"{self.app.accuracy}%", SUCCESS),
            ("ERRORS",   str(self.app.errors),    ERROR),
        ]
        for label, value, colour in stats:
            card = tk.Frame(cards_row, bg=CARD, padx=28, pady=18)
            card.pack(side="left", padx=8)
            tk.Label(card, text=value, font=self.app.fn_stat,
                     bg=CARD, fg=colour).pack()
            tk.Label(card, text=label, font=self.app.fn_small,
                     bg=CARD, fg=MUTED).pack()

        # ── rating message ──
        wpm = self.app.wpm
        if wpm >= 80:
            msg, mc = "🚀  Blazing fast!", ACCENT2
        elif wpm >= 60:
            msg, mc = "⚡  Great speed!", SUCCESS
        elif wpm >= 40:
            msg, mc = "👍  Good effort!", CURSOR_C
        else:
            msg, mc = "🐢  Keep practising!", ERROR
        tk.Label(self.inner, text=msg, font=self.app.fn_btn,
                 bg=BG, fg=mc).pack(pady=(0, 24))

        # ── buttons ──
        tk.Button(self.inner, text="▶  Try Again", font=self.app.fn_btn,
                  bg=ACCENT, fg="white", activebackground=ACCENT2,
                  activeforeground="white", relief="flat", bd=0,
                  padx=36, pady=12, cursor="hand2",
                  command=self._retry).pack(pady=4)

        tk.Button(self.inner, text="🏆  Leaderboard", font=self.app.fn_btn,
                  bg=CARD, fg=ACCENT2, activebackground=SURFACE,
                  activeforeground=ACCENT2, relief="flat", bd=0,
                  padx=36, pady=12, cursor="hand2",
                  command=lambda: self.app.show("LeaderboardPage")).pack(pady=4)

        tk.Button(self.inner, text="⌂  Home", font=self.app.fn_btn,
                  bg=CARD, fg=NEUTRAL, activebackground=SURFACE,
                  activeforeground=TEXT, relief="flat", bd=0,
                  padx=36, pady=12, cursor="hand2",
                  command=lambda: self.app.show("HomePage")).pack(pady=4)

    def _retry(self):
        words = WORD_BANKS[self.app.difficulty]
        self.app.target_text = random.choice(words)
        self.app.show("TestPage")

# ──────────────────────────────────────────────────────────────────────────────

class LeaderboardPage(tk.Frame):
    def __init__(self, parent, app: TypingTestApp):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=30, pady=(20, 0))

        tk.Button(top, text="← Back", font=self.app.fn_small,
                  bg=BG, fg=MUTED, activebackground=BG,
                  activeforeground=TEXT, relief="flat", bd=0,
                  cursor="hand2",
                  command=lambda: self.app.show("HomePage")).pack(side="left")

        tk.Label(self, text="🏆  Leaderboard", font=self.app.fn_title,
                 bg=BG, fg=ACCENT2).pack(pady=(10, 4))
        tk.Label(self, text="Top 10 scores (sorted by WPM)",
                 font=self.app.fn_label, bg=BG, fg=MUTED).pack(pady=(0, 16))

        # ── table frame ──
        table_outer = tk.Frame(self, bg=SURFACE)
        table_outer.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        headers = ["#", "WPM", "ACCURACY", "ERRORS", "DIFFICULTY", "DATE"]
        widths  = [4,   8,     10,         8,        12,            18]
        cols    = [MUTED, ACCENT2, SUCCESS, ERROR, ACCENT2, NEUTRAL]

        # header row
        h_row = tk.Frame(table_outer, bg=CARD)
        h_row.pack(fill="x", padx=0, pady=(0, 2))
        for h, w in zip(headers, widths):
            tk.Label(h_row, text=h, font=self.app.fn_small,
                     bg=CARD, fg=MUTED,
                     width=w, anchor="center").pack(side="left", padx=2, pady=6)

        # scrollable body
        canvas  = tk.Canvas(table_outer, bg=SURFACE, bd=0, highlightthickness=0)
        scrollbar = tk.Scrollbar(table_outer, orient="vertical",
                                 command=canvas.yview)
        self.body = tk.Frame(canvas, bg=SURFACE)

        self.body.bind("<Configure>",
                       lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.body, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # clear button
        tk.Button(self, text="🗑  Clear Scores", font=self.app.fn_small,
                  bg=CARD, fg=ERROR, activebackground=SURFACE,
                  activeforeground=ERROR, relief="flat", bd=0,
                  padx=14, pady=6, cursor="hand2",
                  command=self._clear).pack(pady=(0, 12))

        self._widths = widths
        self._cols   = cols

    def on_show(self, **_):
        for w in self.body.winfo_children():
            w.destroy()

        scores = load_scores()[:10]
        diff_colors = {"Easy": SUCCESS, "Medium": ACCENT2, "Hard": ERROR}
        medals = {0: "🥇", 1: "🥈", 2: "🥉"}

        if not scores:
            tk.Label(self.body, text="No scores yet — play a game!",
                     font=self.app.fn_label, bg=SURFACE, fg=MUTED).pack(pady=30)
            return

        for i, s in enumerate(scores):
            row_bg = CARD if i % 2 == 0 else SURFACE
            row = tk.Frame(self.body, bg=row_bg)
            row.pack(fill="x", padx=0, pady=1)

            rank_txt = medals.get(i, str(i + 1))
            values = [
                rank_txt,
                str(s.get("wpm", "-")),
                f"{s.get('accuracy', '-')}%",
                str(s.get("errors", "-")),
                s.get("difficulty", "-"),
                s.get("date", "-"),
            ]
            for val, w, c in zip(values, self._widths, self._cols):
                dc = diff_colors.get(val, c) if val in diff_colors else c
                tk.Label(row, text=val, font=self.app.fn_small,
                         bg=row_bg, fg=dc,
                         width=w, anchor="center").pack(side="left", padx=2, pady=5)

    def _clear(self):
        if os.path.exists(SCORE_FILE):
            os.remove(SCORE_FILE)
        self.on_show()

# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = TypingTestApp()
    app.mainloop()