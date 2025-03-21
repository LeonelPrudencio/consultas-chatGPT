# consultas-chatGPT

# Automatización de Consultas a ChatGPT

## Descripción General
Este repositorio contiene un script en Python que automatiza múltiples consultas a ChatGPT, recopilando y almacenando las respuestas en un archivo JSON. El script está diseñado con fines de investigación, permitiéndote enviar la misma consulta varias veces y analizar la variación en las respuestas.

## Características
- Automatiza múltiples consultas idénticas a ChatGPT
- Captura las respuestas de ChatGPT
- Identifica automáticamente qué versión de ChatGPT fue utilizada (GPT-3.5, GPT-4, etc.)
- Almacena todos los resultados de las consultas en un archivo JSON estructurado
- Utiliza automatización de navegador no detectable para evitar bloqueos
- Emplea agentes de usuario aleatorios para cada sesión

## Requisitos
- Python 3.6 o superior
- Navegador Chrome instalado
- Conexión a Internet
- Cuenta de OpenAI ChatGPT

## Dependencias
El script requiere los siguientes paquetes de Python:
- `undetected_chromedriver`: Para automatización del navegador que evita la detección
- `fake_useragent`: Para generar agentes de usuario aleatorios
- `selenium`: Para interacción con el navegador web
- `pandas`: Para manipulación y almacenamiento de datos
- `re`: Para expresiones regulares (parte de la biblioteca estándar de Python)

## Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/tunombredeusuario/automatizacion-chatgpt.git
cd automatizacion-chatgpt
```

2. Instala las dependencias requeridas:
```bash
pip install undetected-chromedriver fake-useragent selenium pandas
```

Alternativamente, el script intentará instalar las dependencias requeridas si no están ya presentes.

## Uso

1. Ejecuta el script:
```bash
python chatgpt_automation.py
```

2. Cuando el navegador Chrome se abra, inicia sesión manualmente en tu cuenta de ChatGPT
   - El script se pausará y esperará a que completes este paso

3. Después de iniciar sesión, presiona Enter en la consola para comenzar las consultas automatizadas

4. El script:
   - Enviará tu consulta a ChatGPT
   - Esperará una respuesta
   - Preguntará a ChatGPT qué versión fue utilizada
   - Almacenará los resultados
   - Abrirá un nuevo chat y repetirá el proceso

5. Los resultados se guardan en `chatGPT_respuestas.json` con una copia de respaldo en `chatGPT_respuestas_respaldo.json`

6. Para detener el script, presiona Ctrl+C en la consola

## Personalización

Para cambiar la consulta o el número de iteraciones, modifica la llamada de función al final del script:

```python
chat_gpt_consultas("Tu consulta aquí", numero_de_iteraciones)
```

Por ejemplo, la configuración actual ejecuta 25 iteraciones con la consulta "Dame 10 ejercicios de polinomios".

## Formato de Salida

El archivo JSON de salida contiene un array de objetos con la siguiente estructura:

```json
[
    {
        "timestamp": "2025-02-07T14:30:45.123456",
        "consulta": "Dame 10 ejercicios de polinomios",
        "response": "1. Factoriza el siguiente polinomio: x² - 9...",
        "chatgpt_version": "GPT-4"
    },
    ...
]
```

## Notas Importantes

- El script requiere inicio de sesión manual en ChatGPT debido a las medidas de seguridad de OpenAI
- El navegador Chrome permanecerá abierto hasta que termines manualmente el script
- La automatización excesiva podría violar los términos de servicio de OpenAI, úsalo responsablemente
- El script utiliza WebDriverWait con un tiempo de espera de 30 segundos; ajústalo si es necesario para conexiones más lentas

## Autor
Leonel Antonio Prudencio Castro

## Versión
2.4 (2025-02-07)
