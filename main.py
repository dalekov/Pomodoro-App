from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15
reps = 0
timer = None
# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    """Resets the timer back to 00:00, removes checkmarks, changes title label to default 'Timer'.
    Reset the reps counter back to 0."""
    global reps
    reps = 0
    root.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label["text"] = "Timer"
    checkmark_label["text"] = ""
# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    """Starts the timer for work, short break, or long break based on the current rep count."""
    global reps
    reps += 1

    # Converting minutes to seconds
    work_seconds = int(WORK_MIN * 60)
    short_break_seconds = int(SHORT_BREAK_MIN * 60)
    long_break_seconds = int(LONG_BREAK_MIN * 60)

    # We check the intervals. Every 8th interval is a long break, every 2nd (every even) is a short break.
    # All others are work intervals.
    if reps % 8 == 0:
        count_down(long_break_seconds)
        title_label.config(text="Long Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_seconds)
        title_label.config(text="Short Break", fg=PINK)
    else:
        count_down(work_seconds)
        title_label.config(text="Work", fg=GREEN)
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    """Handles the countdown mechanism and updates the timer text each second."""
    minutes = count // 60
    seconds = count % 60

    # If seconds is one-digit, there needs to be a leading zero.
    if seconds < 10:
        seconds = f"0{seconds}" # Dynamic Typing. -> unique to Python.

    canvas.itemconfig(timer_text, text=f"{minutes}:{seconds}")
    # As long as the time is larger than 0:
    if count > 0:
        global timer
        timer = root.after(1000, count_down, count - 1) # After 1000ms (1s), the count is decreased by 1.
    else: # When count is less than 0, the interval ends.
        # We check if we're after a break interval so we add a checkmark.
        if reps % 2 == 0:
            output = ["✔" for _ in range(int(reps/2))]
            checkmark_label.config(text=''.join(output))

        start_timer()
# ---------------------------- UI SETUP ----------------------------------------- #
# Creating the main root -> Giving it the appropriate background color, size and title.
root = Tk()
root.title("Pomodoro App")
root.config(bg=YELLOW, padx=100, pady=50)

# Creating a canvas so we can add an image and text on top of it.
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_image = PhotoImage(file="tomato.png") # Creating the image using PhotoImage(file=)
canvas.create_image(100, 112, image=tomato_image)
timer_text = canvas.create_text(100, 130, text="25:00", font=(FONT_NAME, 35, "bold"), fill="white")
canvas.grid(column=1, row=1)

# Create the 'Timer' label.
title_label = Label(text="Work", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)

# Create 'Start' button.
start_button = Button(text="Start", highlightbackground=YELLOW, command=start_timer)
start_button.grid(column=0, row=3)

# Create 'Reset' button.
reset_button = Button(text="Reset", highlightbackground=YELLOW, command=reset_timer)
reset_button.grid(column=2, row=3)

# Create checkmark.
checkmark_label = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
checkmark_label.grid(column=1, row=4)


# Run the application.
root.mainloop()
