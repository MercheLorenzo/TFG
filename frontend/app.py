from flask import Flask, render_template, request, send_file, redirect, url_for, session
import requests, os, uuid, json
from dotenv import load_dotenv
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from azure.core.credentials import AzureKeyCredential
from msrest.authentication import CognitiveServicesCredentials
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from PIL import Image
import io
from uuid import uuid4
from pymongo import MongoClient
from datetime import datetime
import bcrypt
import re

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')
 
#@app.route('/', methods=['GET'])
#def index():
    # Ruta principal con tu lógica personalizada para la página de inicio
    #return render_template('index.html')

@app.route('/translator')
def traductor():
    return render_template('traductor.html')

@app.route('/translate', methods=['POST'])
def translate():
    if not session.get('usuario'):
        return redirect(url_for('login'))  # Solo usuarios logueados pueden traducir y guardar

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

     # 🧠 Guardar en la base de datos
    traducciones = db['traducciones']
    traducciones.insert_one({
        "usuario": session['usuario'],
        "original": original_text,
        "traducido": translated_text,
        "idioma_destino": target_language,
        "fecha": datetime.utcnow()
    })

    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )

# Nueva ruta para mostrar el formulario
@app.route('/vision', methods=['GET'])
def vision():
    return render_template('vision.html')

# Nueva ruta para procesar la imagen
@app.route('/describe-image', methods=['POST'])
def describe_image():
    image_file = request.files['image']

    if not image_file:
        return "No se subió ninguna imagen", 400

    # Azure credentials
    vision_key = os.environ.get('AZURE_COMPUTER_VISION_KEY')
    vision_endpoint = os.environ.get('AZURE_COMPUTER_VISION_ENDPOINT')

    if not vision_key or not vision_endpoint:
        return "Error: Faltan credenciales de Azure", 500

    computervision_client = ComputerVisionClient(
        vision_endpoint,
        CognitiveServicesCredentials(vision_key)
    )

    image_data = image_file.read()

    try:
        description_result = computervision_client.describe_image_in_stream(
            io.BytesIO(image_data),
            max_candidates=1,
            language="es"  # Puedes cambiar a "en" para inglés
        )

        if not description_result.captions:
            description = "No se pudo generar una descripción."
        else:
            description = description_result.captions[0].text

    except Exception as e:
        return f"Error al describir la imagen: {e}", 500

    # Después de obtener la descripción
    descripciones = db['descripciones_imagen']
    descripciones.insert_one({
        "usuario": session['usuario'],
        "descripcion": description,
        "fecha": datetime.utcnow()
    })

    return render_template('vision.html', description=description)

# Ruta para mostrar el formulario
@app.route('/sentiment', methods=['GET'])
def sentiment():
    return render_template('sentiment.html')

# Ruta para procesar el texto y analizar el sentimiento
@app.route('/analyze-sentiment', methods=['POST'])
def analyze_sentiment():
    text = request.form['text']

    if not text:
        return "Error: No se proporcionó texto", 400

    # Azure credentials
    text_analytics_key = os.environ.get('AZURE_TEXT_ANALYTICS_KEY')
    text_analytics_endpoint = os.environ.get('AZURE_TEXT_ANALYTICS_ENDPOINT')

    if not text_analytics_key or not text_analytics_endpoint:
        return "Error: Faltan credenciales de Azure", 500

    text_analytics_client = TextAnalyticsClient(
        endpoint=text_analytics_endpoint,
        credential=AzureKeyCredential(text_analytics_key)
    )

    documents = [text]

    try:
        response = text_analytics_client.analyze_sentiment(documents=documents)[0]

        sentiment_en = response.sentiment  # Puede ser 'positive', 'neutral', 'negative'

        traducciones = {
            'positive': 'positivo',
            'neutral': 'neutro',
            'negative': 'negativo'
        }

        sentiment = traducciones.get(sentiment_en, 'desconocido')

    except Exception as e:
        return f"Error al analizar el sentimiento: {e}", 500

    # Después de obtener el sentimiento
    sentimientos = db['sentimientos']
    sentimientos.insert_one({
        "usuario": session['usuario'],
        "texto": text,
        "sentimiento": sentiment,
        "fecha": datetime.utcnow()
    })

    return render_template('sentiment.html', sentiment=sentiment)

