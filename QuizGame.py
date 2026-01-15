import tkinter as tk
from tkinter import messagebox
import json
import random

TIME_LIMIT = 10  # seconds per question


class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        self.root.geometry("500x400")

        self.score = 0
        self.q_index = 0
        self.timer = TIME_LIMIT

        self.load_questions()
        self.create_category_screen()

    def load_questions(self):
        with open("questions.json", "r") as file:
            self.data = json.load(file)

    def create_category_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Select Quiz Category", font=("Arial", 16)).pack(pady=20)

        for category in self.data.keys():
            tk.Button(
                self.root,
                text=category,
                width=20,
                command=lambda c=category: self.start_quiz(c)
            ).pack(pady=5)

    def start_quiz(self, category):
        self.questions = random.sample(self.data[category], len(self.data[category]))
        self.score = 0
        self.q_index = 0
        self.show_question()

    def show_question(self):
        self.clear_screen()
        self.timer = TIME_LIMIT

        self.timer_label = tk.Label(self.root, text=f"Time Left: {self.timer}", font=("Arial", 12))
        self.timer_label.pack(pady=5)

        question_data = self.questions[self.q_index]
        tk.Label(self.root, text=question_data["question"], wraplength=450, font=("Arial", 14)).pack(pady=20)

        self.selected = tk.StringVar()

        for option in question_data["options"]:
            tk.Radiobutton(
                self.root,
                text=option,
                variable=self.selected,
                value=option
            ).pack(anchor="w", padx=50)

        tk.Button(self.root, text="Submit", command=self.check_answer).pack(pady=20)

        self.update_timer()

    def update_timer(self):
        if self.timer > 0:
            self.timer_label.config(text=f"Time Left: {self.timer}")
            self.timer -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.next_question()

    def check_answer(self):
        correct_answer = self.questions[self.q_index]["answer"]
        if self.selected.get() == correct_answer:
            self.score += 1
            messagebox.showinfo("Correct", "Correct Answer!")
        else:
            messagebox.showerror("Wrong", f"Correct Answer: {correct_answer}")
        self.next_question()

    def next_question(self):
        self.q_index += 1
        if self.q_index < len(self.questions):
            self.show_question()
        else:
            self.show_result()

    def show_result(self):
        self.clear_screen()
        tk.Label(self.root, text="Quiz Completed!", font=("Arial", 16)).pack(pady=20)
        tk.Label(self.root, text=f"Your Score: {self.score}", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="Restart", command=self.create_category_screen).pack(pady=20)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    QuizGame(root)
    root.mainloop()