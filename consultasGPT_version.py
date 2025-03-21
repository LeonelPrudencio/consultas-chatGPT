#!/usr/bin/env python3

"""
Este script hace web scraping utilizando selenium y guarda los datos en JSON.
Autor: Leonel Antonio Prudencio
Fecha: 2025-02-07
Versión: 2.4
"""

import undetected_chromedriver as uc
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pandas as pd
import json
import re
from datetime import datetime


###############################################################################
# Función para realizar n consultas (la misma consulta)
###############################################################################
def chat_gpt_consultas(consulta, n):
    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    1.- Abriendo navegador e ingresando credenciales de usuario
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    # Crear el DataFrame vacío para almacenar los resultados
    resultados_df = pd.DataFrame(columns=['timestamp', 'consulta', 'response', 'chatgpt_version'])

    # Crear un User-Agent aleatorio
    ua = UserAgent()
    user_agent = ua.random
    print(f"Usando User-Agent: {user_agent}")
    
    # Configurar opciones del navegador
    options = uc.ChromeOptions()
    options.add_argument(f'--user-agent={user_agent}')
    options.add_argument("--disable-notifications")
    
    # Usar la versión no detectable de Chrome
    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 30)
    
    # Navegar a ChatGPT
    print("--> Abriendo navegador...")
    driver.get("https://chat.openai.com")
    
    # El usuario ingresa sus credenciales y luego debe dar enter en la consola
    print(">>> Navegador abierto. Por favor, inicia sesión manualmente.")
    print(">>> Cuando estés listo para continuar, presiona Enter en la consola.")
    
    # Esperar a que el usuario indique que está listo
    input()
    
    # Inicializando las variables a extraer
    respuesta_text = ""
    chatgpt_version = "desconocido"

    for i in range(n):
        # Consulta que queremos realizar
        print(f"\n--> Realizando consulta principal: '{i+1}'")

        try:
            """
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            2.- Consulta principal
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            """
            # Identificando el área del prompt
            textarea = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='prompt-textarea']")))

            # Hacer clic en el área de texto
            textarea.click()
            time.sleep(2)
                
            # Enviar la consulta principal
            textarea.send_keys(consulta)
            time.sleep(3)
            textarea.send_keys(Keys.ENTER)
            print("--> Consulta principal enviada. Esperando respuesta...")
                
            # Esperar un tiempo para que se cargue inicialmente la respuesta
            time.sleep(15)

            """
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            3.- Consulta para versión de chatGPT
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            """
            # Ahora, preguntar por la versión del modelo
            print("--> Preguntando por la versión del modelo...")

            # Limpiar el área de texto si es necesario
            textarea.clear()

            # Hacer clic en el área de texto
            textarea.click()
            time.sleep(2)
                
            # Enviar la consulta principal
            textarea.send_keys("¿Qué versión de ChatGPT usaste para la respuesta anterior? chatGPT-4-turbo, chatGPT-4 o chatGPT-3.5, solo indica la versión")
            time.sleep(3)
            textarea.send_keys(Keys.ENTER)
            print("--> Consulta sobre la versión enviada. Esperando respuesta...")
                    
            # Esperar a que aparezca la respuesta sobre la versión
            time.sleep(10)

            """
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            4.- Almacenando respuestas
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            """
            print("--> Almacenando respuestas...")

            # Identificando el lugar de las respuestas
            #respuesta = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'markdown')]")))
            respuesta = driver.find_elements(By.CSS_SELECTOR, 'div.markdown.prose.w-full.break-words.dark\\:prose-invert.dark')

            # Respuesta principal
            respuesta_text = respuesta[0].text

            # Versión del chatGPT utilizada
            chatgpt_version = respuesta[1].text

            # Agregar los datos al DataFrame
            nueva_fila = {
                'timestamp': datetime.now().isoformat(),
                'consulta': consulta,
                'response': respuesta_text,
                'chatgpt_version': chatgpt_version
            }
            
            # Guardando respuesta en el data frame
            resultados_df = pd.concat([resultados_df, pd.DataFrame([nueva_fila])], ignore_index=True)
            guardar_df_a_json(resultados_df)

            print(f"--> Datos de la consulta {i+1} agregados al DataFrame y al JSON")
        
        except Exception as e:
            print(f"Error al realizar la consulta: {e}")
            # Agregar los datos que tengamos hasta ahora al DataFrame
            if respuesta_text:
                nueva_fila = {
                    'timestamp': datetime.now().isoformat(),
                    'consulta': consulta,
                    'response': respuesta_text,
                    'chatgpt_version': chatgpt_version
                }

                resultados_df = pd.concat([resultados_df, pd.DataFrame([nueva_fila])], ignore_index=True)
                guardar_df_a_json(resultados_df)

                print(f"--> Datos de la consulta {i+1} agregados al DataFrame y al JSON")

        """
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        5.- Nueva consulta
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        """
        # Esperar a que el elemento sea clickeable y hacer clic usando data-testid
        boton_nuevo_chat = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='create-new-chat-button']")))
        boton_nuevo_chat.click()
        time.sleep(2)

        # Se abre un nuevo chat y se realiza la misma consulta

    """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    6.- Guardar todos los resultados en un archivo JSON
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """
    print("--> Guardando todos los resultados en un data frame")

    # Guardando en un archivo json
    guardar_df_a_json(resultados_df, "chatGPT_respuestas_respaldo.json")
    
    print(">>> El navegador permanecerá abierto. Para salir, presiona Ctrl+C en la consola.")
    # Mantener el navegador abierto
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(">>> Cerrando el navegador...")
        driver.quit()


###############################################################################
# Función para guardar los resultados en un json
###############################################################################
def guardar_df_a_json(resultados_df, nombre_archivo='chatGPT_respuestas.json'):
    # Verificar si el archivo ya existe
    if os.path.exists(nombre_archivo):
        # Cargar el contenido existente del archivo JSON
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            datos_existentes = json.load(archivo)
    else:
        # Si el archivo no existe, inicializar una lista vacía
        datos_existentes = []

    # Convertir el DataFrame a una lista de diccionarios
    nuevos_datos = resultados_df.to_dict(orient='records')

    # Agregar los nuevos datos a los existentes
    datos_existentes.extend(nuevos_datos)

    # Guardar la lista combinada de nuevo en el archivo JSON
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        json.dump(datos_existentes, archivo, ensure_ascii=False, indent=4)
    
    print(f"--> Datos guardados en el archivo: {nombre_archivo}")



if __name__ == "__main__":
    # Instalar dependencias si no están instaladas
    try:
        import undetected_chromedriver
        import fake_useragent
        from selenium.webdriver.common.by import By
        import re
    except ImportError:
        print("Instalando dependencias necesarias...")
        os.system("pip install undetected-chromedriver fake-useragent selenium")
        print("Dependencias instaladas.")
    
    chat_gpt_consultas( "Dame 10 ejercicios de polinomios", 25)
