from flask import Flask, render_template, request
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.storage.blob import BlobServiceClient
from config import AI_ENDPOINT, AI_KEY, DOCUMENT_ENDPOINT, DOCUMENT_KEY, BLOB_CONNECTION_STRING, BLOB_CONTAINER_NAME
from text_analysis import get_language, get_sentiment, get_key_phrases, get_entities
from cv_analysis import analyze_cv
from compatibility import calculate_compatibility_entities
from weights import calculate_entity_weights

app = Flask(__name__)

# Create Azure clients
credential = AzureKeyCredential(AI_KEY)
ai_client = TextAnalyticsClient(endpoint=AI_ENDPOINT, credential=credential)
document_analysis_client = DocumentAnalysisClient(endpoint=DOCUMENT_ENDPOINT, credential=AzureKeyCredential(DOCUMENT_KEY))
blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
blob_container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)

weights = {}

@app.route('/')
def index():
    return render_template('index.html')

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