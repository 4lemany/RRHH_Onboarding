from pathlib import Path
import re
import fitz  # Importamos la librería PyMuPDF

def extraer_texto_pdf_limpio(ruta_pdf):
    documento = fitz.open(ruta_pdf)
    texto_completo = ""

    # 1. Definimos la "Lista Negra" de ruido habitual en documentos del BOE
    lista_negra = [
        "Boletín Oficial del Estado",
        "NIPO",
        "ISBN:",
        "Depósito Legal:",
        "cpage.mpr.gob.es",
        "www.boe.es"
    ]

    # 2. Extracción y primer filtrado línea a línea
    for num_pagina in range(len(documento)):
        pagina = documento[num_pagina]
        texto_pagina = pagina.get_text()
        lineas = texto_pagina.split('\n')
        lineas_limpias = []

        for linea in lineas:
            linea_str = linea.strip()
            
            # Condición A: Suficiente longitud
            # Condición B: Que no tenga palabras de la lista negra
            # Condición C: Que no sea una línea de índice (sin puntos suspensivos)
            if len(linea_str) > 3 and not any(basura in linea_str for basura in lista_negra) and "...." not in linea_str:
                lineas_limpias.append(linea_str)

        texto_completo += " ".join(lineas_limpias) + "\n\n"

    documento.close()

    # 3. Cortes Quirúrgicos específicos (solo se aplican si se detectan en el texto)
    marcador_fin = "ÍNDICE ANALÍTICO"
    if marcador_fin in texto_completo:
        texto_completo = texto_completo.split(marcador_fin)[0]

    marcador_inicio = "TÍTULO I De la relación individual de trabajo"
    if marcador_inicio in texto_completo:
        texto_completo = marcador_inicio + texto_completo.split(marcador_inicio)[1]

    # 4. Limpieza final: Eliminar espacios múltiples
    texto_completo = re.sub(r' {2,}', ' ', texto_completo)

    return texto_completo

# Obtener la ruta de la carpeta donde se encuentra este script
carpeta_actual = Path(__file__).parent

# Buscar todos los archivos .pdf en la carpeta del script
archivos_pdf = list(carpeta_actual.glob("*.pdf"))

if not archivos_pdf:
    print(f"No se encontraron archivos .pdf en la carpeta: {carpeta_actual}")
    print("Coloca tus archivos PDF en esta misma carpeta para poder convertirlos a texto plano.")
else:
    print(f"Se encontraron {len(archivos_pdf)} archivos PDF en la carpeta.\n")
    
    for ruta_pdf in archivos_pdf:
        # Definir la ruta de salida con el mismo nombre pero extensión .txt
        ruta_salida = ruta_pdf.with_suffix(".txt")
        print(f"Procesando: {ruta_pdf.name} ...")
        
        try:
            texto_limpio = extraer_texto_pdf_limpio(ruta_pdf)
            with open(ruta_salida, "w", encoding="utf-8") as archivo:
                archivo.write(texto_limpio)
            print(f" -> ¡Éxito! Archivo de texto creado en: {ruta_salida.name}\n")
        except Exception as e:
            print(f" -> Error al procesar {ruta_pdf.name}: {e}\n")
            
    print("¡Proceso de conversión finalizado!")

    # --- ENCADENAMIENTO DE TAREAS ---
    import subprocess
    import sys
    script_fragmentar = carpeta_actual / "fragmentar_estatuto.py"
    print(f"\n[Encadenamiento] Iniciando fragmentar_estatuto.py...")
    subprocess.run([sys.executable, str(script_fragmentar)], check=True)