# Ruta para cargar la página de carga de imagen
@app.route('/face', methods=['GET'])
def face():
    return render_template('face.html')

@app.route('/detect-faces', methods=['POST'])
def detect_faces():
    image_file = request.files['image']

    if not image_file:
        return "Error: No se subió ninguna imagen", 400

    face_api_key = os.environ.get('AZURE_FACE_API_KEY')
    face_api_endpoint = os.environ.get('AZURE_FACE_API_ENDPOINT')

    if not face_api_key or not face_api_endpoint:
        return "Error: Faltan credenciales de Azure", 500

    headers = {
        'Ocp-Apim-Subscription-Key': face_api_key,
        'Content-Type': 'application/octet-stream'
    }

    # Leer imagen
    image_data = image_file.read()

    # Detectar rostros
    try:
        response = requests.post(
            f"{face_api_endpoint}/face/v1.0/detect",
            headers=headers,
            params={'detectionModel': 'detection_01'},  # detection_01 o detection_03
            data=image_data
        )
        response.raise_for_status()
        faces = response.json()

    except requests.exceptions.RequestException as e:
        return f"Error al detectar rostros: {e}", 500

    # Guardar temporalmente la imagen para mostrarla
    image_path = os.path.join('static', 'uploaded_image.jpg')
    with open(image_path, 'wb') as f:
        f.write(image_data)

    image_url = '/' + image_path  # ruta relativa para mostrarla en el navegador

    # Justo después de obtener la lista de caras
    caras = db['caras_detectadas']
    caras.insert_one({
        "usuario": session['usuario'],
        "num_caras": len(faces),
        "detalles": faces,
        "fecha": datetime.utcnow()
    })

    return render_template('face.html', faces=faces, image_url=image_url)


# Diccionario de idiomas: código -> (nombre en español, nombre en inglés)
IDIOMAS = {
    "es": ("español", "Spanish"),
    "en": ("inglés", "English"),
    "fr": ("francés", "French"),
    "de": ("alemán", "German"),
    "it": ("italiano", "Italian"),
    "pt": ("portugués", "Portuguese"),
    "ru": ("ruso", "Russian"),
    "zh": ("chino", "Chinese"),
    "zh-Hans": ("chino", "Chinese"),
    # Agrega más idiomas según sea necesario...
}

@app.route('/detect', methods=['GET'])
def detect():
    return render_template('detectar.html')

@app.route('/detect_language', methods=['POST'])
def detect_language():
    original_text = request.form['text']

    if not original_text:
        return "Error: No text provided", 400

    key = os.environ.get('AZURE_TRANSLATOR_KEY')
    endpoint = os.environ.get('AZURE_TRANSLATOR_ENDPOINT')
    location = os.environ.get('AZURE_TRANSLATOR_REGION')

    if not key or not endpoint or not location:
        return "Error: Missing Azure credentials", 500

    path = '/detect?api-version=3.0'
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': original_text}]

    try:
        detector_request = requests.post(constructed_url, headers=headers, json=body)
        detector_request.raise_for_status()  # Lanza un error si la respuesta no es 200
        detector_response = detector_request.json()
        detected_language_code = detector_response[0]['language']
        
        # Obtener el nombre del idioma en español e inglés
        detected_language_name = IDIOMAS.get(detected_language_code, ("Desconocido", "Unknown"))
        
    except requests.exceptions.RequestException as e:
        return f"Error en la detección del idioma: {e}", 500

    # Después de obtener detected_language_code y detected_language_name
    detecciones = db['detecciones_idioma']
    detecciones.insert_one({
        "usuario": session['usuario'],
        "texto": original_text,
        "codigo_idioma": detected_language_code,
        "nombre_es": detected_language_name[0],
        "nombre_en": detected_language_name[1],
        "fecha": datetime.utcnow()
    })

    return render_template(
        'language_detected.html',
        detected_language_code=detected_language_code,
        detected_language_name_sp=detected_language_name[0],
        detected_language_name_en=detected_language_name[1],
        original_text=original_text
    )

