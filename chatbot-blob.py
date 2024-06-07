import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
apikey = os.environ.get("AZURE_OPENAI_API_KEY")
deployment = os.environ.get("CHAT_COMPLETIONS_DEPLOYMENT_NAME")

client = AzureOpenAI(
    api_key=apikey,
    api_version="2024-02-01",
    azure_endpoint=endpoint
)

#Pide al reclutador el perfil que necesita que genere el chat
user_message = input("¿Qué es lo que necesitas?\n")

completion = client.chat.completions.create(
    model=deployment,
    messages=[
        {
            "role": "system",
            "content": "Actúa como un reclutador profesional con amplia experiencia en contratación de profesionales de múltiples áreas de trabajo y de multiples perfiles profesionales. \n\n"
        },
        {
            "role": "user",
            "content": "necesito contratar a una persona que me ayude con la creciente startup que tengo, somos una compañia de desarrollo de software para pymes, planeamos expandirnos por el momento con una oficina mas y darnos abasto con los clinetes que ya tenemos y que vamos adquiriendo, la tecnologia principal usada en la empresa es Laravel."
        },
        {
            "role": "assistant",
            "content": "Buscamos un full stack developer con al menos 3 años de experiencia en desarrollo web y conocimientos sólidos en laravel y vue.js. es esencial tener habilidades sólidas de comunicación y capacidad para trabajar en equipo. las responsabilidades incluyen el desarrollo de interfaces de usuario, la construcción de aplicaciones web y la realización de pruebas del sistema. requisitos: experiencia mínima de 3 años como full stack developer. conocimientos sólidos en laravel y vue.js. habilidades de comunicación sólidas. capacidad para trabajar en equipo."
        },
        {
            "role": "user",
            "content": "Mi empresa ya establecida está teniendo problemas con las páginas web; cargan lento y no se ven muy bien en todos los dispositivos. Por lo tanto, necesito a alguien para integrarse en el equipo de desarrollo. Nos dedicamos a hacer webs estáticas."
        },
        {
            "role": "assistant",
            "content": "Buscamos un Desarrollador Frontend con experiencia en optimización web y diseño responsivo.\nResponsabilidades:\nOptimizar el rendimiento de páginas web.\nImplementar diseño responsivo.\nMejorar apariencia y usabilidad en colaboración con el equipo de diseño.\nRealizar pruebas de compatibilidad en navegadores y dispositivos.\nRequisitos:\nExperiencia en desarrollo frontend de sitios web estáticos.\nConocimiento de HTML5, CSS3 y JavaScript.\nExperiencia en optimización de rendimiento web.\nFamiliaridad con Bootstrap o Flexbox.\nConocimiento básico de SEO.\nHabilidades de resolución de problemas y trabajo en equipo.\nExcelentes habilidades de comunicación."
        },
        {
            "role": "user",
            "content": "quiero un cientifico de datos"
        },
        {
            "role": "assistant",
            "content": "Buscamos un Científico de Datos con experiencia en matemáticas, estadística y programación para unirse a nuestro equipo.\nResponsabilidades:\n- Realizar análisis de datos.\n- Desarrollar modelos predictivos y de clasificación.\n- Trabajar con el equipo de ingeniería en soluciones escalables.\n- Interpretar y comunicar resultados del análisis.\n- Mantenerse actualizado con técnicas y herramientas de análisis de datos.\n- Colaborar en soluciones de negocio efectivas.\nRequisitos:\n- Licenciatura o Maestría en Matemáticas, Estadística, Ciencias de la Computación o campo relacionado.\n- Experiencia en programación en Python, R u otro lenguaje de programación estadística.\n- Uso de herramientas de análisis de datos (Pandas, NumPy, Matplotlib, Scikit-Learn, TensorFlow, Keras, etc.).\n- Habilidades de análisis y resolución de problemas.\n- Excelentes habilidades de comunicación y trabajo en equipo.\n- Experiencia con grandes conjuntos de datos y bases de datos relacionales.\n- Conocimiento en visualización de datos (Tableau, Power BI, QlikView) es una ventaja.\nSi cumples con los requisitos y estás interesado, ¡esperamos saber de ti!"
        },
        {
            "role": "user",
            "content": user_message
        }
    ]
)

# Hace una llamada al chat para obtener una respuesta
print(completion.choices[0].message.content)