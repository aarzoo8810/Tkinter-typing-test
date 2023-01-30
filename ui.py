"""python modules for user interface"""
from tkinter import Tk, Label, Entry, INSERT, Text, Button
import random

seconds = 60
time_limit = 0

class Ui():
    # pylint: disable=too-many-instance-attributes
    # this is reasonable amount. I think .....

    """This class initializes user interface"""
    def __init__(self, text) -> None:
        self.background_color = "#252526"
        self.text_color = "white"
        self.char_limit = 81
        self.text_list = text
        self.random_paragraph = random.choice(self.text_list).replace("\n", "").strip()
        self.text = self.random_paragraph
        # self.text1 = text # this variable doesn't get modified so we can store it in self.text after users restarts it
        self.wrong_char_list = []
        self.last_word_index = 0
        self.check_input_after_func = None
        self.window = None
        self.window_name = "Tk Typing Speed"

        # it stores uncorrected letters with that word's index
        # so when users try to correct their mistakes it can be deleted easily
        self.uncorrected_letter = {}
        self.uncorrected_words = {}


        self.home()


    def home(self):
        """It is start window"""
        self.start_window = Tk()
        self.start_window.title(self.window_name)
        self.start_window.geometry("500x400")
        self.start_window.config(bg=self.background_color)

        self.start_button = Button(self.start_window, text="Start", command=self.type_window)
        self.start_button.place(x=220, y=170)

        self.start_window.mainloop()


    def type_window(self):
        """it is main window where you type"""
        try:
            self.start_window.destroy()
        except:
            if self.window is not None:
                self.window.destroy()


        self.window = Tk()
        self.window.title(self.window_name)
        self.window.geometry("850x600")
        self.window.config(bg=self.background_color)

        self.timer_label = Label(
            self.window,
            text="Time: 1:00",
            background=self.background_color,
            fg=self.text_color,
            font=("Arial", 14)
            )
        self.timer_label.grid(column=1, row=0)

        self.display_text = Text(
            self.window,
            width=82,
            height=10,
            font=("Arial", 14)
        )
        self.display_text.grid(column=0, row=1, columnspan=2, padx=10, pady=10)

        self.input_label = Entry(
            self.window,
            font=('Ariel', 14)
        )
        self.input_label.grid(column=0, row=2, columnspan=2)
        self.input_label.xview_moveto(1)

        self.input_label.focus()

        self.insert_text()
        self.timer(seconds)
        self.check_input()
        self.window.mainloop()


    def insert_text(self):
        """This function inserts text into Text widget"""

        # this doesn't work as intended. Line gets shorter and shorter after each line.
        if len(self.text) > 80:
            for i in range(81, 0, -1):
                try:
                    if self.text[i] == " ":
                        split_text = self.text[:i]
                        self.display_text.insert(INSERT, split_text)
                        self.display_text.insert(INSERT, "\n")
                        self.text = self.text[i:]
                except IndexError:
                    self.display_text.insert(INSERT, self.text)
                    break
            self.display_text.config(state="disabled")


    def check_input(self):
        """it checks user input against given text and how much error there is"""
        user_input = self.input_label.get().strip().split(" ")
        given_text = self.random_paragraph.split(" ")

        last_word_index = self.last_word_index
        if last_word_index > len(user_input) -1:
            self.last_word_index -= 1
            last_word_index = self.last_word_index

        user_last_word = user_input[last_word_index]
        given_last_word = given_text[last_word_index]

        # print(f"{user_input = }")
        if len(user_input) - 1 > last_word_index or len(user_last_word) > len(given_last_word):
            if given_last_word != user_last_word:
                self.uncorrected_words[last_word_index] = given_last_word
                uncorrected_letters_list = []
                for index, given_word_char in enumerate(given_last_word):
                    try:
                        user_word_char = user_last_word[index]
                    except IndexError:
                        pass
                    else:
                        if given_word_char != user_word_char:
                            uncorrected_letters_list.append(user_word_char)

                self.uncorrected_letter[last_word_index] = uncorrected_letters_list
            self.last_word_index += 1


        else:
            try:
                self.uncorrected_letter.pop(last_word_index)
            except KeyError:
                pass


        # print(f"{self.uncorrected_letter = }")

        self.check_input_after_func = self.window.after(1, self.check_input)

        # print(self.wrong_char_list)


    def timer(self, time):
        """call check_input function after and counts time till 1 minute is passed"""
        # self.start_button.grid_forget()
        time_seconds = time - 1

        if time_seconds < 10:
            time_seconds = f"0{str(time_seconds)}"

        self.timer_label.config(text=f"{time_limit}:{time_seconds}")

        if time_seconds == "00":
            self.check_input()
            self.input_label.config(state="disabled")
            # self.start_button.grid()
            # if self.check_input_after_func is not None:
            self.window.after_cancel(self.check_input_after_func)
            self.typing_speed()
        else:
            self.window.after(1000, self.timer, int(time_seconds))


    def typing_speed(self):
        """Calculates typing speed"""
        for value in self.uncorrected_letter.values():
            self.wrong_char_list += value

        gross_wpm = len(self.input_label.get()) / 5
        # total_uncorrected_char = len(self.wrong_char_list)/5
        total_uncorrected_char = len(self.uncorrected_words)
        print(self.uncorrected_words)

        net_wpm = round(gross_wpm - total_uncorrected_char)

        result_label = Label(self.window, text=f"Result: {net_wpm} WPM", font=("Sans", 16))
        result_label.grid(column=0, row=3, columnspan=2, pady=10)

        self.text = random.choice(self.text_list).replace("\n", "").strip()
        retry_btn = Button(self.window, text="Restart", command=self.type_window)
        retry_btn.grid(column=1, row=3, columnspan=2)
