from flask import Flask, render_template, request
import requests, os, uuid, json
from dotenv import load_dotenv
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from azure.core.credentials import AzureKeyCredential
from PIL import Image
import io

load_dotenv()

app = Flask(__name__)

# Configuración de credenciales y cliente
subscription_key = os.environ.get('AZURE_COMPUTER_VISION_KEY')
endpoint = os.environ.get('AZURE_COMPUTER_VISION_ENDPOINT')

if not subscription_key or not endpoint:
    raise ValueError("No Azure Computer Vision credentials found")

computervision_client = ComputerVisionClient(endpoint, AzureKeyCredential(subscription_key))

@app.route('/computerVision', methods=['GET', 'POST'])
def computer_vision():
    if request.method == 'POST':
        # Obtener la imagen cargada
        file = request.files['image']
        image_data = file.read()

        # Convertir la imagen a un objeto de tipo BytesIO para ser procesada por el cliente
        image_stream = io.BytesIO(image_data)
        
        # Llamada al cliente de Computer Vision para generar la descripción de la imagen
        description_result = computervision_client.describe_image_in_stream(image_stream)

        # Obtener la mejor descripción
        if len(description_result.captions) > 0:
            caption = description_result.captions[0].text
        else:
            caption = "No se pudo generar una descripción."

        return render_template('computerVision.html', caption=caption, image_data=image_data)

    return render_template('computerVision.html', caption=None)

@app.route('/', methods=['GET'])
def index():
    # Ruta principal con tu lógica personalizada para la página de inicio
    return render_template('index.html')

@app.route('/pruebaTranslator')
def traductor():
    return render_template('traductor.html')

@app.route('/translate', methods=['POST'])
def translate():
    original_text = request.form['text']
    target_language = request.form['language']

    if target_language == "custom":
        custom_language = request.form['customLanguage'].strip()  # Eliminar espacios en blanco
        if custom_language:  # Solo usar si se escribió algo
            target_language = custom_language

    if not target_language:
        return "Error: No language selected", 400

    key = os.environ.get('AZURE_TRANSLATOR_KEY')
    endpoint = os.environ.get('AZURE_TRANSLATOR_ENDPOINT')
    location = os.environ.get('AZURE_TRANSLATOR_REGION')

    if not key or not endpoint or not location:
        return "Error: Missing Azure credentials", 500

    path = '/translate?api-version=3.0'
    target_language_parameter = '&to=' + target_language
    constructed_url = endpoint + path + target_language_parameter

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': original_text}]

    try:
        translator_request = requests.post(constructed_url, headers=headers, json=body)
        translator_request.raise_for_status()  # Lanza un error si la respuesta no es 200
        translator_response = translator_request.json()
        translated_text = translator_response[0]['translations'][0]['text']
    except requests.exceptions.RequestException as e:
        return f"Error en la traducción: {e}", 500

    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )

if __name__ == '__main__':
    app.run(debug=True)
