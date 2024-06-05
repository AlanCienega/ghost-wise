from azure.ai.textanalytics import TextAnalyticsClient

def get_language(text, client: TextAnalyticsClient):
    response = client.detect_language(documents=[text])[0]
    return response.primary_language.name

def get_sentiment(text, client: TextAnalyticsClient):
    response = client.analyze_sentiment(documents=[text])[0]
    return response.sentiment

def get_key_phrases(text, client: TextAnalyticsClient):
    response = client.extract_key_phrases(documents=[text])[0]
    return response.key_phrases

def get_entities(text, client: TextAnalyticsClient):
    response = client.recognize_entities(documents=[text])[0]
    return [entity.text for entity in response.entities]