AZURE_TTS_KEY = os.environ.get("AZURE_TTS_KEY")
AZURE_TTS_REGION = os.environ.get("AZURE_TTS_REGION", "francecentral")  # ajusta si es diferente

@app.route("/speak", methods=["GET", "POST"])
def speak():
    if request.method == "POST":
        text = request.form["text"]
        language = request.form["language"]
        voice = get_default_voice(language)

        # Get access token
        token_url = f"https://{AZURE_TTS_REGION}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        token_headers = {
            "Ocp-Apim-Subscription-Key": AZURE_TTS_KEY
        }
        token_response = requests.post(token_url, headers=token_headers)
        access_token = token_response.text

        # Build SSML
        ssml = f"""
        <speak version='1.0' xml:lang='{language}'>
            <voice xml:lang='{language}' xml:gender='Female' name='{voice}'>
                {text}
            </voice>
        </speak>
        """

        # Send TTS request
        tts_url = f"https://{AZURE_TTS_REGION}.tts.speech.microsoft.com/cognitiveservices/v1"
        tts_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
            "User-Agent": "FlaskTTSApp"
        }

        tts_response = requests.post(tts_url, headers=tts_headers, data=ssml)
        audio_path = f"static/audio_{uuid4().hex}.mp3"
        with open(audio_path, "wb") as f:
            f.write(tts_response.content)

        return render_template("text_to_speech.html", audio_url=url_for('static', filename=os.path.basename(audio_path)))

    return render_template("text_to_speech.html")


def get_default_voice(language_code):
    """Returns a default voice for the selected language."""
    voices = {
        "en-US": "en-US-JennyNeural",
        "en-GB": "en-GB-RyanNeural",
        "es-ES": "es-ES-ElviraNeural",
        "zh-CN": "zh-CN-XiaoxiaoNeural",
        "fr-FR": "fr-FR-DeniseNeural",
        "de-DE": "de-DE-KatjaNeural",
        "it-IT": "it-IT-ElsaNeural",
        "ja-JP": "ja-JP-NanamiNeural",
        "ko-KR": "ko-KR-SunHiNeural",
        "pt-BR": "pt-BR-FranciscaNeural"
    }
    return voices.get(language_code, "en-US-JennyNeural")

@app.route("/")
def home():
    return "<h1>Bienvenido</h1><p>Rutas: /speak, /translate, etc.</p>"

AZURE_LANGUAGE_KEY = os.environ.get("AZURE_TEXT_ANALYTICS_KEY")
AZURE_LANGUAGE_ENDPOINT = os.environ.get("AZURE_TEXT_ANALYTICS_ENDPOINT")

@app.route("/summarize", methods=["GET", "POST"])
def summarize():
    summary = None
    if request.method == "POST":
        input_text = request.form["text"]
        url = AZURE_LANGUAGE_ENDPOINT + "/language/analyze-text/jobs?api-version=2023-04-01"

        headers = {
            "Ocp-Apim-Subscription-Key": AZURE_LANGUAGE_KEY,
            "Content-Type": "application/json"
        }

        body = {
            "displayName": "Text summarization example",
            "analysisInput": {
                "documents": [
                    {
                        "id": "1",
                        "language": "es",
                        "text": input_text
                    }
                ]
            },
            "tasks": [
                {
                    "kind": "AbstractiveSummarization" #ExtractiveSummarization
                }
            ]
        }

        # Lanzamos el job
        response = requests.post(url, headers=headers, json=body)
        job_location = response.headers.get("operation-location")

        import time
        for _ in range(10):
            result = requests.get(job_location, headers=headers).json()
            if result["status"] == "succeeded":
                summary = result["tasks"]["items"][0]["results"]["documents"][0]["summaries"][0]["text"]

                # Guardar en la base de datos
                resumenes = db['resumenes']
                resumenes.insert_one({
                    "usuario": session['usuario'],
                    "original": input_text,
                    "resumen": summary,
                    "fecha": datetime.utcnow()
                })

                break  # salir del bucle si ya está listo

            time.sleep(1)

    return render_template("summarize.html", summary=summary)

