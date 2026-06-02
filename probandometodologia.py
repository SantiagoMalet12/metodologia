
import os
from urllib import response
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
TOKEN_JULIUS = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJoM0dwdVZXd2JMMTJpYnBtamlxWCJ9.eyJodHRwczovL2NoYXR3aXRoeW91cmRhdGEuaW8vdXNlcl9lbWFpbCI6InNhbnRpYWdvLm1hbGV0LjEyQGdtYWlsLmNvbSIsImh0dHBzOi8vY2hhdHdpdGh5b3VyZGF0YS5pby9qdWxpdXNfaWQiOiIwMjAxZDNmZS1jMjBiLTRlYmItYjRlNy0zZGE0M2Q4ZjdkZDQiLCJodHRwczovL2NoYXR3aXRoeW91cmRhdGEuaW8vbWVyZ2VkX3N1Yl9pZCI6Imdvb2dsZS1vYXV0aDJfMTA0NjIzNzAwNzgzMTYzOTk4Mzc5IiwiaHR0cHM6Ly9jaGF0d2l0aHlvdXJkYXRhLmlvL3VzZXJfaXAiOiIyODAzOjk4MDA6OThjNDo2ZWRlOmQ0NGU6NjI4NDo0MTBlOjNiNiIsImh0dHBzOi8vY2hhdHdpdGh5b3VyZGF0YS5pby91c2VyX2NvbnRpbmVudENvZGUiOiJTQSIsImh0dHBzOi8vY2hhdHdpdGh5b3VyZGF0YS5pby9lbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaHR0cHM6Ly9jaGF0d2l0aHlvdXJkYXRhLmlvL2NyZWF0ZWRfYXQiOiIyMDI2LTA2LTAyVDE4OjQ3OjUzLjI5NFoiLCJpc3MiOiJodHRwczovL2F1dGguanVsaXVzLmFpLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA0NjIzNzAwNzgzMTYzOTk4Mzc5IiwiYXVkIjpbImh0dHBzOi8vY2hhdHdpdGh5b3VyZGF0YS5pbyIsImh0dHBzOi8vY2hhdHdpdGh5b3VyZGF0YS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzgwNDI2MDc1LCJleHAiOjE3ODA0MzMyNzUsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgb2ZmbGluZV9hY2Nlc3MiLCJhenAiOiJRWFRzV0RsdHlUSTFWclJIT1FSUmZUdEcxY2Y0WURLOCJ9.eCnzygQI3ut0BlvE27Erh7RMCWq__FMPDMXzftpLy4E-IHI2uc2cAAjWU4F0cW313dadHp0Qm_F1pkmuMwY_s-3eWLnZt7SYFlz3ZcomUpeJ4szBI676eoDhF3VMuWH5LtiUuIY23xH-R_x0tM80gdAQz-SATR_gJSybK0Bb_FyFgthcOPquw6A4q7X9mPt2oSSvjoIbnIbxqJYWK282eHhlO5gJUtQbxS7EdwWRR6cZzY--SVIQG1NSlhlbBBNeFGhy6dzViQbGfBsvPkwwXxd97-yAE0UWNUVOxDq801FN60RLdXTF5usoGVrnZku9z5GUPTSDbzXpwepIkVKerg"
julius = Julius(api_key=TOKEN_JULIUS)
api_keyy = os.getenv('API_KEYY')



def emitir_ejercicio(id_minimo):
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
            query = "SELECT id, texto_ejercicio FROM ejercicio WHERE id > %s"
            cursor.execute(query, (id_minimo,))

            # fetchall trae una lista de tuplas
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
    for elemento in sorted(
        os.listdir(ruta_carpeta),
        key=lambda x: int(os.path.splitext(x)[0])
    ):
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

            sql_insertar = "INSERT INTO ejercicio (id, texto_ejercicio, materia) VALUES (%s, %s, %s)"

            id_ejercicio = int(os.path.splitext(elemento)[0])
            valores = (
                id_ejercicio,
                ejercicio_en_texto,
                "Analisis matematico 2"
            )
            cursor.execute(sql_insertar, valores)

            conexion.commit()
        
        
    
    return lista_ejercicios




load_dotenv()


