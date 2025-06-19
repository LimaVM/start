
# 🛡️ Protetor Start do Brasil – Sistema de Licenciamento Offline

Este sistema protege o acesso ao `software.exe` com criptografia, verificação de licença por chave de ativação e controle rígido de máquina. Tudo funciona 100% offline.

---

## 📂 Estrutura do Projeto

```
/StartSoftware/
├── start_launcher.exe         # Launcher que protege e executa
├── gerador_chave.exe          # Gerador de chaves baseado na data
├── software.exe               # Arquivo original (só na primeira execução)
├── startshield.dat            # Arquivo criptografado (gerado automaticamente)
├── id.dat                     # ID da máquina original (gerado na primeira execução)
```

---

## ⚙️ Como funciona

### 🛠 Primeira execução (`start_launcher.exe`)
1. Verifica se existe o `software.exe` na pasta.
2. Se não existir:  
   ❌ Erro: Arquivo raiz não encontrado.  
   👉 **Entre em contato com o administrador: (61) 99997-4302**
3. Se existir:
   - Criptografa como `startshield.dat`
   - Remove o `software.exe`
   - Salva o identificador da máquina como `id.dat`
   - Finaliza com sucesso e solicita reinício com a chave

---

### 🔐 Validação nas execuções seguintes
1. Solicita a **chave de ativação de 8 caracteres**
2. A chave decodifica a **data de expiração**
3. Verifica:
   - Se a máquina é a original (ID bate com `id.dat`)
   - Quantos dias faltam ou se já venceu
4. Comportamento:
   - ✅ Até 2 dias antes: alerta de aviso
   - ⚠️ No dia do vencimento: alerta forte
   - ⏳ Até 2 dias após vencimento: alerta + ainda executa
   - ❌ Após isso: bloqueia e exige nova chave

---

### 🔁 Enquanto o software roda:
- O launcher fica **monitorando em segundo plano**
- Se a data ultrapassar o limite de 2 dias vencido:
  - Fecha o software automaticamente
  - Exibe:
    ```
    ❌ Licença expirada. O software foi encerrado.
    Entre em contato com o administrador: (61) 99997-4302
    ```

---

## 🧑‍💻 Como gerar uma chave

1. Execute:
```bash
python gerador_chave.py
```

2. Digite a data de expiração no formato `DD/MM/AAAA`

3. Você receberá uma chave como:
```
🔑 Chave gerada: A9K3X2M1
```

💡 Essa chave deve ser enviada ao usuário junto com a data de expiração.

---

## 🧪 Chave vitalícia

Chave especial para desbloqueio permanente:

```
VOLTESEMPRE-START
```

---

## 📦 Compilação recomendada

```bash
pyinstaller --noconsole --onefile --icon=icon.ico start_launcher.py
pyinstaller --console --onefile gerador_chave.py
```

---

## 📞 Suporte

Em todos os erros, exiba para o usuário:

```
Entre em contato com o administrador: (61) 99997-4302
```

---

© 2025 Start do Brasil
