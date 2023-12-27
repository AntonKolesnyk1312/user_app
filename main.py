import sqlite3
import tkinter as tk
from tkinter import messagebox


class UserDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Database App")
        self.root.geometry('400x300')

        # З'єднання з базою даних
        self.connection = sqlite3.connect("user_database.db")
        self.cursor = self.connection.cursor()

        # Інтерфейс
        self.label_name = tk.Label(root, text="Ім'я:")
        self.label_name.grid(row=0, column=0, padx=10, pady=5)
        self.entry_name = tk.Entry(root)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)

        self.label_lastname = tk.Label(root, text="Прізвище:")
        self.label_lastname.grid(row=1, column=0, padx=10, pady=5)
        self.entry_lastname = tk.Entry(root)
        self.entry_lastname.grid(row=1, column=1, padx=10, pady=5)

        self.label_age = tk.Label(root, text="Вік:")
        self.label_age.grid(row=2, column=0, padx=10, pady=5)
        self.entry_age = tk.Entry(root)
        self.entry_age.grid(row=2, column=1, padx=10, pady=5)

        self.label_email = tk.Label(root, text="Email:")
        self.label_email.grid(row=3, column=0, padx=10, pady=5)
        self.entry_email = tk.Entry(root)
        self.entry_email.grid(row=3, column=1, padx=10, pady=5)

        self.button_add = tk.Button(root, text="Додати", command=self.add_user)
        self.button_add.grid(row=4, column=0, columnspan=2, pady=5)

        self.button_view = tk.Button(root, text="Переглянути користувачів", command=self.view_users)
        self.button_view.grid(row=5, column=0, columnspan=2, pady=5)

    def add_user(self):
        name = self.entry_name.get()
        lastname = self.entry_lastname.get()
        age = self.entry_age.get()
        email = self.entry_email.get()

        if name and age and lastname and email:
            try:
                age = int(age)
                # код на вставлення
                user_to_insert = (name, lastname, age, email)
                self.cursor.execute("INSERT INTO users(ім_я, прізвище, вік, email) VALUES(?,?,?,?)", user_to_insert)
                self.connection.commit()

                messagebox.showinfo("Успіх", "Користувач доданий до бази даних.")
            except ValueError:
                messagebox.showerror("Помилка", "Будь ласка, введіть правильне значення")
        else:
            messagebox.showwarning("Попередження", "Будь ласка, заповніть всі поля.")

    def view_users(self):
        self.cursor.execute('SELECT * FROM users')
        data = self.cursor.fetchall()

        if data:
            top = tk.Toplevel(self.root)
            top.title("Список користувачів")

            def delete_row(row_index, id):
                # видалення рядка з інтерфейсу
                for widget in top.grid_slaves(row=row_index):
                    widget.grid_remove()

                # видалення рядка із БД
                test = 'DELETE FROM users WHERE id=' + str(id)
                self.cursor.execute(test)
                self.connection.commit()

            def edit(id):
                def edit_user():
                    nonlocal id
                    name = entry_name.get()
                    lastname = entry_lastname.get()
                    age = entry_age.get()
                    email = entry_email.get()

                    if name and age and lastname and email:
                        try:
                            age = int(age)
                            # код на вставлення
                            user_to_insert = (name, lastname, age, email, id)
                            self.cursor.execute(
                                "UPDATE users SET ім_я=?, прізвище=?, вік=?, email=? WHERE id=?",
                                user_to_insert
                            )
                            self.connection.commit()

                            messagebox.showinfo("Успіх", "Інформація оновлена.")
                        except ValueError:
                            messagebox.showerror("Помилка", "Будь ласка, введіть правильне значення")
                    else:
                        messagebox.showwarning("Попередження", "Будь ласка, заповніть всі поля.")

                self.cursor.execute('SELECT * FROM users WHERE id=' + str(id))
                data = self.cursor.fetchall()
                data = data[0]

                edit_window = tk.Toplevel(self.root)
                edit_window.title("Редагування користувача")

                label_name = tk.Label(edit_window, text="Ім'я:")
                label_name.grid(row=0, column=0, padx=10, pady=5)
                entry_name = tk.Entry(edit_window)
                entry_name.insert(0, data[1])
                entry_name.grid(row=0, column=1, padx=10, pady=5)

                label_lastname = tk.Label(edit_window, text="Прізвище:")
                label_lastname.grid(row=1, column=0, padx=10, pady=5)
                entry_lastname = tk.Entry(edit_window)
                entry_lastname.insert(0, data[2])
                entry_lastname.grid(row=1, column=1, padx=10, pady=5)

                label_age = tk.Label(edit_window, text="Вік:")
                label_age.grid(row=2, column=0, padx=10, pady=5)
                entry_age = tk.Entry(edit_window)
                entry_age.insert(0, data[3])
                entry_age.grid(row=2, column=1, padx=10, pady=5)

                label_email = tk.Label(edit_window, text="Email:")
                label_email.grid(row=3, column=0, padx=10, pady=5)
                entry_email = tk.Entry(edit_window)
                entry_email.insert(0, data[4])
                entry_email.grid(row=3, column=1, padx=10, pady=5)

                button_add = tk.Button(edit_window, text="Змінити", command=edit_user)
                button_add.grid(row=4, column=0, columnspan=2, pady=5)

            font_params = 'Arial 8 bold'

            tk.Label(top, text="ID", font=font_params).grid(sticky='W', row=0, column=0)
            tk.Label(top, text="Ім'я", font=font_params).grid(sticky='W', row=0, column=1)
            tk.Label(top, text="Прізвище", font=font_params).grid(sticky='W', row=0, column=2)
            tk.Label(top, text="Вік", font=font_params).grid(sticky='W', row=0, column=3)
            tk.Label(top, text="Email", font=font_params).grid(sticky='W', row=0, column=4)

            for i, row in enumerate(data):
                i = i + 1
                tk.Label(top, text=row[0]).grid(sticky='W', row=i, column=0)
                tk.Label(top, text=row[1]).grid(sticky='W', row=i, column=1)
                tk.Label(top, text=row[2]).grid(sticky='W', row=i, column=2)
                tk.Label(top, text=row[3]).grid(sticky='W', row=i, column=3)
                tk.Label(top, text=row[4]).grid(sticky='W', row=i, column=4)
                tk.Button(top, text='Видалити', command=lambda i=i, id=row[0]: delete_row(i, id)) \
                    .grid(sticky='W', row=i, column=5)
                tk.Button(top, text='Змінити', command=lambda i=i, id=row[0]: edit(id)) \
                    .grid(sticky='W', row=i, column=6)

        else:
            messagebox.showinfo("Інформація", "База даних користувачів порожня.")


if __name__ == "__main__":
    root = tk.Tk()
    app = UserDatabaseApp(root)
    root.mainloop()
