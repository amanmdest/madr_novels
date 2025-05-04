def sanitiza(string):
    sanitizado = ''
    for letra in string: 
        if letra.isalnum() or letra.isspace():
            sanitizado += letra.lower()
    return ' '.join(sanitizado.split())
