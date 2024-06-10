from flask import Flask, render_template, request, jsonify
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.storage.blob import BlobServiceClient
from config import AI_ENDPOINT, AI_KEY, DOCUMENT_ENDPOINT, DOCUMENT_KEY, BLOB_CONNECTION_STRING, BLOB_CONTAINER_NAME
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
from text_analysis import get_language, get_sentiment, get_key_phrases, get_entities
from cv_analysis import analyze_cv
from compatibility import calculate_compatibility_entities
from weights import calculate_entity_weights

load_dotenv()

app = Flask(__name__)

# Create Azure clients
credential = AzureKeyCredential(AI_KEY)
ai_client = TextAnalyticsClient(endpoint=AI_ENDPOINT, credential=credential)
document_analysis_client = DocumentAnalysisClient(endpoint=DOCUMENT_ENDPOINT, credential=AzureKeyCredential(DOCUMENT_KEY))
blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
blob_container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
apikey = os.environ.get("AZURE_OPENAI_API_KEY")
deployment = os.environ.get("CHAT_COMPLETIONS_DEPLOYMENT_NAME")

client = AzureOpenAI(
    api_key=apikey,
    api_version="2024-02-01",
    azure_endpoint=endpoint
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_message', methods=['POST'])
def generate_message():
    data = request.json
    compatibility_percentage = float(data['compatibility_percentage'])
    candidate_name = "candidato"
    common_entities = data['common_entities']
    
    if compatibility_percentage >= 70:
        message = (f"Estimado {candidate_name},\n\n"
                   f"Gracias por tu aplicación. Tus conocimientos y experiencia en {', '.join(common_entities)} "
                   f"nos parecen asombrosos y queremos que te unas a nuestro equipo.")
    else:
        message = (f"Estimado {candidate_name},\n\n"
                   f"Agradecemos tu interés en unirte a nuestro equipo. Aunque en esta ocasión no has sido seleccionado, "
                   f"te sugerimos mejorar tu experiencia en {', '.join(common_entities)} para futuras oportunidades. ¡Te deseamos mucho éxito!")

    return jsonify({"message": message})

@app.route('/get_profile', methods=['POST'])
def get_profile():
    data = request.json
    question = data['question']

    completion = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "system",
                "content": "Actúa como un reclutador profesional con amplia experiencia en contratación de profesionales de múltiples áreas de trabajo y de múltiples perfiles profesionales. \n\n"
            },
            {
                "role": "user",
                "content": "Necesito contratar a una persona que me ayude con la creciente startup que tengo, somos una compañía de desarrollo de software para pymes, planeamos expandirnos por el momento con una oficina más y darnos abasto con los clinetes que ya tenemos y que vamos adquiriendo, la tecnologia principal usada en la empresa es Laravel."
            },
            {
                "role": "assistant",
                "content": "Se busca Full Stack Developer con experiencia en desarrollo web, especializado en Laravel y Vue.js.\nHabilidades indispensables incluyen comunicación efectiva y trabajo en equipo.\nResponsabilidades: desarrollo de interfaces de usuario, construcción de aplicaciones web y pruebas del sistema.\nRequisitos adicionales: experiencia con git, testing phpunit, cypress y jest, sólidos conocimientos en Laravel y Vue.js, así como experiencia en metodologías ágiles como Scrum o Kanban."
            },
            {
                "role": "user",
                "content": "Mi empresa ya establecida está teniendo problemas con las páginas web; cargan lento y no se ven muy bien en todos los dispositivos.\nPor lo tanto, necesito a alguien para integrarse en el equipo de desarrollo.\nNos dedicamos a hacer webs estáticas."
            },
            {
                "role": "assistant",
                "content": "Se busca Desarrollador Frontend especializado en optimización de carga de páginas y mejora de la experiencia de usuario (UX/UI), con enfoque en sitios web estáticos adaptativos y responsivos.\nHabilidades clave incluyen dominio de HTML, CSS, y JavaScript, así como experiencia en herramientas modernas de optimización como Webpack, Vite y técnicas de renderizado rápido.\nEste profesional integrará nuestro equipo de desarrollo para garantizar que las páginas web carguen rápidamente y se vean óptimas en todos los dispositivos."
            },
            {
                "role": "user",
                "content": "Quiero un cientifico de datos."
            },
            {
                "role": "assistant",
                "content": "Estamos en la búsqueda de un Científico de Datos para unirse a nuestro equipo.\nResponsabilidades incluyen análisis de datos, modelado predictivo y desarrollo de algoritmos para resolver problemas comerciales complejos.\nHabilidades clave incluyen experiencia en Python, R, SQL, así como conocimientos en aprendizaje automático y estadísticas.\nSe valora experiencia en la implementación de soluciones de inteligencia artificial y habilidades de visualización de datos."
            },
            {
                "role": "user",
                "content": "Quisiera contratar a un ejecutivo de ventas pero solo personas de U.S.A."
            },
            {
                "role": "assistant",
                "content": "Me gustaria darte una descripción para ese puesto, pero soy un asistente que no fomenta la discriminación de ningun tipo, raza, etnia, religión, preferencias sexuales y especialmente género."
            },
            {
                "role": "user",
                "content": "Quisiera contratar a un taxista hombre con experiencia en viajes nacionales."
            },
            {
                "role": "assistant",
                "content": "Este puesto al igual que muchos existentes podría desempeñarlo cualquier persona, incluyendo una mujer también, te recomiendo adaptar tu requerimiento sin especificar filtros discriminativos."
            },
            {
                "role": "user",
                "content": "Estoy buscando a una desarrolladora web para mi empresa."
            },
            {
                "role": "assistant",
                "content": "Aprecio tu entusiasmo al querer incluir a una mujer, pero sé que aunque no pongas explícitamente que deba ser mujer, llegaran varias y muy talentosas mujeres, tu requerimiento seguirá siendo inclusivo con ellas aún si no especificas el género, de eso no te preocupes."
            },
            {
                "role": "user",
                "content": "Estoy buscando a un recepcionista para un hotel, sin discapacidad."
            },
            {
                "role": "assistant",
                "content": "Soy un asistente que no fomenta la discriminación de ningún tipo, por lo que te tengo que decir que este puesto al igual que muchos otros que no requieren esfuerzo físico excesivo o movimiento, debe poder ofrecerse a cualquier persona."
            },
            {
                "role": "user",
                "content": "Estoy buscando a una ayudante general mujer que pueda cargar 25kg."
            },
            {
                "role": "assistant",
                "content": "Aprecio tu entusiasmo con la inclusión, el perfil puede ofrecerse pero ten en cuenta que las leyes mexicanas tienen establecidos ciertos criterios con respecto al peso que puede cargar un trabajador (25kg hombres, 15kg mujeres), podrías incurrir en una falta si no sigues esos lineamientos, en cualquiera de los casos deberias proporcionar material de carga adecuados así como las condiciones."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )
    profile_text = completion.choices[0].message.content

    return jsonify({"profile": profile_text})

