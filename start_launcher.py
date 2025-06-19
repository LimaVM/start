# start_launcher.py
import hashlib
import os
import subprocess
import uuid
from datetime import datetime
import time
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

SEGREDO = "StartSoftware2025"
ARQUIVO_ORIGINAL = "software.exe"
ARQUIVO_CRIPTO = "startshield.dat"
ARQUIVO_TEMP = "_start_temp.exe"
ARQUIVO_ID = "id.dat"
CHAVE_VITALICIA = "VOLTESEMPRE-START"
SUPORTE = "Entre em contato com o administrador: (61) 99997-4302"

def pegar_id_maquina():
    return str(uuid.getnode())

def salvar_id(id_maquina):
    with open(ARQUIVO_ID, "w") as f:
        f.write(id_maquina)

def carregar_id():
    if not os.path.exists(ARQUIVO_ID):
        return None
    with open(ARQUIVO_ID, "r") as f:
        return f.read().strip()

def embaralhar_data(data: str) -> str:
    dia, mes, ano = data.split("/")
    s = ano[2:] + mes + dia
    mapa = "Z8Y7X6W5V4U3T2S1R0QPONMLKJIHGFEDCBA9876543210"
    chave = ""
    for i, c in enumerate(s):
        v = int(c)
        chave += mapa[(v + i * 3) % len(mapa)]
    return chave[:8]

def desembra(data_code: str) -> str:
    mapa = "Z8Y7X6W5V4U3T2S1R0QPONMLKJIHGFEDCBA9876543210"
    indices = [mapa.index(c) for c in data_code]
    vals = [(v - i * 3) % 10 for i, v in enumerate(indices)]
    dia = str(vals[5]) + str(vals[6])
    mes = str(vals[3]) + str(vals[4])
    ano = "20" + str(vals[0]) + str(vals[1])
    return f"{dia}/{mes}/{ano}"

def dias_restantes(data_expiracao: str) -> int:
    hoje = datetime.now()
    exp = datetime.strptime(data_expiracao, "%d/%m/%Y")
    return (exp - hoje).days

def criptografar(nome_in, nome_out, chave):
    with open(nome_in, "rb") as f:
        data = f.read()
    data = bytearray([b ^ ord(chave[i % len(chave)]) for i, b in enumerate(data)])
    with open(nome_out, "wb") as f:
        f.write(data)

def descriptografar(nome_in, nome_out, chave):
    criptografar(nome_in, nome_out, chave)  # mesma função

def erro(msg):
    messagebox.showerror("Erro", f"{msg}\n{SUPORTE}")
    sys.exit()

def alerta(msg):
    messagebox.showwarning("Atenção", msg)

def pedir_input(prompt: str) -> str:
    """Exibe uma janela grande para entrada de texto."""
    var = tk.StringVar()

    def confirmar():
        root.quit()

    for w in root.winfo_children():
        if getattr(w, "is_bg", False):
            continue
        w.destroy()

    bg_label = tk.Label(root, image=root.bg_image)
    bg_label.place(relwidth=1, relheight=1)
    bg_label.lower()
    bg_label.is_bg = True
    root.bg_label = bg_label

    frame = tk.Frame(root, bg="#ffffff", bd=0)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text=prompt, bg="#ffffff").pack(pady=20)
    entry = tk.Entry(frame, textvariable=var, width=30)
    entry.pack(pady=10)
    tk.Button(
        frame,
        text="Confirmar",
        command=confirmar,
        bg="#4CAF50",
        fg="white",
        padx=20,
        pady=10,
    ).pack(pady=20)
    entry.focus()
    root.deiconify()
    root.mainloop()
    root.withdraw()
    return var.get().strip()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Start Launcher")
    root.geometry("800x500")
    root.option_add("*Font", "Helvetica 18")
    root.iconbitmap("icon.ico")
    root.configure(bg="#f0f0f0")

    bg_image = ImageTk.PhotoImage(Image.open("icon.jpeg"))
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)
    bg_label.lower()
    bg_label.is_bg = True

    root.withdraw()
    root.bg_image = bg_image
    id_atual = pegar_id_maquina()
    id_salvo = carregar_id()

    # Primeira inicialização
    if not id_salvo:
        if not os.path.exists(ARQUIVO_ORIGINAL):
            erro("Erro: Arquivo raiz não encontrado.")
        messagebox.showinfo("Primeira execução", "🔐 Primeira execução detectada.")
        while True:
            data = pedir_input("Data de expiração (DD/MM/AAAA):")
            if not data:
                erro("Data de expiração não fornecida.")
            try:
                datetime.strptime(data, "%d/%m/%Y")
                break
            except Exception:
                messagebox.showerror("Erro", "Data inválida. Tente novamente.")
        chave_gerada = embaralhar_data(data)
        criptografar(ARQUIVO_ORIGINAL, ARQUIVO_CRIPTO, chave_gerada)
        os.remove(ARQUIVO_ORIGINAL)
        salvar_id(id_atual)
        messagebox.showinfo(
            "Sucesso",
            "✅ Software protegido com sucesso.\nAgora inicie novamente com sua chave.",
        )
        sys.exit()

    # Impede cópia para outro PC
    if id_atual != id_salvo:
        erro("Este programa foi copiado de outra máquina.")

    if not os.path.exists(ARQUIVO_CRIPTO):
        erro("Arquivo raiz não encontrado.")

    chave_usuario = pedir_input("Digite sua chave de ativação:")
    if not chave_usuario:
        erro("Nenhuma chave informada.")
    chave_usuario = chave_usuario.strip().upper()

    if chave_usuario == CHAVE_VITALICIA:
        messagebox.showinfo("Licença", "🔓 Licença vitalícia ativada.")
        data_decodificada = "31/12/2099"
    else:
        try:
            data_decodificada = desembra(chave_usuario)
            dias = dias_restantes(data_decodificada)
        except Exception:
            erro("Chave inválida.")

        if dias < -2:
            erro("Licença expirada.")
        elif dias == -2 or dias == -1:
            alerta("Licença vencida! Período de tolerância ativo.")
        elif dias == 0:
            alerta("Hoje é o último dia de uso da licença.")
        elif dias <= 2:
            alerta(f"Atenção: Faltam {dias} dias para a licença vencer.")

    # Descriptografar e executar
    descriptografar(ARQUIVO_CRIPTO, ARQUIVO_TEMP, chave_usuario)
    proc = subprocess.Popen(ARQUIVO_TEMP)

    # Monitorar vencimento enquanto o software roda
    while proc.poll() is None:
        if chave_usuario != CHAVE_VITALICIA:
            if dias_restantes(data_decodificada) < -2:
                proc.kill()
                os.remove(ARQUIVO_TEMP)
                erro("Licença expirada. O software foi encerrado.")
        time.sleep(60)

    if os.path.exists(ARQUIVO_TEMP):
        os.remove(ARQUIVO_TEMP)
    root.destroy()
