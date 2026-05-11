import google.generativeai as genai
import os
from PIL import Image
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def analisiscongemini():
    API_KEY = os.getenv('API_KEYY')
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-flash-latest')

    def analizar_lote(carpeta_origen):
        if not os.path.exists(carpeta_origen):
            print(f"Error: La carpeta {carpeta_origen} no existe.")
            return

        #listamos archivos que sean imagenes 
        extensiones_validas = ('.png', '.jpg', '.jpeg')
        archivos = [f for f in os.listdir(carpeta_origen) if f.lower().endswith(extensiones_validas)]

        if not archivos:
            print("No se encontraron imágenes en la carpeta.")
            return

        print(f"Se encontraron {len(archivos)} ejercicios. Iniciando proceso...\n")

        
        for nombre_archivo in archivos:
            ruta_completa = os.path.join(carpeta_origen, nombre_archivo)
            
            try:
                img = Image.open(ruta_completa)
                
                prompt = (
                    "Pretende que eres un profesor de matemáticas de Harvard. Analiza esta imagen. "
                    "Da el resultado final claramente como RESULTADO GEMINI: [valor]. "
                    "No quiero explicaciones, SOLO el resultado final sin decoraciones."
                )

                print(f"Cargando: {nombre_archivo}...")
                response = model.generate_content([prompt, img])
                
                
                print(f"Archivo: {nombre_archivo} -> {response.text.strip()}")

            except Exception as e:
                print(f"Error con {nombre_archivo}: {e}")

    ruta_carpeta = r'C:\Users\Santi\Desktop\ejerciciosss' 
    analizar_lote(ruta_carpeta)



def analisisconqwenmath():
    

    OPENROUTER_KEY = os.getenv('OPENROUTER_KEY')    
    

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_KEY,
    )

    def codificar_imagen_base64(ruta_imagen):
        try:
            with open(ruta_imagen, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except FileNotFoundError:
            print(f"No se encontro el archivo en {ruta_imagen}")
            return None

    def procesar_carpeta_qwen(ruta_carpeta):
        if not os.path.exists(ruta_carpeta):
            print(f"La carpeta '{ruta_carpeta}' no existe.")
            return

        # Listamos los archivos de imagen
        archivos = [f for f in os.listdir(ruta_carpeta) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not archivos:
            print("no hay imagenes en la carpeta.")
            return


        for nombre_archivo in archivos:
            ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
            imagen_base64 = codificar_imagen_base64(ruta_completa)
            
            if not imagen_base64:
                continue

            try:
                print(f"enviando {nombre_archivo} a Qwen2-VL...")
                
                response = client.chat.completions.create(
                    model="qwen/qwen-2-vl-72b-instruct",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text", 
                                    "text": "Pretende que eres un profesor de matemáticas de Harvard. Analiza la imagen de este ejercicio matemático. "
                                            "Da el resultado final claramente como RESULTADO QWEN-MATH: [valor]. "
                                            "No quiero explicaciones, SOLO el RESULTADO FINAL sin decoraciones."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{imagen_base64}"
                                    }
                                }
                            ]
                        }
                    ]
                )

                solucion = response.choices[0].message.content
                print(f"Archivo: {nombre_archivo} -> {solucion.strip()}")

            except Exception as e:
                print(f"error al procesar {nombre_archivo} con Qwen: {e}")

    ruta_ejercicios = r'C:\Users\Santi\Desktop\ejerciciosss'
    procesar_carpeta_qwen(ruta_ejercicios)



analisisconqwenmath()