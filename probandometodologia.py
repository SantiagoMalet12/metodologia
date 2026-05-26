
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
import mysql.connector
from mysql.connector import Error


prompt = (
                    "Pretende que eres un profesor de matemáticas de Harvard. Analiza este ejercicio. "
                    "Da el resultado final claramente"
                    "No quiero explicaciones, SOLO el resultado final sin decoraciones."
                )



ruta_carpeta = r"C:\Users\Santi\Desktop\ejerciciosss"
load_dotenv()
TOKEN_JULIUS = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJoM0dwdVZXd2JMMTJpYnBtamlxWCJ9.eyJodHRwczovL2NoYXR3aXRoeW91cmRhdGEuaW8vdXNlcl9lbWFpbCI6InNvbG9kaXNjb3JkamFqYUBnbWFpbC5jb20iLCJodHRwczovL2NoYXR3aXRoeW91cmRhdGEuaW8vanVsaXVzX2lkIjoiZmQ1NTEyOTQtNDRkOS00ODE0LTlmMGItNDBmMDZlNjdjYWJhIiwiaHR0cHM6Ly9jaGF0d2l0aHlvdXJkYXRhLmlvL21lcmdlZF9zdWJfaWQiOiJnb29nbGUtb2F1dGgyXzEwMjU1ODM2NzE1NTM2NDY0MzY5OCIsImh0dHBzOi8vY2hhdHdpdGh5b3VyZGF0YS5pby91c2VyX2lwIjoiMjgwMzo5ODAwOjk4YzQ6NmVkZTo0MDNhOjZkOGY6MWQ2MDoxOTA4IiwiaHR0cHM6Ly9jaGF0d2l0aHlvdXJkYXRhLmlvL3VzZXJfY291bnRyeUNvZGUiOiJBUiIsImh0dHBzOi8vY2hhdHdpdGh5b3VyZGF0YS5pby91c2VyX2NvbnRpbmVudENvZGUiOiJTQSIsImh0dHBzOi8vY2hhdHdpdGh5b3VyZGF0YS5pby9lbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaHR0cHM6Ly9jaGF0d2l0aHlvdXJkYXRhLmlvL2NyZWF0ZWRfYXQiOiIyMDI2LTA1LTIwVDE4OjAwOjA1LjA3OVoiLCJpc3MiOiJodHRwczovL2F1dGguanVsaXVzLmFpLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTAyNTU4MzY3MTU1MzY0NjQzNjk4IiwiYXVkIjpbImh0dHBzOi8vY2hhdHdpdGh5b3VyZGF0YS5pbyIsImh0dHBzOi8vY2hhdHdpdGh5b3VyZGF0YS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzc5Mzg5NTExLCJleHAiOjE3NzkzOTY3MTEsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgb2ZmbGluZV9hY2Nlc3MiLCJhenAiOiJRWFRzV0RsdHlUSTFWclJIT1FSUmZUdEcxY2Y0WURLOCJ9.GopGk3J_w5VHzRk-ie78tlEM4mWbQ6hsViM5cTVDxsVwp42Cp1rikfJOj9f1HYW5aiFoBvARLrIzjU_2gMhb5lvkOJ6lsRBAEamQvH1H4gUtYF9jEfvHrDbvj6UOlMaOspDbr_Br99wcT4IldD8iq16RYxXpm6ouqJNf96x6uNshZlJZ4N9u5HnseVSo9ie_OmJfEhAcY-dBuZXyUaaAkIV0R9XAzGba5mcwNJ43hgr2V313rkc7UpKIi2J_kQHxGQQHvP_PsW55MBXU3lg00e9m_mGQjvViJBwhWM5XO1Wov3xvcnAch_Xj7UOZaey2Ou5tMTWvUw9wJaPETBvKRg"
julius = Julius(api_key=TOKEN_JULIUS)
api_keyy = os.getenv('API_KEYY')



def emitir_ejercicio():
    try:
        # conexion
        conexion = mysql.connector.connect(
            host='localhost',         
            user='root',              
            password='12345',    
            database='tp_metodologia'       
        )


        if conexion.is_connected():
            cursor = conexion.cursor()
            query = "SELECT id, texto_ejercicio FROM ejercicio"
            cursor.execute(query)

            # fetchall() trae una lista de tuplas [(id, nombre, punt), (id, nombre, punt)]
            resultados = cursor.fetchall()

            print(f"Total de registros encontrados: {len(resultados)}\n")

            # recorrer y mostrar los datos
            for fila in resultados:
                
                id = fila[0]
                texto_ejercicio = fila[1]
                
                print(f"ID: {id} | Ejercicio: {texto_ejercicio}")
    except Error as e:
        print(f"Error al conectar o leer la base de datos: {e}")
    return resultados



def gemini_respuesta():
    lista_ejercicios = []

    conexion = mysql.connector.connect(
        host='localhost',          
        user='root',               
        password='12345',  
        database='tp_metodologia'       
    )

    
    client = genai.Client(api_key=api_keyy)
    #lectura de carpeta
    for elemento in os.listdir(ruta_carpeta):
        ruta_completa = os.path.join(ruta_carpeta, elemento)
        if os.path.isfile(ruta_completa):
            img = Image.open(ruta_completa)

            prompt_ocr = (
            "Actúa como un OCR experto en matemáticas. Transcribe exactamente el ejercicio, "
            "ecuación o problema que aparece en la imagen a texto plano. "
            "No quiero explicaciones, introducciones, ni que lo resuelvas. SOLO el texto matemático limpio."
            )
        
            
            response_gemini = client.models.generate_content(
                model='gemini-2.5-flash',  
                contents=[prompt_ocr, img]
            )


        ejercicio_en_texto = response_gemini.text.strip()
        lista_ejercicios.append(ejercicio_en_texto)
        
        #inserta texto ejercicio
        if conexion.is_connected():
            cursor = conexion.cursor()

            sql_insertar = "INSERT INTO ejercicio (texto_ejercicio) VALUES (%s)"
            valores = (
                ejercicio_en_texto,  # texto_ejercicio (TEXT)
            )
            cursor.execute(sql_insertar, valores)

            conexion.commit()
        
        
    
    return lista_ejercicios




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



def analisiscongemini():

    conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345', 
            database='tp_metodologia'
        )

    print("Trayendo ejercicios desde la base de datos para resolverlos con Gemini...")
    lista_ejercicios = emitir_ejercicio()
    
    client = genai.Client(api_key=api_keyy)



    for i in range(0, len(lista_ejercicios)):

        id_ejercicio = lista_ejercicios[i][0]
        enunciado = lista_ejercicios[i][1]
        print("Enunciado :" + enunciado)

    
        consigna_final = prompt + f" {enunciado}"
    
        try:
            
            response = client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=consigna_final
            )

            # retora el texto limpio
            resultado = response.text.strip()
            
            #inserta valores
            if conexion.is_connected():
                cursor = conexion.cursor()

                sql_insertar = "INSERT INTO resultado (idejercicio, nombreia, resultado) VALUES (%s, %s, %s)"
                valores = (id_ejercicio, "Gemini", resultado)

                cursor.execute(sql_insertar, valores)
                conexion.commit()
            

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

        response = client.chat.completions.create(
            model="qwen/qwen-2-vl-72b-instruct", 
            messages=[
                {
                    "role": "user",
                    "content": prompt_completo  
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



analisiscongemini()
