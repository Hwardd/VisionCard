import re

def string_number_cleaner(texto):
    # Usamos una expresión regular para encontrar todos los dígitos y comas
    # y luego usamos ''.join() para combinarlos en un solo string
    resultado = ''.join(re.findall(r'[0-9,]', texto))
    
    # Si no se encontraron caracteres numéricos ni comas, devolvemos None
    if not resultado:
        return None
    
    return resultado

def string_text_cleaner(texto):
    # Usamos una expresión regular para encontrar todos los dígitos y comas
    # y luego usamos ''.join() para combinarlos en un solo string
    resultado = ''.join(re.findall(r'[0-9A-Za-z,]', texto))
    
    # Si no se encontraron caracteres numéricos ni comas, devolvemos None
    if not resultado:
        return None
    
    return resultado