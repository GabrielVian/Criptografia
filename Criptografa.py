from cryptography.fernet import Fernet

# Gerar chave e inicializar Fernet
chave = Fernet.generate_key()
f = Fernet(chave)

print(chave)

with open("texto.txt", "rb") as f_in:
    dados = f_in.read()
    cifrado = f.encrypt(dados)

with open("texto.txt.enc", "wb") as f_out:
    f_out.write(cifrado)

