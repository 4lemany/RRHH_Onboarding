from pathlib import Path
import sys
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Reconfigurar la consola para que admita caracteres españoles sin fallar
sys.stdout.reconfigure(encoding='utf-8')

def fragmentar_documento(ruta_txt):
    # 1. Leemos el archivo limpio
    with open(ruta_txt, "r", encoding="utf-8") as archivo:
        texto_completo = archivo.read()

    # 2. Configuramos el fragmentador inteligente
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        length_function=len,
        separators=["\n\n", "\n", ".", " ", ""] 
    )

    # 3. Ejecutamos la fragmentación
    fragmentos = text_splitter.create_documents([texto_completo])
    return fragmentos

# Ejecutamos el proceso
carpeta_actual = Path(__file__).parent

# Buscar todos los archivos .txt en la carpeta del script (excluyendo tutoriales o archivos markdown)
archivos_txt = list(carpeta_actual.glob("*.txt"))

if not archivos_txt:
    print(f"Error: No se encontraron archivos .txt en: {carpeta_actual}")
    print("Asegúrate de haber ejecutado primero converter_pdf_a_texto.py.")
else:
    print(f"Se encontraron {len(archivos_txt)} archivos de texto para fragmentar.\n")
    for ruta_datos in archivos_txt:
        print(f"=== Procesando fragmentación de: {ruta_datos.name} ===")
        mis_fragmentos = fragmentar_documento(ruta_datos)
        print(f"Número total de fragmentos generados: {len(mis_fragmentos)}")

        # Imprimimos los dos primeros para comprobar visualmente que mantienen coherencia
        if len(mis_fragmentos) >= 1:
            print("\n  [Muestra del Fragmento 1]")
            print("  " + mis_fragmentos[0].page_content[:300] + "...")
        if len(mis_fragmentos) >= 2:
            print("\n  [Muestra del Fragmento 2]")
            print("  " + mis_fragmentos[1].page_content[:300] + "...\n")
            
    # --- ENCADENAMIENTO DE TAREAS ---
    import subprocess
    script_vectorizar = carpeta_actual / "vectorizar_estatuto.py"
    print(f"\n[Encadenamiento] Iniciando vectorizar_estatuto.py...")
    subprocess.run([sys.executable, str(script_vectorizar)], check=True)