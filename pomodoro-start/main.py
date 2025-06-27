from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
BG_COLOR = "#f0f0f0"
ACCENT = "#6C63FF"
WORK_COLOR = "#4CAF50"
BREAK_COLOR = "#2196F3"
LONG_BREAK_COLOR = "#f44336"
TEXT_COLOR = "#333333"
FONT_NAME = "Segoe UI"
WORK_MIN = 35
SHORT_BREAK_MIN = 8
LONG_BREAK_MIN = 25
laps = 0
timerr = None
paused = False
remaining_time = 0


def check_mark():
    check_label.config(text="✓" * (laps // 2))


def timer_reset():
    global laps, timerr, paused, remaining_time
    if timerr:
        view.after_cancel(timerr)
    label_timer.config(text="TIMER", fg=TEXT_COLOR)
    canvas.itemconfig(timer_text, text="00:00")
    laps = 0
    paused = False
    remaining_time = 0
    button_start_pause.config(text="Start", state=NORMAL)
    button_next.config(state=DISABLED)
    check_label.config(text="")


def press_start_pause():
    global paused
    if button_start_pause["text"] == "Start":
        button_start_pause.config(text="Pause")
        button_next.config(state=NORMAL)
        if paused:
            count_down(remaining_time)
            paused = False
        else:
            start_session()
    else:
        pause_timer()


def pause_timer():
    global timerr, remaining_time, paused
    if timerr:
        view.after_cancel(timerr)
        timerr = None
        paused = True
        button_start_pause.config(text="Start")


def start_session():
    global laps
    laps += 1

    if laps % 8 == 0:
        label_timer.config(text="LONG BREAK", fg=LONG_BREAK_COLOR)
        count_down(LONG_BREAK_MIN * 60)
    elif laps % 2 == 0:
        label_timer.config(text="SHORT BREAK", fg=BREAK_COLOR)
        count_down(SHORT_BREAK_MIN * 60)
    else:
        label_timer.config(text="WORK", fg=WORK_COLOR)
        count_down(WORK_MIN * 60)


def count_down(count):
    global timerr, remaining_time
    remaining_time = count

    mins = math.floor(count / 60)
    secs = count % 60
    time_str = f"{mins:02d}:{secs:02d}"
    canvas.itemconfig(timer_text, text=time_str)

    if count > 0:
        timerr = view.after(1000, count_down, count - 1)
    else:
        button_start_pause.config(text="Start")
        button_next.config(state=DISABLED)
        start_session()
        if laps % 2 == 0:
            check_mark()


def skip_next():
    global timerr, paused
    if timerr:
        view.after_cancel(timerr)
    paused = False
    button_start_pause.config(text="Pause")
    start_session()


# ---------------------------- UI SETUP ------------------------------- #
view = Tk()
view.title("Pomodoro Timer")
view.config(padx=40, pady=30, bg=BG_COLOR)

# TITLE
title_label = Label(text="🍅 Pomodoro Timer", font=(FONT_NAME, 24, "bold"), fg=ACCENT, bg=BG_COLOR)
title_label.grid(row=0, column=1, pady=(0, 10))

# TIMER LABEL
label_timer = Label(text="TIMER", font=(FONT_NAME, 36, "bold"), fg=TEXT_COLOR, bg=BG_COLOR)
label_timer.grid(row=1, column=1)

# CANVAS WITH TIMER
canvas = Canvas(width=260, height=260, bg=BG_COLOR, highlightthickness=0)
try:
    tomato_img = PhotoImage(file="tomato.png")
    canvas.create_image(130, 130, image=tomato_img)
except Exception:
    canvas.create_oval(30, 30, 230, 230, fill=ACCENT, outline="")
timer_text = canvas.create_text(130, 140, text="00:00", fill="white", font=(FONT_NAME, 32, "bold"))
canvas.grid(row=2, column=1)

# BUTTON STYLES
BUTTON_STYLE = {
    "font": (FONT_NAME, 12, "bold"),
    "fg": "white",
    "relief": FLAT,
    "padx": 14,
    "pady": 8,
    "bd": 0,
    "cursor": "hand2"
}

# START/PAUSE BUTTON
button_start_pause = Button(
    text="Start", bg=WORK_COLOR, command=press_start_pause, **BUTTON_STYLE
)
button_start_pause.grid(row=3, column=0, pady=25, padx=5)

# NEXT BUTTON
button_next = Button(
    text="Next", bg=BREAK_COLOR, command=skip_next, state=DISABLED, **BUTTON_STYLE
)
button_next.grid(row=3, column=1, pady=25, padx=5)

# RESET BUTTON
button_reset = Button(
    text="Reset", bg=LONG_BREAK_COLOR, command=timer_reset, **BUTTON_STYLE
)
button_reset.grid(row=3, column=2, pady=25, padx=5)

# CHECKMARK
check_label = Label(font=(FONT_NAME, 16), fg=ACCENT, bg=BG_COLOR)
check_label.grid(row=4, column=1)

view.mainloop()