# Conexión a MongoDB usando la variable DB
mongo_uri = os.getenv('DB')  # "mongodb://172.29.80.1:27017/microservice"
client = MongoClient(mongo_uri)
db = client[os.getenv('DB_NAME')]  # "microservice"
usuarios = db['auth_users']

# Simulación de usuarios válidos (puedes conectar con una BD luego)
USUARIOS_VALIDOS = {
    "admin": "1234",
    "usuario": "demo"
}

# Clave secreta para sesiones
# app.secret_key = os.getenv('SECRET_KEY', 'kH2!x9@Rtz#W3lPq8DnM5vLz')
app.secret_key = os.getenv('SECRET_KEY')
if app.secret_key is None:
    raise RuntimeError("SECRET_KEY no está definida en las variables de entorno")

# Crear hash de contraseña
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def es_password_segura(password):
    if (len(password) < 8 or
        not re.search(r"[A-Z]", password) or
        not re.search(r"[a-z]", password) or
        not re.search(r"\d", password) or
        not re.search(r"[^\w\s]", password)):
        return False
    return True

# Insertar usuario
def crear_usuario(username, password, email, full_name, role="user"):
    if usuarios.find_one({'username': username}):
        print(f"El usuario '{username}' ya existe.")
        return

    if not es_password_segura(password):
        print("La contraseña no cumple los requisitos de seguridad.")
        return

    hashed = hash_password(password)
    nuevo_usuario = {
        "username": username,
        "password": hashed,
        "email": email,
        "full_name": full_name,
        "role": role,
        "created_at": datetime.utcnow()
    }
    usuarios.insert_one(nuevo_usuario)
    print(f"Usuario '{username}' insertado correctamente.")

# Ejemplos con contraseñas seguras:
crear_usuario("admin", "Adm1n$2024", "admin@ejemplo.com", "Administrador del Sistema", "admin")
crear_usuario("usuario", "Us3r!Demo", "usuario@ejemplo.com", "Usuario Demo")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        usuario = usuarios.find_one({'username': username})

        #if usuario and usuario.get('password') == password:
        if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario['password'].encode('utf-8')):
            session['usuario'] = username
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Usuario o contraseña incorrectos.")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# Proteger tu página de inicio, si quieres
@app.before_request
def requerir_login():
    rutas_libres = ['login', 'static']
    if not session.get('usuario') and not request.endpoint in rutas_libres:
        if not request.endpoint or not request.endpoint.startswith('static'):
            return redirect(url_for('login'))

@app.route('/historial')
def historial():
    if 'usuario' not in session:
        return redirect(url_for('login'))  # O lo que uses para controlar acceso

    usuario = session['usuario']

    historial = {
        'traducciones': list(db['traducciones'].find({'usuario': usuario}).sort('fecha', -1)),
        'resumenes': list(db['resumenes'].find({'usuario': usuario}).sort('fecha', -1)),
        'detecciones_idioma': list(db['detecciones_idioma'].find({'usuario': usuario}).sort('fecha', -1)),
        'sentimientos': list(db['sentimientos'].find({'usuario': usuario}).sort('fecha', -1)),
        'descripciones_imagen': list(db['descripciones_imagen'].find({'usuario': usuario}).sort('fecha', -1)),
        'caras_detectadas': list(db['caras_detectadas'].find({'usuario': usuario}).sort('fecha', -1))
    }

    return render_template('historial.html', historial=historial)
      
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
