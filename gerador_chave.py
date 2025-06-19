# gerador_chave.py
import datetime
import tkinter as tk
from tkinter import messagebox

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
    root.geometry("600x300")
    root.configure(bg="#f0f0f0")
    root.option_add("*Font", "Helvetica 16")

    tk.Label(
        root,
        text="Data de expiração (DD/MM/AAAA):",
        bg="#f0f0f0",
    ).pack(pady=20)

    data_var = tk.StringVar()
    entry = tk.Entry(root, textvariable=data_var, width=20)
    entry.pack(pady=10)
    entry.focus()

    result_var = tk.StringVar()
    tk.Label(root, textvariable=result_var, bg="#f0f0f0").pack(pady=20)

    def gerar():
        data = data_var.get().strip()
        try:
            datetime.datetime.strptime(data, "%d/%m/%Y")
            chave = embaralhar_data(data)
            result_var.set(f"🔑 {chave}")
        except Exception:
            messagebox.showerror("Erro", "❌ Data inválida.")

    tk.Button(
        root,
        text="Gerar Chave",
        command=gerar,
        bg="#4CAF50",
        fg="white",
        padx=20,
        pady=10,
    ).pack(pady=10)

    root.mainloop()
