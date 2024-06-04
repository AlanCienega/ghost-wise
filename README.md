# ghost-wise

Stopping Ghosting with Artificial and Human Intelligence

## clone

```
git clone git@github.com:AlanCienega/ghost-wise.git
```

## set up environment

```
python -m venv env_gw
pip install -r requirements.txt
```
## create a .env file

AI_SERVICE_ENDPOINT="YOUR-LANGUAGE-ENDPOINT"
AI_SERVICE_KEY="YOUR-LANGUAGE-KEY"
AZURE_FORMRECOGNIZER_ENDPOINT="YOUR-DOCUMENT-INTELLIGENCE-ENDPOINT"
AZURE_FORMRECOGNIZER_KEY="YOUR-DOCUMENT-INTELLIGENCE-KEY"

---
**NOTE**

if you install more dependecies update requirements.txt by using:
---
```
pip freeze > requirements.txt
```
## start server
```
python app.py
```
## open your app in
[ http://127.0.0.1:5000]( http://127.0.0.1:5000)