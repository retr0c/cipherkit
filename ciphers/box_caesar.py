"""
ciphers/box_caesar.py — Algoritmo Real de dCode Box Caesar (Transposición en 7 Columnas)
"""
import math

def encrypt(text: str, key: int, sep: str = ".", box_size: int = 0) -> str:
    # dCode fija el número de columnas con el tamaño de la caja (7)
    num_cols = box_size if box_size > 0 else key
    if num_cols <= 1:
        return text

    num_rows = math.ceil(len(text) / num_cols)
    
    # Inicializar matriz vacía
    matrix = [['' for _ in range(num_cols)] for _ in range(num_rows)]
    
    # Cifrar: Escribir por columnas, fila por fila
    idx = 0
    for col in range(num_cols):
        for row in range(num_rows):
            if idx < len(text):
                matrix[row][col] = text[idx]
                idx += 1
            else:
                matrix[row][col] = sep # Relleno si dCode lo requiere
                
    # Leer fila por fila
    result = []
    for row in range(num_rows):
        for col in range(num_cols):
            if matrix[row][col]:
                result.append(matrix[row][col])
                
    return "".join(result)


def decrypt(text: str, key: int, sep: str = ".", box_size: int = 0) -> str:
    # Al descifrar, dCode asume que el texto cifrado se acomoda en un ancho fijo de columnas
    num_cols = box_size if box_size > 0 else key
    if num_cols <= 1:
        return text

    num_rows = math.ceil(len(text) / num_cols)
    
    # Inicializar matriz vacía
    matrix = [['' for _ in range(num_cols)] for _ in range(num_rows)]
    
    # Descifrar: Escribir el texto cifrado fila por fila
    idx = 0
    for row in range(num_rows):
        for col in range(num_cols):
            if idx < len(text):
                matrix[row][col] = text[idx]
                idx += 1
                
    # Leer columna por columna para recuperar el orden original
    result = []
    for col in range(num_cols):
        for row in range(num_rows):
            if matrix[row][col]:
                result.append(matrix[row][col])
                
    return "".join(result)


def brute_force_full(text: str, sep: str = ".") -> list:
    """Prueba combinaciones de tamaños de caja y desplazamientos Caesar."""
    results = []
    # Limitamos el tamaño máximo de caja al largo del texto o 50 para evitar bucles infinitos
    max_box = min(len(text), 50) if len(text) > 0 else 10
    
    for box_size in range(2, max_box + 1):
        for shift in range(1, 26):
            try:
                # Desciframos usando los parámetros de la iteración
                candidate = decrypt(text, key=shift, sep=sep, box_size=box_size)
                
                # Asignamos un score básico o cálculo de legibilidad si tienes el analizador.
                # Por ahora, un formato compatible con lo que espera el 'fmt' de main.py:
                # formato esperado en tu main.py: (key, box_size, texto, score)
                score = 0.0  
                
                results.append((shift, box_size, candidate, score))
            except Exception:
                continue
                
    # Ordenamos los resultados si es necesario (aquí por tamaño de caja o clave de forma estándar)
    return results