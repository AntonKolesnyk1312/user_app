import tkinter as tk
from DatabaseProxy import *


class DatabaseProxy:
    def __init__(self):
        # З'єднання з базою даних
        self.connection = sqlite3.connect("user_database.db")
        self.cursor = self.connection.cursor()

    def get_users(self):
        self.cursor.execute('SELECT * FROM users')
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

class UserDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Database App")
        self.root.geometry('400x300')

        self.db = DatabaseProxy()

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

        self.button_add = tk.Button(root, text="Додати", command=lambda: self.db.add_user(
            self.entry_name.get(), self.entry_lastname.get(), self.entry_age.get(), self.entry_email.get()
        ))
        self.button_add.grid(row=4, column=0, columnspan=2, pady=5)

        self.button_view = tk.Button(root, text="Переглянути користувачів", command=self.view_users)
        self.button_view.grid(row=5, column=0, columnspan=2, pady=5)

    def view_users(self):
        data = self.db.get_users()

        if data:
            top = tk.Toplevel(self.root)
            top.title("Список користувачів")

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

            def delete_row(row_index, id):
                # видалення рядка з інтерфейсу
                for widget in top.grid_slaves(row=row_index):
                    widget.grid_remove()

                self.db.delete_user(id)

            def edit(id):
                edit_window = tk.Toplevel(self.root)
                edit_window.title("Редагування користувача")

                label_name = tk.Label(edit_window, text="Ім'я:")
                label_name.grid(row=0, column=0, padx=10, pady=5)
                entry_name = tk.Entry(edit_window)
                entry_name.grid(row=0, column=1, padx=10, pady=5)

                label_lastname = tk.Label(edit_window, text="Прізвище:")
                label_lastname.grid(row=1, column=0, padx=10, pady=5)
                entry_lastname = tk.Entry(edit_window)
                entry_lastname.grid(row=1, column=1, padx=10, pady=5)

                label_age = tk.Label(edit_window, text="Вік:")
                label_age.grid(row=2, column=0, padx=10, pady=5)
                entry_age = tk.Entry(edit_window)
                entry_age.grid(row=2, column=1, padx=10, pady=5)

                label_email = tk.Label(edit_window, text="Email:")
                label_email.grid(row=3, column=0, padx=10, pady=5)
                entry_email = tk.Entry(edit_window)
                entry_email.grid(row=3, column=1, padx=10, pady=5)

                button_add = tk.Button(edit_window, text="Змінити", command=lambda: self.db.edit_user(
                    id, entry_name.get(), entry_lastname.get(), entry_age.get(), entry_email.get()
                ))
                button_add.grid(row=4, column=0, columnspan=2, pady=5)
        else:
            messagebox.showinfo("Інформація", "База даних користувачів порожня.")


if __name__ == "__main__":
    root = tk.Tk()
    app = UserDatabaseApp(root)
    root.mainloop()