@app.route('/submit', methods=['POST'])
def submit():
    profile_text = request.form['profile']

    # Analyze technical profile
    profile_language = get_language(profile_text, ai_client)
    sentiment = get_sentiment(profile_text, ai_client)
    profile_key_phrases = get_key_phrases(profile_text, ai_client)
    profile_entities = get_entities(profile_text, ai_client)

    # Convert to lowercase and remove duplicates
    profile_key_phrases = list(set([phrase.lower() for phrase in profile_key_phrases]))
    profile_entities = list(set([entity.lower() for entity in profile_entities]))

    # Calculate entity weights
    weights = calculate_entity_weights(profile_entities)

    # Update the weights dictionary with calculated values
    weights.update(weights)

    profile_analysis = {
        "original_text": profile_text,
        "language": profile_language,
        "sentiment": sentiment,
        "key_phrases": profile_key_phrases,
        "entities": profile_entities
    }

    compatibility_results = []

    # Iterate through files in blob storage
    for blob in blob_container_client.list_blobs():
        blob_client = blob_container_client.get_blob_client(blob)
        
        # Analyze CV from Azure Blob Storage
        cv_data = analyze_cv(blob_client, document_analysis_client)

        # Get CV text
        cv_text = " ".join(cv_data.get("text", []))
        cv_language = get_language(cv_text, ai_client)
        cv_key_phrases = get_key_phrases(cv_text, ai_client)
        cv_entities = get_entities(cv_text, ai_client)

        # Convert to lowercase and remove duplicates
        cv_key_phrases = list(set([phrase.lower() for phrase in cv_key_phrases]))
        cv_entities = list(set([entity.lower() for entity in cv_entities]))

        # Calculate compatibility
        compatibility_percentage = calculate_compatibility_entities(profile_entities, cv_entities, weights)
        compatibility_percentage = round(compatibility_percentage, 2)

        compatibility_results.append({
            "cv_filename": blob.name,
            "cv_analysis": cv_data,
            "compatibility_percentage": compatibility_percentage,
            "common_entities": list(set(profile_entities).intersection(set(cv_entities))),
            "common_phrases": list(set(profile_key_phrases).intersection(set(cv_key_phrases)))
        })

    return render_template('result.html', profile_analysis=profile_analysis, compatibility_results=compatibility_results)
