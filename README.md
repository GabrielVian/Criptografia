# No repositório você vai encontrar duas maneiras de criptografar e decifrar dados. 

## Criar a venv

```bash
# ~ python3 -m venv venv
// linux/mac
# ~ source venv/bin/activate
// Windows (PowerShell)
# ~ venv\Scripts\Activate.ps1
```

## Simplificado (usando dois arquivos)
> Existe um arquivo chamado texto.txt, ele pode ser modificado por você, mas o nome tem que ser mantido

```bash
# ~ python Criptografa.py 
b'hjasdfiouhqweiunfiwuehrihsfd'
```

- Copie a chave passada por inteiro (até o "b''")

- Será gerado um arquivo .enc

```bash
# ~ python Descriptografa.py 
```

- Será gerado um arquivo descriptografado igual ao original

## Interface WEB
> Usando flask

- Crie uma venv (ambiente) nova para instalar as dependências encontradas no *requirements.txt*

- Depois rode:
```bash
# ~ python app.py
```
> Isso vai abrir uma porta (6100) no seu localhost. Acesse a interface e utilize para criptografar qualquer arquivo


