import sqlite3
from tkinter import messagebox

class DatabaseProxy:
    def __init__(self):
        # З'єднання з базою даних
        self.connection = sqlite3.connect("user_database.db")
        self.cursor = self.connection.cursor()

    def get_users(self):
        self.cursor.execute('SELECT * FROM users')
        data = self.cursor.fetchall()

        return data

    def get_user(self, id):
        self.cursor.execute(f'SELECT * FROM users WHERE id = {id}')
        data = self.cursor.fetchall()

        return data

    def edit_user(self, id, name, lastname, age, email):
        if name and age and lastname and email:
            try:
                age = int(age)
                user_to_update = (name, lastname, age, email, id)
                self.cursor.execute(
                    "UPDATE users SET ім_я=?, прізвище=?, вік=?, email=? WHERE id=?",
                    user_to_update
                )
                self.connection.commit()

                messagebox.showinfo("Успіх", "Інформація оновлена.")
            except ValueError:
                messagebox.showerror("Помилка", "Будь ласка, введіть правильне значення")
        else:
            messagebox.showwarning("Попередження", "Будь ласка, заповніть всі поля.")

    def add_user(self, name, lastname, age, email):
        if name and age and lastname and email:
            try:
                age = int(age)
                user_to_insert = (name, lastname, age, email)
                self.cursor.execute("INSERT INTO users(ім_я, прізвище, вік, email) VALUES(?,?,?,?)", user_to_insert)
                self.connection.commit()

                messagebox.showinfo("Успіх", "Користувач доданий до бази даних.")
            except ValueError:
                messagebox.showerror("Помилка", "Будь ласка, введіть правильне значення")
        else:
            messagebox.showwarning("Попередження", "Будь ласка, заповніть всі поля.")

    def delete_user(self, id):
        self.cursor.execute('DELETE FROM users WHERE id=' + str(id))
        self.connection.commit()