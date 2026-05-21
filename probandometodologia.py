
import os
import requests
import json
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
from google import genai


load_dotenv()

RUTA_IMAGEN = r"C:\Users\Santi\Desktop\ejerciciosss\ejercicio2.jpg"
TOKEN_JULIUS = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJoM0dwdVZXd2JMMTJpYnBtamlxWCJ9.eyJodHRwczovL2NoYXR3aXRoeW91cmRhdGEuaW8vdXNlcl9lbWFpbCI6InNvbG9kaXNjb3JkamFqYUBnbWFpbC5jb20iLCJodHRwczovL2NoYXR3aXRoeW91cmRhdGEuaW8vanVsaXVzX2lkIjoiZmQ1NTEyOTQtNDRkOS00ODE0LTlmMGItNDBmMDZlNjdjYWJhIiwiaHR0cHM6Ly9jaGF0d2l0aHlvdXJkYXRhLmlvL21lcmdlZF9zdWJfaWQiOiJnb29nbGUtb2F1dGgyXzEwMjU1ODM2NzE1NTM2NDY0MzY5OCIsImh0dHBzOi8vY2hhdHdpdGh5b3VyZGF0YS5pby91c2VyX2lwIjoiMjgwMzo5ODAwOjk4YzQ6NmVkZTo0MDNhOjZkOGY6MWQ2MDoxOTA4IiwiaHR0cHM6Ly9jaGF0d2l0aHlvdXJkYXRhLmlvL3VzZXJfY291bnRyeUNvZGUiOiJBUiIsImh0dHBzOi8vY2hhdHdpdGh5b3VyZGF0YS5pby91c2VyX2NvbnRpbmVudENvZGUiOiJTQSIsImh0dHBzOi8vY2hhdHdpdGh5b3VyZGF0YS5pby9lbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaHR0cHM6Ly9jaGF0d2l0aHlvdXJkYXRhLmlvL2NyZWF0ZWRfYXQiOiIyMDI2LTA1LTIwVDE4OjAwOjA1LjA3OVoiLCJpc3MiOiJodHRwczovL2F1dGguanVsaXVzLmFpLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTAyNTU4MzY3MTU1MzY0NjQzNjk4IiwiYXVkIjpbImh0dHBzOi8vY2hhdHdpdGh5b3VyZGF0YS5pbyIsImh0dHBzOi8vY2hhdHdpdGh5b3VyZGF0YS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzc5Mzg5NTExLCJleHAiOjE3NzkzOTY3MTEsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgb2ZmbGluZV9hY2Nlc3MiLCJhenAiOiJRWFRzV0RsdHlUSTFWclJIT1FSUmZUdEcxY2Y0WURLOCJ9.GopGk3J_w5VHzRk-ie78tlEM4mWbQ6hsViM5cTVDxsVwp42Cp1rikfJOj9f1HYW5aiFoBvARLrIzjU_2gMhb5lvkOJ6lsRBAEamQvH1H4gUtYF9jEfvHrDbvj6UOlMaOspDbr_Br99wcT4IldD8iq16RYxXpm6ouqJNf96x6uNshZlJZ4N9u5HnseVSo9ie_OmJfEhAcY-dBuZXyUaaAkIV0R9XAzGba5mcwNJ43hgr2V313rkc7UpKIi2J_kQHxGQQHvP_PsW55MBXU3lg00e9m_mGQjvViJBwhWM5XO1Wov3xvcnAch_Xj7UOZaey2Ou5tMTWvUw9wJaPETBvKRg"
julius = Julius(api_key=TOKEN_JULIUS)
api_keyy = os.getenv('API_KEYY')

prompt = (
                    "Pretende que eres un profesor de matemáticas de Harvard. Analiza este ejercicio. "
                    "Da el resultado final claramente"
                    "No quiero explicaciones, SOLO el resultado final sin decoraciones."
                )



def gemini_respuesta():

    # 1. Inicializás el cliente pasando tu API key customizada desde las variables de entorno
    # (Si tu variable se llamara GEMINI_API_KEY, el cliente la tomaría automáticamente sin pasarle parámetros)
    client = genai.Client(api_key=api_keyy)
    
    # 2. Abrís la imagen
    img = Image.open(RUTA_IMAGEN)
                
    prompt_ocr = (
        "Actúa como un OCR experto en matemáticas. Transcribe exactamente el ejercicio, "
        "ecuación o problema que aparece en la imagen a texto plano. "
        "No quiero explicaciones, introducciones, ni que lo resuelvas. SOLO el texto matemático limpio."
    )
    
    # 3. Llamás al modelo usando la estructura del nuevo SDK
    response_gemini = client.models.generate_content(
        model='gemini-2.5-flash',  # El modelo recomendado para estas tareas
        contents=[prompt_ocr, img]
    )
    
    ejercicio_en_texto = response_gemini.text.strip()
    
    return ejercicio_en_texto





