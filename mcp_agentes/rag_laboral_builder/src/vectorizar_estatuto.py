from pathlib import Path
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_chroma import Chroma

# Reconfigurar la consola para que admita caracteres españoles sin fallar
sys.stdout.reconfigure(encoding='utf-8')

# Obtener la carpeta donde se encuentra este script
carpeta_actual = Path(__file__).parent

# Cargar variables de entorno del archivo .env de la raíz (subiendo 2 niveles)
ruta_env = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ruta_env)

# Configurar el ID del proyecto de GCP obtenido del .env
proyecto_gcp = os.getenv("GOOGLE_CLOUD_PROJECT", "project3grupo1")
os.environ["GOOGLE_CLOUD_PROJECT"] = proyecto_gcp

# Configurar la localización si está en el .env
if os.getenv("GOOGLE_CLOUD_LOCATION"):
    os.environ["GOOGLE_CLOUD_LOCATION"] = os.getenv("GOOGLE_CLOUD_LOCATION")

print(f"Usando proyecto GCP: {os.environ['GOOGLE_CLOUD_PROJECT']}")

def crear_base_vectorial(archivos_txt, directorio_bd):
    # 1. Conectar con Vertex AI para preparar el modelo de embeddings
    print("Conectando con Vertex AI y configurando modelo de embeddings...")
    modelo_embeddings = VertexAIEmbeddings(model_name="text-embedding-004")

    # 2. Cargar base de datos existente si ya existe para acumular el conocimiento
    base_de_datos = None
    if directorio_bd.exists():
        print(f"Base de datos vectorial existente detectada en: {directorio_bd}")
        print(" -> Cargando base de datos para acumular nuevos documentos (sin borrar los anteriores)...")
        base_de_datos = Chroma(
            persist_directory=str(directorio_bd),
            embedding_function=modelo_embeddings
        )

    # 3. Leer y fragmentar cada archivo de texto disponible
    for ruta_txt in archivos_txt:
        print(f"\nProcesando documento: {ruta_txt.name}")
        with open(ruta_txt, "r", encoding="utf-8") as archivo:
            texto_completo = archivo.read()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100,
            length_function=len,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        fragmentos = text_splitter.create_documents([texto_completo])
        
        # Añadir metadato de origen
        for f in fragmentos:
            f.metadata["source"] = ruta_txt.name
            
        print(f" -> Generados {len(fragmentos)} fragmentos.")

        # 4. Procesar en lotes de 40 para evitar superar los límites de tokens de Vertex AI
        tamanio_batch = 40
        print(f" -> Indexando fragmentos en base de datos Chroma local...")
        for i in range(0, len(fragmentos), tamanio_batch):
            batch = fragmentos[i:i + tamanio_batch]
            print(f"    -> Procesando lote {(i // tamanio_batch) + 1} (fragmentos {i} a {i + len(batch)})...")
            if base_de_datos is None:
                # Si es la primera vez de todas que creamos la base
                base_de_datos = Chroma.from_documents(
                    documents=batch,
                    embedding=modelo_embeddings,
                    persist_directory=str(directorio_bd)
                )
            else:
                # Si ya existía o ya se inicializó en el lote anterior, los añadimos
                base_de_datos.add_documents(documents=batch)

        # 5. Operaciones de limpieza post-procesamiento y registro
        # Borrar PDF y TXT para dejar la carpeta limpia
        ruta_pdf = ruta_txt.with_suffix(".pdf")
        if ruta_txt.exists():
            print(f" -> Borrando archivo temporal de texto: {ruta_txt.name}")
            ruta_txt.unlink()
        if ruta_pdf.exists():
            print(f" -> Borrando archivo PDF procesado: {ruta_pdf.name}")
            ruta_pdf.unlink()

        # Escribir en el registro histórico de RAG
        ruta_registro = carpeta_actual / "registro_documentos.txt"
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(ruta_registro, "a", encoding="utf-8") as registro:
            registro.write(f"[{fecha_actual}] Indexado correctamente: {ruta_pdf.name} ({len(fragmentos)} fragmentos)\n")
        print(f" -> Registrado en: {ruta_registro.name}")

    print(f"\n¡Éxito! Todos los documentos nuevos han sido indexados en la base de datos: {directorio_bd}")
    return base_de_datos

# Ejecutamos el proceso usando todos los archivos .txt de la carpeta
archivos_txt = list(carpeta_actual.glob("*.txt"))
directorio_bd = carpeta_actual / "mi_base_vectorial"

if not archivos_txt:
    print(f"No se encontraron nuevos archivos de texto (.txt) para procesar en: {carpeta_actual}")
else:
    crear_base_vectorial(archivos_txt, directorio_bd)