import os
from azure.ai.formrecognizer import DocumentModelAdministrationClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
load_dotenv()

# Cargar clave y endpoint desde variables de entorno
endpoint = os.getenv("AZURE_FORMRECOGNIZER_ENDPOINT")
key = os.getenv("AZURE_FORMRECOGNIZER_KEY")

# Crear el cliente de administración de modelos de documentos
client = DocumentModelAdministrationClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Listar los modelos disponibles
def list_models():
    try:
        models = client.list_document_models()
        print("Modelos disponibles:")
        for model in models:
            print(f"Model ID: {model.model_id}")
    except Exception as e:
        print(f"Error occurred: {e}")

# Llamada a la función para listar los modelos
list_models()