# gerador_chave.py
import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry

def embaralhar_data(data: str) -> str:
    # Entrada: "DD/MM/AAAA"
    dia, mes, ano = data.split("/")
    s = ano[2:] + mes + dia  # Ex: "250630"
    mapa = "Z8Y7X6W5V4U3T2S1R0QPONMLKJIHGFEDCBA9876543210"
    chave = ""
    for i, c in enumerate(s):
        v = int(c)
        chave += mapa[(v + i * 3) % len(mapa)]
    return chave[:8]

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gerador de Chave")
    root.geometry("700x400")
    root.option_add("*Font", "Helvetica 18")
    root.iconbitmap("icon.ico")

    bg_image = ImageTk.PhotoImage(Image.open("icon.jpeg"))
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)
    bg_label.lower()

    frame = tk.Frame(root, bg="#ffffff", bd=0)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        frame,
        text="Data de expiração:",
        bg="#ffffff",
    ).pack(pady=20)

    data_var = tk.StringVar()
    entry = DateEntry(
        frame,
        textvariable=data_var,
        date_pattern="dd/mm/yyyy",
        background="#4CAF50",
        foreground="white",
        borderwidth=2,
        width=18,
    )
    entry.pack(pady=10)
    entry.focus()

    result_var = tk.StringVar()
    tk.Label(frame, textvariable=result_var, bg="#ffffff").pack(pady=20)

    def gerar():
        data = data_var.get().strip()
        try:
            datetime.datetime.strptime(data, "%d/%m/%Y")
            chave = embaralhar_data(data)
            result_var.set(f"🔑 {chave}")
        except Exception:
            messagebox.showerror("Erro", "❌ Data inválida.")

    tk.Button(
        frame,
        text="Gerar Chave",
        command=gerar,
        bg="#4CAF50",
        fg="white",
        padx=20,
        pady=10,
    ).pack(pady=10)

    root.mainloop()
