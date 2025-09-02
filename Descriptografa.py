from cryptography.fernet import Fernet

chave_str = input("Digite a chave: ")

if chave_str.startswith("b'") and chave_str.endswith("'"):
    chave_str = chave_str[2:-1]  

chave = chave_str.encode('latin-1')
f = Fernet(chave)

with open("texto.txt.enc", "rb") as f_in:
    dados_cifrados = f_in.read()
    decifrado = f.decrypt(dados_cifrados)

with open("texto_recuperado.txt", "wb") as f_out:
    f_out.write(decifrado)
