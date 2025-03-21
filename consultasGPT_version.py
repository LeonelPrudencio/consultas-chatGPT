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
import json
import re
from datetime import datetime

def open_chatgpt_and_query(consulta, n):
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
    print("Abriendo navegador...")
    driver.get("https://chat.openai.com")
    
    print("Navegador abierto. Por favor, inicia sesión manualmente.")
    print("Cuando estés listo para continuar, presiona Enter en la consola.")
    
    # Esperar a que el usuario indique que está listo
    input()
    
    # Consulta que queremos realizar
    query = consulta
    print(f"Realizando consulta principal: '{query}'")
    
    response_text = ""
    chatgpt_version = "Versión desconocida"
    
    try:
        # Intentar diferentes selectores para el área de texto
        textarea_selectors = [
            "//div[@id='prompt-textarea']", 
            "//div[contains(@class, 'ProseMirror')]",
            "//div[@contenteditable='true']",
            "//div[contains(@placeholder, 'Pregunta lo que quieras')]",
            "//div[contains(@data-placeholder, 'Pregunta lo que quieras')]"
        ]
        
        textarea = None
        for selector in textarea_selectors:
            try:
                textarea = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                print(f"Área de texto encontrada con selector: {selector}")
                break
            except:
                print(f"Selector no encontrado: {selector}")
                continue
        
        if textarea:
            # Hacer clic en el área de texto
            textarea.click()
            time.sleep(1)
            
            # Enviar la consulta principal
            textarea.send_keys(query)
            time.sleep(1)
            textarea.send_keys(Keys.ENTER)
            print("Consulta principal enviada. Esperando respuesta...")
            
            # Esperar un tiempo para que se cargue inicialmente la respuesta
            time.sleep(5)
            
            # Esperar a que aparezca la respuesta (buscar un elemento que contenga la respuesta de ChatGPT)
            response_selectors = [
                "//div[contains(@class, 'markdown')]",
                "//div[contains(@class, 'message-content')]",
                "//div[contains(@data-message-author-role, 'assistant')]",
                "//div[contains(@class, 'assistant')]//div[contains(@class, 'text-message')]"
            ]
            
            response_element = None
            for selector in response_selectors:
                try:
                    # Esperar a que el elemento de respuesta esté presente y visible
                    response_element = wait.until(EC.visibility_of_element_located((By.XPATH, selector)))
                    print(f"Elemento de respuesta encontrado con selector: {selector}")
                    break
                except:
                    print(f"Selector de respuesta no encontrado: {selector}")
                    continue
            
            # Esperar a que la respuesta se complete (ChatGPT puede tardar en generar la respuesta completa)
            # Este tiempo puede necesitar ajustes según la longitud de la respuesta esperada
            time.sleep(15)
            
            if response_element:
                # Obtener el texto de la respuesta
                response_text = response_element.text
                print("Respuesta principal obtenida correctamente.")
                
                # Ahora, preguntar por la versión del modelo
                print("Preguntando por la versión del modelo...")
                
                # Limpiar el área de texto si es necesario
                try:
                    textarea.clear()
                except:
                    # Si no se puede limpiar, buscar el área de texto nuevamente
                    for selector in textarea_selectors:
                        try:
                            textarea = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                            break
                        except:
                            continue
                
                # Hacer clic en el área de texto nuevamente
                textarea.click()
                time.sleep(1)
                
                # Enviar la consulta para averiguar la versión
                version_query = "¿Qué versión de ChatGPT usaste para la respuesta anterior?"
                textarea.send_keys(version_query)
                time.sleep(1)
                textarea.send_keys(Keys.ENTER)
                print("Consulta de versión enviada. Esperando respuesta...")
                
                # Esperar a que aparezca la respuesta sobre la versión
                time.sleep(10)
                
                # Buscar la respuesta sobre la versión (el último mensaje del asistente)
                version_response_selectors = [
                    "//div[contains(@class, 'markdown')]",
					"//div[contains(@class, 'message-content')]",
					"//div[contains(@data-message-author-role, 'assistant')]",
					"//div[contains(@class, 'assistant')]//div[contains(@class, 'text-message')]"
					]
                
                version_response_element = None
                for selector in version_response_selectors:
                    try:
                        version_response_element = wait.until(EC.visibility_of_element_located((By.XPATH, selector)))
                        break
                    except:
                        continue
                
                if version_response_element:
                    version_response_text = version_response_element.text
                    print("Respuesta de versión obtenida.")
                    
                    # Buscar la versión en la respuesta
                    chatgpt_version = version_response_text
                    print(f"Versión detectada: {chatgpt_version}")
                else:
                    print("No se pudo obtener la respuesta sobre la versión.")
            else:
                print("No se pudo encontrar el elemento que contiene la respuesta principal.")
        else:
            print("No se pudo encontrar el área de texto para enviar la consulta.")
        
        # Guardar la consulta y la respuesta en un archivo JSON
        save_to_json(query, response_text, chatgpt_version)
    
    except Exception as e:
        print(f"Error al realizar la consulta: {e}")
        # Intentar guardar lo que tengamos hasta ahora
        if response_text:
            save_to_json(query, response_text, chatgpt_version)
    
    print("El navegador permanecerá abierto. Para salir, presiona Ctrl+C en la consola.")
    
    # Mantener el navegador abierto
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Cerrando el navegador...")
        driver.quit()


def save_to_json(query, response, chatgpt_version):
    """
    Guarda la consulta, la respuesta y la versión de ChatGPT en un archivo JSON
    """
    # Crear un nombre de archivo basado en la fecha y hora
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chatgpt_respuestas.json"
    
    # Crear el diccionario de datos
    data = {
        "timestamp": datetime.now().isoformat(),
        "chatgpt_version": chatgpt_version,
        "query": query,
        "response": response
    }
    
    # Guardar los datos en el archivo JSON
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"Datos guardados en el archivo: {filename}")

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
    
    open_chatgpt_and_query( "Dame 10 ejercicios de polinomios", 1)
