import time
import sys
import tkinter as tk
import random
import threading
import re
import pickle
from os.path import exists


class Help:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Typing help")
        self.root.geometry("700x140")
        self.root.configure(bg='#050A1A')
        self.root.resizable(width=False, height=False)
        self.help_text = tk.Label(self.root, text=open("Help_text.txt", "r").read(), fg="white", bg="#050A1A")
        self.help_text.pack()
        self.quit_button = tk.Button(self.root, text="Understood", fg="white", bg="#050A1A", command=self.root.destroy, font=("Arial", 20))
        self.quit_button.pack()
        self.root.mainloop()


class Window:

    def NewText(self):
        self.current_text = random.choice(self.texts_variants)
        self.TextLabel.config(text=self.current_text)

    def StartProgramm(self, event):
        if not self.is_active:
            self.is_active = True
            prg = threading.Thread(target=self.Timer)
            prg.daemon = True
            prg.start()

    def Timer(self):
        self.time_passed = 0
        while self.is_active:
            time.sleep(0.1)
            self.time_passed += 0.1

            self.TimePassedStat.config(text=f"{self.time_passed:.0f} s")
            CPM = 60 * (self.char_count / self.time_passed)
            self.CPMstat.config(text=f"CPM: {CPM:.0f}")

    def is_valid(self, newval):
        if (len(newval) == len(self.current_text) and newval[-1] == self.current_text[self.current_character_index]):
            self.current_character_index = 0
            self.UserInputSace.delete(0, len(self.current_text))
            self.NewText()
            self.word_counter += 1
            if not self.time_passed == 0:
                self.words_per_minute = 60 * (self.word_counter / self.time_passed)
            else:
                self.words_per_minute = 0
            self.UserInputSace.after_idle(lambda: self.UserInputSace.configure(validate="all"))
            self.WPMstat.config(text=f"{self.words_per_minute:.0f} WPM")
            return True
        if (len(newval) != 0 and newval[-1] == self.current_text[self.current_character_index]):
            if newval[-1] == " ":
                self.word_counter += 1
                if not self.time_passed == 0:
                    self.words_per_minute = 60 * (self.word_counter / self.time_passed)
                else:
                    self.words_per_minute = 0
                self.WPMstat.config(text=f"{self.words_per_minute:.0f} WPM")
            self.current_character_index += 1
            self.char_count += 1
            return True
        else:
            self.error_count += 1
            pickle.dump(self.error_count, open("error_log.dat", "wb"))
            self.ErrorsStat.config(text=f"{self.error_count} errors")
            return False

    def OpenHelp(self):
        Help()

    def ClearText(self):
        self.UserInputSace.delete(0, len(self.UserInputSace.get()))

    def Reset(self):

        self.is_active = False
        self.error_count = 0
        pickle.dump(self.error_count, open("error_log.dat", "wb"))
        self.ErrorsStat.config(text=f"{self.error_count} errors")
        self.time_passed = 0.1
        self.current_character_index = len(self.current_text) - 1
        self.UserInputSace.destroy()
        self.UserInputSace = tk.Entry(self.root, width=80, bg='white', validate="key", validatecommand=self.check)
        self.UserInputSace.place(anchor="n", x=300, y=150)
        self.current_character_index = 0
        self.word_counter = 0
        self.WPMstat.config(text="0 WPM")
        self.NewText()
        self.char_count = 0

    def __init__(self):
        self.root = tk.Tk()
        self.time_passed = 0
        self.current_character_index = 0
        self.word_counter = 0
        if not exists("error_log.dat"):
            pickle.dump(0, open("error_log.dat"), "wb")
        self.char_count = 0
        self.error_count = pickle.load(open("error_log.dat", "rb"))
        self.texts_variants = open("texts.txt", "r").read().split('\n')
        self.is_active = False
        self.root.title("Typing simulator")
        self.root.geometry("600x400")
        self.root.configure(bg='#050A1A')
        self.current_text = "Press new text"
        self.root.resizable(width=False, height=False)
        self.the_above_space = tk.Label(self.root, height=7, text="", bg='#050A1A')
        self.the_above_space.place(anchor="n", x=300, y=50)
        # Widgets:
        self.TextLabel = tk.Label(self.root, text=self.current_text, bg='#050A1A', font=("Arial", 15), fg="white")
        self.TextLabel.place(anchor="n", x=300, y=100)
        self.check = (self.root.register(self.is_valid), "%P")
        self.g = tk.Entry
        self.UserInputSace = tk.Entry(self.root, width=80, bg='white', validate="key", validatecommand=self.check)
        self.UserInputSace.bind("<KeyPress>", self.StartProgramm)
        self.UserInputSace.place(anchor="n", x=300, y=150)
        self.CPMstat = tk.Label(self.root, text=("CPM:", 0), bg='#050A1A', fg="white", font=("Arial", 10))
        self.CPMstat.place(anchor="n", x=300, y=400)
        self.TimePassedStat = tk.Label(self.root, text=(0, "s"), bg='#050A1A', fg="white", font=("Arial", 10))
        self.TimePassedStat.place(anchor="n", x=300, y=225)
        self.ErrorsStat = tk.Label(self.root, text=f"{self.error_count} errors", bg='#050A1A', fg="white", font=("Arial", 10))
        self.ErrorsStat.place(anchor="n", x=300, y=250)
        self.words_per_minute = 0
        self.WPMstat = tk.Label(self.root, text=f"{self.words_per_minute:.0f} WPM", bg='#050A1A', fg="white", font=("Arial", 10))
        self.WPMstat.place(anchor="n", x=300, y=275)
        self.ResetErrorButton = tk.Button(self.root, text="Reset", bg='#050A1A', fg="white", font=("Arial", 15), command=self.Reset)
        self.ResetErrorButton.place(anchor="n", x=300, y=180)
        self.HelpButton = tk.Button(self.root, text="Help", bg='#050A1A', fg="white", font=("Arial", 10), command=self.OpenHelp)
        self.HelpButton.place(anchor="n", x=300, y=300)
        self.root.mainloop()



Window()