load_dotenv()
def resolver_ejercicio_laguna(prompt_ejercicio):
    api_key = os.getenv('API_KEY_LAGUNA')
    modelo="openai/gpt-oss-120b:free"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "Script Local Metodologia"
    }

    intentos = 0
    # 2 intentos por si salta el error de limite de peticiones
    while intentos < 2:
        print(f"Resolviendo ejercicio con: {modelo} (Intento {intentos + 1})...")
        
        data = {
            "model": modelo,
            "messages": [
                {
                    "role": "system",
                    "content": "Pretende que eres un profesor de matemáticas de Harvard. Analiza y resuelve el ejercicio que te van a brindar. "
                },
                {
                    "role": "user",
                    "content": f"Analiza y resuelve este ejercicio. Da el resultado final claramente. No quiero explicaciones, SOLO el resultado final sin decoraciones: {prompt_ejercicio}"
                }
            ]
        }
        
        try:
            # empiezo el temporizador antes de enviar la peticion
            tiempo_inicio = time.time()
            
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                data=json.dumps(data)
            )
            
            tiempo_final = time.time()
            segundos_transcurridos = tiempo_final - tiempo_inicio
            
            # si la respuesta es exitosa
            if response.status_code == 200:
                resultado = response.json()
                respuesta_texto = resultado['choices'][0]['message']['content']
                # .2f es para formatear a 2 decimales
                print(f"Tiempo de respuesta: {segundos_transcurridos:.2f} segundos.")
                print(respuesta_texto)
                return respuesta_texto
            
            #si esta saturado
            elif response.status_code == 429:
                print(f"el modelo {modelo} esta saturado (429). Esperando 15 segundos para reintentar...")
                time.sleep(15)
                intentos += 1
                continue
            
            # si esta caido
            elif response.status_code == 404:
                print(f"El modelo {modelo} tiro error 404 (No disponible).")
                break 
                
            else:
                print(f"Error {response.status_code} con el modelo {modelo}: {response.text}")
                break
                    
        except Exception as e:
            print(f"Error de conexión: {e}")
            break

    print("No se pudo obtener respuesta de ningún modelo.")
    return None



def analisiscongemini(enunciado):
    
    client = genai.Client(api_key=api_keyy)

    print(f"-> Gemini extrajo el siguiente texto: '{enunciado}'")
    consigna_final = prompt + f" {enunciado}"
    
    try:
        


        # Corregido: Usamos 'client.models.generate_content' y le pasamos el modelo que uses (ej: 'gemini-2.5-flash')
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=consigna_final
        )

        # Retornamos o imprimimos el resultado limpio
        resultado = response.text.strip()
        print(resultado)
        

    except Exception as e:
        print(f"Error al procesar el ejercicio: {e}")
        return None




def analisisconqwenmath(ejercicio):
    

    OPENROUTER_KEY = os.getenv('API_KEY_LAGUNA')    
    

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_KEY,
    )


    try:
        
        prompt_completo = (
            "Pretende que eres un profesor de matemáticas de Harvard. Analiza este ejercicio matemático. "
            f"El ejercicio es: {ejercicio}. "
            "Da el resultado final claramente como RESULTADO QWEN-MATH: [valor]. "
            "No quiero explicaciones, SOLO el resultado final sin decoraciones."
        )

        # 2. Simplificamos los mensajes a puro texto (Sin 'image_url')
        response = client.chat.completions.create(
            model="qwen/qwen-2-vl-72b-instruct", 
            messages=[
                {
                    "role": "user",
                    "content": prompt_completo  # <-- Pasamos el texto directo aquí
                }
            ]
        )
        
        solucion = response.choices[0].message.content
        print(solucion)
        return solucion

    except Exception as e:
        print(f"error" + str(e))



def probar_texto_julius(enunciado):
    
    print(f"-> Gemini extrajo el siguiente texto: '{enunciado}'")
    consigna_final = prompt + f" {enunciado}"
    
    print(f"2. Intentando enviar el mensaje: '{enunciado}' a Julius para resolverlo...")

    try:
        response = julius.chat.completions.create(
            model="default",
            messages=[
                {
                    "role": "user",
                    "content": consigna_final
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




analisisconqwenmath(gemini_respuesta())
analisiscongemini(gemini_respuesta())
           
