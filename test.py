"""python modules for user interface"""
from tkinter import Tk, Label, Entry, INSERT, Text


class Ui():
    """Class for initializing User Interface"""
    def __init__(self, text) -> None:
        background = "#252526"
        self.text = text
        self.window = Tk()
        self.window.title = "Touch Typing Test"
        self.window.geometry("700x600")
        self.window.config(bg=background, padx=20, pady=20)

        

        # text widget for displaying text because we can configure different color
        # for different text
        self.display_text = Text(
            self.window,
            width=82,
            height=10,
            font=("Ariel", 14)
        )

        self.display_text.grid(column=0, row=1, columnspan=2)

        self.display_text.insert(INSERT, self.text,)
        self.display_text.config(state="disabled")

        self.input_label = Entry(
            self.window,
            font=('Arial', 14),)
        self.entry = Entry(self.window, font=('Arial', 14))
        self.input_label.config(
            justify="center",
        )
        self.input_label.grid(column=0, row=2, columnspan=2)
        self.input_label.focus()

        self.check_input()

        self.window.mainloop()


    def check_input(self):
        """It check input after 1ms"""
        user_char_list = list(self.input_label.get())
        char_list = list(self.text)

        num_of_char_on_line = 81
        num_of_lines = int(len(char_list) / num_of_char_on_line)
        char_count = 0

        for index in enumerate(char_list):
            char_on_line = 0
            index = index[0]

            if char_count > num_of_char_on_line:
                char_count = 0

            for i in range(1, num_of_lines + 1):
                if index > num_of_char_on_line * (i -1) and index <= num_of_char_on_line * i:
                    char_on_line = i

            try:
                if user_char_list[index] == char_list[index]:
                    self.display_text.tag_remove("wrong", f"{char_on_line}.{char_count}")
                    self.display_text.tag_config("correct", foreground="green")
                    self.display_text.tag_add("correct", f"{char_on_line}.{char_count}")
                    self.display_text.tag_remove("default", f"{char_on_line}.{char_count}")
                    print(f"{char_on_line}.{char_count}")
                elif user_char_list[index] != char_list[index]:
                    self.display_text.tag_remove("correct", f"{char_on_line}.{char_count}")
                    self.display_text.tag_remove("default", f"{char_on_line}.{char_count}")
                    self.display_text.tag_config("wrong", foreground="red")
                    self.display_text.tag_add("wrong", f"{char_on_line}.{char_count}")

            except IndexError:
                self.display_text.tag_remove("correct", f"{char_on_line}.{char_count}")
                self.display_text.tag_remove("wrong", f"{char_on_line}.{index}")

                self.display_text.tag_config("default", foreground="black")
                self.display_text.tag_add("default", f"{char_on_line}.{char_count}")

            char_count += 1

        self.window.after(1, self.check_input)
        