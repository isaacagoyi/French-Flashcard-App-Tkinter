from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}
try:
    word_data = pd.read_csv("data/french_words_to_learn.csv")
except FileNotFoundError:
    original_words = pd.read_csv("data/french_words.csv")
    to_learn = original_words.to_dict(orient="records")
else:
    to_learn = word_data.to_dict(orient="records")
random_dict = None


def next_card():
    global flip_timer
    global random_dict
    window.after_cancel(flip_timer)
    random_dict = random.choice(to_learn)
    random_word = random_dict["French"]
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_text, text=random_word, fill="black")

    flip_timer= window.after(3000, flip_card)

def flip_card():
    canvas.itemconfig(card_image, image=card_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_text, text=random_dict["English"], fill="white")

def update_flashcard():
    to_learn.remove(random_dict)
    to_learn_dataframe = pd.DataFrame(to_learn)
    to_learn_dataframe.to_csv("data/french_words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flash Card")
window.config(pady=50, padx=50, bg = BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")

card_image = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 24, "bold"))
card_text = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg = BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row = 0, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image = cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
check_button = Button(image=check_image, highlightthickness=0, command=update_flashcard)
check_button.grid(row=1, column=1)

flip_timer = window.after(3000, flip_card)
next_card()

window.mainloop()
