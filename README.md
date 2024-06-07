# Ghost Wise: Deteniendo el ghosting con inteligencia artificial y humana

## Potenciando la Red Global de Mujeres en Tecnología

<p>Nuestra aplicación transforma el proceso de reclutamiento, garantizando una comunicación continua y respetuosa entre las empresas y los candidatos. Este enfoque no solo elimina el ghosting, sino que también fortalece la red global de mujeres en tecnología, en línea con los objetivos de Women in Cloud. </p>

## ¿Cómo lo hacemos?
1. Respuestas Inteligentes y Personalizadas:
   - Utilizamos un modelo de lenguaje avanzado (LLM) entrenado para responder a requerimientos de manera concreta y precisa. Por ejemplo, al buscar un "Desarrollador Flutter", el LLM genera un perfil detallado y directo que incluye habilidades clave y responsabilidades, asegurando descripciones claras y atractivas para atraer al talento adecuado.
2. Comparación y Compatibilidad Automática:
   - Nuestra aplicación analiza los perfiles de los candidatos en comparación con las descripciones de los puestos almacenadas en Azure Blob Storage. Utilizando técnicas de procesamiento de lenguaje natural, extraemos y comparamos entidades, asignando valores de compatibilidad para identificar a los candidatos más adecuados y evitar postulaciones inadecuadas.
3. Retroalimentación Personalizada:
   - Todos los candidatos reciben un mensaje personalizado, independientemente del resultado de su aplicación. Aquellos que no avanzan en el proceso reciben retroalimentación constructiva, mejorando su experiencia y percepción de la empresa, y reduciendo las críticas negativas en plataformas como Glassdoor.
## Impacto Social y Profesional:
<p>En línea con el reto presentado por Women in Cloud, nuestra solución se compromete a amplificar el poder de la red global de mujeres en tecnología. Al seguir los pilares de la IA responsable, nuestra aplicación garantiza que las mujeres y otros grupos subrepresentados tengan acceso equitativo a oportunidades basadas únicamente en sus habilidades y experiencia, sin discriminación por etnia, edad u otros factores demográficos.</p>

## Ampliación de la Red y Oportunidades:
<p>Nuestra herramienta facilita la identificación y el empoderamiento de talento femenino en tecnología, asegurando que las mujeres adecuadas estén en los puestos adecuados. Esto no solo mejora la inclusión y la diversidad en el lugar de trabajo, sino que también fortalece las redes profesionales y las oportunidades de colaboración.</p>

## Desafíos y Soluciones:
<p>A pesar de los obstáculos iniciales con la API de LinkedIn, nuestro equipo persistió y desarrolló una solución robusta e innovadora, demostrando nuestra capacidad para adaptarnos y superar desafíos tecnológicos.</P>

## Futuro de la Inclusión y la Diversidad:
<p>Nuestra aplicación no solo mejora la eficiencia del reclutamiento, sino que también promueve la transparencia, la igualdad y el respeto hacia todos los candidatos. Al eliminar sesgos inconscientes y garantizar que las mujeres en tecnología tengan acceso equitativo a oportunidades profesionales, estamos estableciendo un nuevo estándar en el ámbito profesional.</p>

# configuracion del proyecto

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


<h2 id="contrib">Contribuyentes</h2>

[Ani](https://github.com/anabugal) | [Meepo](#contrib) | [xooseph](https://github.com/xooseph) | [jesusreyes](https://github.com/jesusreyes) | [AlanCienega](https://github.com/AlanCienega)