def analisiscongptoss(var):
    api_key = os.getenv('API_KEY_LAGUNA')
    modelo = "openai/gpt-oss-120b:free"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "Script Local Metodologia"
    }

    conexion = None
    cursor = None

    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345', 
            database='tp_metodologia'
        )

        print(f"Trayendo ejercicios desde la base de datos para resolverlos con {modelo}...")
        lista_ejercicios = emitir_ejercicio(var)

        if not lista_ejercicios:
            print("No se encontraron ejercicios para procesar.")
            return
        
        cursor = conexion.cursor(buffered=True)

        for i in range(len(lista_ejercicios)):
            id_ejercicio = lista_ejercicios[i][0]
            enunciado = lista_ejercicios[i][1]
            print(f"\nProcesando ID {id_ejercicio} | Enunciado: {enunciado[:60]}...")

            consigna_final = prompt + f" {enunciado}"

            data = {
                "model": modelo,
                "messages": [
                    {
                        "role": "system",
                        "content": "Pretende que eres un profesor de matemáticas de Harvard. Analiza y resuelve el ejercicio que te van a brindar. "
                    },
                    {
                        "role": "user",
                        "content": f"Analiza y resuelve este ejercicio. Da el resultado final claramente. No quiero explicaciones, SOLO el resultado final sin decoraciones: {consigna_final}"
                    }
                ]
            }

            intentos = 0
            while intentos < 2:
                print(f"-> Llamando a OpenRouter (Intento {intentos + 1})...")
                
                try:
                    inicio = time.perf_counter()
                    
                    response = requests.post(
                        url="https://openrouter.ai/api/v1/chat/completions",
                        headers=headers,
                        data=json.dumps(data)
                    )
                    
                    fin = time.perf_counter()
                    tiempo_ejercicio = round(fin - inicio, 3)
                    
                    if response.status_code == 200:
                        resultado_json = response.json()
                        solucion = resultado_json['choices'][0]['message']['content']
                        print(f"-> Respuesta recibida con éxito en {tiempo_ejercicio}s.")

                        # Inserción en la base de datos utilizando el mismo cursor
                        try:
                            sql_insertar = "INSERT INTO resultado (idejercicio, nombreia, resultado, tiempoejercicio) VALUES (%s, %s, %s, %s)"
                            valores = (int(id_ejercicio), "GPT-OSS-120B", str(solucion), float(tiempo_ejercicio))

                            cursor.execute(sql_insertar, valores)
                            conexion.commit()
                            print(f" OK: Guardado en BD para ID {id_ejercicio}.")
                        except mysql.connector.Error as err:
                            print(f" ERROR DE MYSQL al insertar ID {id_ejercicio}: {err}")
                            conexion.rollback()
                        
                        break # Éxito: salimos del bucle de intentos para este ejercicio

                    elif response.status_code == 429:
                        print(f"El modelo {modelo} está saturado (429). Esperando 15 segundos para reintentar...")
                        time.sleep(15)
                        intentos += 1
                        continue

                    elif response.status_code == 404:
                        print(f"El modelo {modelo} tiró error 404 (No disponible). Saltando ejercicio.")
                        break 
                        
                    else:
                        print(f"Error {response.status_code} con el modelo {modelo}: {response.text}")
                        break

                except Exception as e:
                    print(f"Error de conexión en la petición para ID {id_ejercicio}: {e}")
                    break

            # Espera estándar entre diferentes ejercicios para evitar saturar tu cuota
            print("Esperando 3 segundos antes del siguiente ejercicio...")
            time.sleep(3)

    except Exception as e:
        print(f"Error crítico en la conexión o ejecución general: {e}")

    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()
            print("\nConexión a la base de datos cerrada correctamente.")



def analisiscongemini(var):

    conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345', 
            database='tp_metodologia'
        )

    print("Trayendo ejercicios desde la base de datos para resolverlos con Gemini...")
    lista_ejercicios = emitir_ejercicio(var)
    
    client = genai.Client(api_key=api_keyy)



    for i in range(0, len(lista_ejercicios)):

        id_ejercicio = lista_ejercicios[i][0]
        enunciado = lista_ejercicios[i][1]
        print("Enunciado :" + enunciado)

    
        consigna_final = prompt + f" {enunciado}"
    
        try:

            inicio = time.perf_counter()
            
            response = client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=consigna_final
            )

            fin = time.perf_counter()

            tiempo_ejercicio = round(fin - inicio, 3)

            # retora el texto limpio
            resultado = response.text.strip()
            
            #inserta valores
            if conexion.is_connected():
                cursor = conexion.cursor()

                sql_insertar = "INSERT INTO resultado (idejercicio, nombreia, resultado, tiempoejercicio) VALUES (%s, %s, %s, %s)"
                valores = (id_ejercicio, "Gemini", resultado, tiempo_ejercicio)

                cursor.execute(sql_insertar, valores)
                conexion.commit()
            

        except Exception as e:
            print(f"Error al procesar el ejercicio: {e}")
            return None




