import google.generativeai as genai
import os
from PIL import Image
import base64
from openai import OpenAI
from dotenv import load_dotenv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from playwright.sync_api import sync_playwright
import os
from julius_api import Julius

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



TOKEN_JULIUS = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJoM0dwdVZXd2JMMTJpYnBtamlxWCJ9.eyJodHRwczovL2NoYXR3aXRoeW91cmRhdGEuaW8vdXNlcl9lbWFpbCI6InNvbG9kaXNjb3JkamFqYUBnbWFpbC5jb20iLCJodHRwczovL2NoYXR3aXRoeW91cmRhdGEuaW8vanVsaXVzX2lkIjoiZmQ1NTEyOTQtNDRkOS00ODE0LTlmMGItNDBmMDZlNjdjYWJhIiwiaHR0cHM6Ly9jaGF0d2l0aHlvdXJkYXRhLmlvL21lcmdlZF9zdWJfaWQiOiJnb29nbGUtb2F1dGgyXzEwMjU1ODM2NzE1NTM2NDY0MzY5OCIsImh0dHBzOi8vY2hhdHdpdGh5b3VyZGF0YS5pby91c2VyX2lwIjoiMjgwMzo5ODAwOjk4YzQ6NmVkZTo1NTJjOmMxNjU6ZDFkZjpiNmU4IiwiaHR0cHM6Ly9jaGF0d2l0aHlvdXJkYXRhLmlvL3VzZXJfY29udGluZW50Q29kZSI6IlNBIiwiaHR0cHM6Ly9jaGF0d2l0aHlvdXJkYXRhLmlvL2VtYWlsX3ZlcmlmaWVkIjp0cnVlLCJodHRwczovL2NoYXR3aXRoeW91cmRhdGEuaW8vY3JlYXRlZF9hdCI6IjIwMjYtMDUtMjBUMTg6MDA6MDUuMDc5WiIsImlzcyI6Imh0dHBzOi8vYXV0aC5qdWxpdXMuYWkvIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDI1NTgzNjcxNTUzNjQ2NDM2OTgiLCJhdWQiOlsiaHR0cHM6Ly9jaGF0d2l0aHlvdXJkYXRhLmlvIiwiaHR0cHM6Ly9jaGF0d2l0aHlvdXJkYXRhLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE3NzkzMDAwMDcsImV4cCI6MTc3OTMwNzIwNywic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBvZmZsaW5lX2FjY2VzcyIsImF6cCI6IlFYVHNXRGx0eVRJMVZyUkhPUVJSZlR0RzFjZjRZREs4In0.EzgMVOSkN9Cs19Vl1mojG7N3QcTe07Q21r-Wgph1KmgQJvXLSjMu7B3GzPUUCoq9B5dqq6_7rbDrzc4hz4x_yUeVctr0Pw5XIYzwCepfJdGQX0e4ZCk_uG5XTg6J9z0SEf1wMj3i_imnJ3bkKLP0gSswyA3mJyDVM53gh_Bea1dStGYrH6vxL6IlDhJ60MrPWlpyGm046JgUMJGXPRE79osfldsP5C6oa4dyB74x3QPN332OvJZf1DOAMBiuC1xcESFAR_MUtatluLf4ugsVrQIoZODs-Xa9ptf_EZCBNsI4LqGV0XiNdgajwCRAtW4o4ngsHoMGi6rLik-yTXyyFQ"
RUTA_IMAGEN = r"C:\Users\Santi\Desktop\ejerciciosss\ejercicio1.jpg"

API_KEY = os.getenv('API_KEYY')
genai.configure(api_key=API_KEY)
model_gemini = genai.GenerativeModel('gemini-flash-latest')


# 2. Inicializás el cliente de Julius
julius = Julius(api_key=TOKEN_JULIUS)

def probar_texto_julius(mensaje_ejercicio):
    print(f"2. Intentando enviar el mensaje: '{mensaje_ejercicio}'")
    
    try:
        response = julius.chat.completions.create(
            model="default",
            messages=[
                {
                    "role": "user",
                    "content": mensaje_ejercicio
                }
            ],
            advanced_reasoning=True  
        )
        
        print("3. Petición enviada. Procesando respuesta...")
        
        if not response:
            return "Error: El servidor de Julius devolvió un objeto vacío (None)."
            
        if hasattr(response, 'message') and response.message.content:
            return response.message.content
        else:
            return f"Alerta: Se conectó pero la respuesta no trae texto. Estructura recibida: {response}"

    except Exception as e:
        return f"Error crítico en la conexión: {e}"


# --- NUEVA LÓGICA DE TRANCRIPCIÓN ---
if __name__ == "__main__":
    print("1. Gemini leyendo la imagen para extraer la ecuación...")
    
    if not os.path.exists(RUTA_IMAGEN):
        print(f"Error: La imagen no existe en {RUTA_IMAGEN}")
    else:
        try:
            # Gemini abre la foto
            img = Image.open(RUTA_IMAGEN)
            
            prompt_ocr = (
                "Actúa como un OCR experto en matemáticas. Transcribe exactamente el ejercicio, "
                "ecuación o problema que aparece en la imagen a texto plano. "
                "No quiero explicaciones, introducciones, ni que lo resuelvas. SOLO el texto matemático limpio."
            )
            
            response_gemini = model_gemini.generate_content([prompt_ocr, img])
            ejercicio_en_texto = response_gemini.text.strip()
            
            print(f"-> Texto extraído de la foto: '{ejercicio_en_texto}'")
            
            # Le concatenamos el pedido de resolución para Julius
            consigna_final = f"Resuelve el siguiente ejercicio paso a paso de forma detallada: {ejercicio_en_texto}"
            
            # Se lo mandamos a tu función de Julius que anda de diez
            respuesta = probar_texto_julius(consigna_final)
            
            print("\n==================================================")
            print("Respuesta de Julius:")
            print(respuesta)
            print("==================================================")
            
        except Exception as e:
            print(f"Error en el proceso: {e}")


respuesta = probar_texto_julius("Resuelve el siguiente ejercicio: 2 + 2 * 3")
print("Respuesta de Julius:", respuesta)