from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.formrecognizer import DocumentAnalysisClient

app = Flask(__name__)

# Cargar configuraciones
load_dotenv()
ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
ai_key = os.getenv('AI_SERVICE_KEY')
document_endpoint = os.getenv("AZURE_FORMRECOGNIZER_ENDPOINT")
document_key = os.getenv("AZURE_FORMRECOGNIZER_KEY")

# Crear clientes de Azure
credential = AzureKeyCredential(ai_key)
ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)
document_analysis_client = DocumentAnalysisClient(endpoint=document_endpoint, credential=AzureKeyCredential(document_key))

# Funciones de análisis de texto
def get_language(text, client):
    response = client.detect_language(documents=[text])[0]
    return response.primary_language.name

def get_sentiment(text, client):
    response = client.analyze_sentiment(documents=[text])[0]
    return response.sentiment

def get_key_phrases(text, client):
    response = client.extract_key_phrases(documents=[text])[0]
    return response.key_phrases

def get_entities(text, client):
    response = client.recognize_entities(documents=[text])[0]
    return [entity.text for entity in response.entities]

# Función de análisis de CV
def analyze_cv(cv_path, client):
    with open(cv_path, "rb") as file:
        try:
            poller = client.begin_analyze_document("prebuilt-document", file)
            result = poller.result()
        except Exception as e:
            print(f"Error occurred: {e}")
            return {}

        extracted_data = {"text": []}
        for page in result.pages:
            page_text = []
            for line in page.lines:
                page_text.append(line.content)
            extracted_data["text"].append(" ".join(page_text))
        
        extracted_data["tables"] = []
        for table in result.tables:
            table_data = []
            for cell in table.cells:
                table_data.append({
                    "content": cell.content,
                    "rowIndex": cell.row_index,
                    "columnIndex": cell.column_index
                })
            extracted_data["tables"].append(table_data)
        
        return extracted_data

# Función para calcular la compatibilidad
def calculate_compatibility(profile_entities, profile_phrases, cv_entities, cv_phrases):
    common_entities = set(profile_entities).intersection(set(cv_entities))
    common_phrases = set(profile_phrases).intersection(set(cv_phrases))
    
    total_elements = len(profile_entities) + len(profile_phrases)
    if total_elements == 0:
        return 0
    
    compatibility_score = (len(common_entities) + len(common_phrases)) / total_elements * 100
    return compatibility_score

def calculate_compatibility_entities(profile_entities, cv_entities):
    common_entities = set(profile_entities).intersection(set(cv_entities))
    
    total_entities = len(profile_entities)
    if total_entities == 0:
        return 0
    
    compatibility_score = len(common_entities) / total_entities * 100
    return compatibility_score


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    profile_text = request.form['profile']
    cv_file = request.files['cv']

    # Analizar perfil técnico
    profile_language = get_language(profile_text, ai_client)
    sentiment = get_sentiment(profile_text, ai_client)
    profile_key_phrases = get_key_phrases(profile_text, ai_client)
    profile_entities = get_entities(profile_text, ai_client)

    profile_analysis = {
        "original_text": profile_text,
        "language": profile_language,
        "sentiment": sentiment,
        "key_phrases": profile_key_phrases,
        "entities": profile_entities
    }

    # Crear el directorio 'uploads' si no existe
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Guardar CV y analizarlo
    cv_path = os.path.join(upload_dir, cv_file.filename)
    cv_file.save(cv_path)
    cv_data = analyze_cv(cv_path, document_analysis_client)

    # Obtener el texto del CV
    cv_text = " ".join(cv_data.get("text", []))
    cv_language = get_language(cv_text, ai_client)
    cv_key_phrases = get_key_phrases(cv_text, ai_client)
    cv_entities = get_entities(cv_text, ai_client)

    # Calcular compatibilidad
    compatibility_percentage = calculate_compatibility_entities(profile_entities, cv_entities)

    result = {
        "profile_analysis": profile_analysis,
        "cv_analysis": cv_data,
        "compatibility_percentage": compatibility_percentage,
        "common_entities": list(set(profile_entities).intersection(set(cv_entities))),
        "common_phrases": list(set(profile_key_phrases).intersection(set(cv_key_phrases)))
    }

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