def analisisconqwenmath(var):
    OPENROUTER_KEY = os.getenv('API_KEY_LAGUNA') 

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_KEY,
    )

    conexion = None
    cursor = None

    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345', 
            database='tp_metodologia'
        )

        print("Trayendo ejercicios desde la base de datos para resolverlos con Qwen-Math...")
        lista_ejercicios = emitir_ejercicio(var)

        if not lista_ejercicios:
            print("No se encontraron ejercicios para procesar.")
            return
        
        cursor = conexion.cursor(buffered=True)

        for i in range(len(lista_ejercicios)):
            id_ejercicio = lista_ejercicios[i][0]
            enunciado = lista_ejercicios[i][1]
            print(f"\nProcesando ID {id_ejercicio} | Enunciado: {enunciado[:60]}...")

            consigna_final = prompt + f" {enunciado}"

            # ESTE TRY DEBE ESTAR ADENTRO DEL FOR
            try:
                inicio = time.perf_counter()

                response = client.chat.completions.create(
                    model="qwen/qwen-2-vl-72b-instruct", 
                    messages=[
                        {
                            "role": "user",
                            "content": consigna_final 
                        }
                    ]
                )

                fin = time.perf_counter()
                tiempo_ejercicio = round(fin - inicio, 3)
                
                solucion = response.choices[0].message.content
                print(f"-> Respuesta recibida con éxito en {tiempo_ejercicio}s.")

                try:
                    sql_insertar = "INSERT INTO resultado (idejercicio, nombreia, resultado, tiempoejercicio) VALUES (%s, %s, %s, %s)"
                    # Corregido "Julius" por "Qwen-Math"
                    valores = (int(id_ejercicio), "Qwen-Math", str(solucion), float(tiempo_ejercicio))

                    cursor.execute(sql_insertar, valores)
                    conexion.commit()
                    print(f" OK: Guardado en BD para ID {id_ejercicio}.")

                except mysql.connector.Error as err:
                    print(f" ERROR DE MYSQL al insertar ID {id_ejercicio}: {err}")
                    conexion.rollback()

            except Exception as e:
                print(f"Error en la petición OpenRouter para ID {id_ejercicio}: {e}")

            # Pausa para evitar bloqueos por límite de peticiones (Rate Limit)
            print("Esperando 3 segundos antes del siguiente ejercicio...")
            time.sleep(3)

    except Exception as e:
        print(f"Error crítico en la conexión o ejecución: {e}")

    finally:
        # Aseguramos el cierre de conexiones siempre
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()
            print("\nConexión a la base de datos cerrada correctamente.")


def probar_texto_julius(var):
    conexion = None
    cursor = None
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345', 
            database='tp_metodologia'
        )
        
        print("Trayendo ejercicios desde la base de datos para resolverlos con Julius...")
        lista_ejercicios = emitir_ejercicio(var)
        
        if not lista_ejercicios:
            print("No se encontraron ejercicios para procesar.")
            return

        # Usamos buffered=True para mantener los datos en memoria si es necesario
        cursor = conexion.cursor(buffered=True)

        for i in range(len(lista_ejercicios)):
            id_ejercicio = lista_ejercicios[i][0]
            enunciado = lista_ejercicios[i][1]
            print(f"\nProcesando ID {id_ejercicio} | Enunciado: {enunciado[:60]}...")

            consigna_final = prompt + f" {enunciado}"

            try:
                inicio = time.perf_counter()
                
                response = julius.chat.completions.create(
                    model="default",
                    messages=[
                        {
                            "role": "user",
                            "content": consigna_final
                        }
                    ]
                )
                
                if response and hasattr(response, 'message') and response.message.content:
                    fin = time.perf_counter()
                    tiempo_ejercicio = round(fin - inicio, 3)
                    resultado = response.message.content
                    print(f"-> Respuesta recibida con éxito en {tiempo_ejercicio}s.")
                    
                    try:
                        # REUTILIZAMOS EL CURSOR PRINCIPAL
                        sql_insertar = "INSERT INTO resultado (idejercicio, nombreia, resultado, tiempoejercicio) VALUES (%s, %s, %s, %s)"
                        valores = (int(id_ejercicio), "Julius", str(resultado), float(tiempo_ejercicio))

                        cursor.execute(sql_insertar, valores)
                        conexion.commit()
                        print(f" OK: Guardado en BD para ID {id_ejercicio}.")

                    except mysql.connector.Error as err:
                        print(f" ERROR DE MYSQL al insertar ID {id_ejercicio}: {err}")
                        conexion.rollback()
                else:
                    print(f"Alerta: Julius no devolvió texto para el ID {id_ejercicio}.")

            except Exception as e:
                print(f"Error procesando ID {id_ejercicio}: {e}")
            
            print("Esperando 5 segundos antes del siguiente ejercicio...")
            time.sleep(15)

    except Exception as e:
        print(f"Error crítico en la conexión o ejecución: {e}")
        
    finally:
        # Cierre seguro de la conexión y el único cursor
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()
            print("\nConexión a la base de datos cerrada correctamente.")



analisiscongemini(62)
