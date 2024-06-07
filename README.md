# Ghost Wise

Deteniendo el ghosting con inteligencia artificial y humana
## clonar

```
git clone git@github.com:AlanCienega/ghost-wise.git
cd ghost-wise
```

## configurar el entorno

```
python -m venv env_gw
pip install -r requirements.txt
```

## crear un archivo .env con tus credenciales
```
AI_SERVICE_ENDPOINT="YOUR-LANGUAGE-ENDPOINT"
AI_SERVICE_KEY="YOUR-LANGUAGE-KEY"
AZURE_FORMRECOGNIZER_ENDPOINT="YOUR-DOCUMENT-INTELLIGENCE-ENDPOINT"
AZURE_FORMRECOGNIZER_KEY="YOUR-DOCUMENT-INTELLIGENCE-KEY"
AZURE_BLOB_STORAGE_CONNECTION_STRING="YOUR AZURE-BLOB-CONNECTION-STRING"
AZURE_BLOB_STORAGE_CONTAINER_NAME="YOUR-CONTAINER-NAME"
AZURE_OPENAI_ENDPOINT="YOUR-OPENAI-ENDPOINT"
AZURE_OPENAI_API_KEY="YOUR-OPENAI-API-KEY"
CHAT_COMPLETIONS_DEPLOYMENT_NAME="YOUR-OPENAI-DEPLOYMENT-NAME"
```

---
**¡NOTA!**

si instalas más dependencias, actualiza requirements.txt usando:
---
```
pip freeze > requirements.txt
```

## iniciar el servidor
```
python app.py
```

## abre tu aplicación en
[ http://127.0.0.1:5000]( http://127.0.0.1:5000)
