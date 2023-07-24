import re
import hashlib
import tkinter as tk
import tkinter.ttk as ttk


def email_check(email: str) -> bool:
    return (
        True
        if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-z0-9-.]+$", email)
        else False
    )


def password_check(password: str) -> bool:
    return (
        True
        if re.match(
            r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", password
        )
        else False
    )


def save_credentials():
    email = entry_email.get()
    password = entry_password.get() #qwertyQWERTY123!@ <-- valid password

    if email_check(email) and password_check(password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        with open("credentials.txt", "a") as file:
            file.write(f"Email: {email}\n")
            file.write(f"Password: {hashed_password}\n")
            file.write("\n")

        label_result.config(text="Регистрация прошла успешно!")
    else:
        label_result.config(text="Некорректный email или пароль. Повторите попытку.")


def clicked():
    save_credentials()


window = tk.Tk()
window.title("Регистрация")
window.geometry("1280x720")

label_email = tk.Label(window, text="Email:", font=("Arial Bold", 12))
label_email.grid(column=0, row=0, sticky="E")

entry_email = tk.Entry(window, width=30, font=("Arial", 12))
entry_email.grid(column=1, row=0)

label_password = tk.Label(window, text="Пароль:", font=("Arial Bold", 12))
label_password.grid(column=0, row=1, sticky="E")

entry_password = tk.Entry(window, width=30, show="*", font=("Arial", 12))
entry_password.grid(column=1, row=1)

button_register = tk.Button(
    window, text="Зарегистрироваться", command=clicked, font=("Arial Bold", 12)
)
button_register.grid(column=1, row=2)

label_result = tk.Label(window, text="", font=("Arial", 12))
label_result.grid(column=0, row=3, columnspan=2)

window.mainloop()
