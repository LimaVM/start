# gerador_chave.py
import datetime

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
    data = input("Data de expiração (DD/MM/AAAA): ").strip()
    try:
        datetime.datetime.strptime(data, "%d/%m/%Y")
        chave = embaralhar_data(data)
        print(f"\n🔑 Chave gerada: {chave}")
    except:
        print("❌ Data inválida.")
