from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.storage.blob import BlobClient

def analyze_cv(blob_client: BlobClient, client: DocumentAnalysisClient):
    download_stream = blob_client.download_blob()
    file_data = download_stream.readall()

    try:
        poller = client.begin_analyze_document("prebuilt-businessCard", file_data)
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
