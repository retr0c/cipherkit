import itertools
import math
import time
import sys
from concurrent.futures import ProcessPoolExecutor
from ciphers import caesar, vigenere, rot13, atbash, box_caesar
from ciphers.vigenere import score, _KEY_DICT

# Mapeo necesario para el menú y compatibilidad con main.py
CIPHER_MAP = {
    "1": caesar, "2": vigenere, "3": rot13, "4": atbash, "5": box_caesar
}
CIPHER_DISPLAY_NAMES = {
    "1": "Caesar", "2": "Vigenère", "3": "ROT13", "4": "Atbash", "5": "Caja Caesar"
}

def estimate_combinations(selected_ids: list) -> int:
    """
    Calcula de forma exacta el número de combinaciones basadas 
    únicamente en los cifrados seleccionados por el usuario.
    """
    permutations_count = math.perm(len(selected_ids))
    total = permutations_count
    
    if "2" in selected_ids:  # Vigenère
        total *= len(_KEY_DICT)
    if "1" in selected_ids:  # Caesar
        total *= 26
    if "5" in selected_ids:  # Caja Caesar (Rango de 2 a 15 columnas)
        total *= 14
        
    return total

def _worker_crack_permutation(args):
    """
    Worker global requerido para Multiprocessing. 
    Procesa una permutación completa en un núcleo independiente de la CPU.
    """
    p, text, v_keys, c_shifts, box_sizes = args
    local_results = []
    
    for v_key in v_keys:
        for c_shift in c_shifts:
            for box_size in box_sizes:
                current = text
                # Ejecución en cadena según el orden de la permutación
                for cid in p:
                    if cid == "2":   
                        current = vigenere.decrypt(current, v_key)
                    elif cid == "1": 
                        current = caesar.decrypt(current, c_shift)
                    elif cid == "3": 
                        current = rot13.decrypt(current)
                    elif cid == "4": 
                        current = atbash.decrypt(current)
                    elif cid == "5": 
                        current = box_caesar.decrypt(current, box_size)
                
                current_score = score(current)
                
                if current_score > 0.0:
                    # Crear una lista de claves descriptiva solo para los cifrados usados en esta permutación
                    claves_usadas = []
                    for cid in p:
                        if cid == "2": claves_usadas.append(f"Vig:{v_key}")
                        elif cid == "1": claves_usadas.append(f"Cae:{c_shift}")
                        elif cid == "5": claves_usadas.append(f"Box:{box_size}")
                        else: claves_usadas.append("N/A")
                    
                    local_results.append({
                        "order": p, 
                        "text": current,
                        "score": current_score,
                        "keys": claves_usadas
                    })
                    
    # Ordenamos el lote de este núcleo y retornamos únicamente el Top 10 para ahorrar IPC
    local_results.sort(key=lambda x: x["score"], reverse=True)
    return local_results[:10]

def crack(text: str, selected_ids: list) -> list[dict]:
    """
    Función general adaptada a CipherKit v2 que paraleliza el procesamiento
    y actualiza la barra de progreso de main.py en tiempo real.
    """
    results = []
    permutations = list(itertools.permutations(selected_ids))
    total_combinations = estimate_combinations(selected_ids)
    
    # Preparar los paquetes de datos para los sub-procesos
    tasks = []
    for p in permutations:
        v_keys = _KEY_DICT if "2" in p else [""]
        c_shifts = range(26) if "1" in p else [0]
        box_sizes = range(2, 16) if "5" in p else [0]
        tasks.append((p, text, v_keys, c_shifts, box_sizes))
        
    processed_combinations = 0
    start_time = time.time()
    
    # Orquestador multi-núcleo de alto rendimiento
    with ProcessPoolExecutor() as executor:
        from concurrent.futures import as_completed
        futures = {executor.submit(_worker_crack_permutation, task): task for task in tasks}
        
        for future in as_completed(futures):
            p, _, v_keys, c_shifts, box_sizes = futures[future]
            local_top = future.result()
            
            for res in local_top:
                results.append({
                    "sequence": [f"{CIPHER_DISPLAY_NAMES[cid]}" for cid in res["order"]],
                    "text": res["text"],
                    "score": res["score"],
                    "keys": res["keys"] # Ahora es una lista de strings limpia
                })
            # Calcular el avance en base a las combinaciones reales completadas por el proceso terminado
            task_combinations = len(v_keys) * len(c_shifts) * len(box_sizes)
            processed_combinations += task_combinations
            
            # Clonar el diseño exacto de tu TUI en consola de manera dinámica
            pct = (processed_combinations / total_combinations) * 100
            filled = int(pct // 2.5)  # 40 bloques en total equivalentes a la barra original
            bar_str = "█" * filled + "░" * (40 - filled)
            elapsed = time.time() - start_time
            
            # El '\r' inicial barre la línea estática de main.py y la actualiza con esteroides
            sys.stdout.write(f"\r  Probando combinaciones: [{bar_str}]   {pct:.0f}%  {processed_combinations}/{total_combinations}  ({elapsed:.1f}s)   ")
            sys.stdout.flush()
            
    # Clasificación global definitiva de candidatos legibles
    results.sort(key=lambda x: x["score"], reverse=True)
    print()  # Salto de línea limpio para no alterar los siguientes menús de la interfaz
    return results[:100]