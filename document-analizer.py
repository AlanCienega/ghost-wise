import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
load_dotenv()

# Cargar clave y endpoint desde variables de entorno
endpoint = os.getenv("AZURE_FORMRECOGNIZER_ENDPOINT")
key = os.getenv("AZURE_FORMRECOGNIZER_KEY")

# Crear el cliente de análisis de documentos
document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

cv_path = "resume.pdf"

def analyze_cv(cv_path):
    with open(cv_path, "rb") as file:
        try:
            poller = document_analysis_client.begin_analyze_document("prebuilt-document", file)
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

cv_data = analyze_cv(cv_path)

print(cv_data)