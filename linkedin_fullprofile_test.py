
import os
from dotenv import load_dotenv
from linkedin_api import Linkedin


load_dotenv()

# Autenticar con tus credenciales de LinkedIn
                   
email = os.getenv('CORREO')
password= os.getenv('PASSWORD')
linkedin = Linkedin(email,password)

# Función para buscar perfiles según habilidades específicas
def search_profiles_by_skills(api, skills):
    query = ' '.join(skills)
    results = api.search_people(keywords=query,limit=5)
    print("buscando")
    return results

def get_profile_contact_info(api,id):
    query = ' '.join(id)
    results = api.get_profile_contact_info(id)
    print("infocontacts")
    return results
   
def get_profile(api,id):
    query = ' '.join(id)
    results = api.get_profile(id)
    print("infototal")
    return results

# Lista de habilidades deseadas
#desired_skills = ['Python']
desired_skills = ['Python', 'Data Analysis', 'Machine Learning', 'SQL']    
 
print(desired_skills)

# Buscar perfil
profiles = search_profiles_by_skills(linkedin, desired_skills)
print(profiles)

  
# Imprimir resultados
for profile in profiles:
    print(f"Full Name: {profile['name']}")   
    contact_info=get_profile_contact_info(linkedin, profile['urn_id'])    
    print(contact_info)
    fullprofile=get_profile(linkedin, profile['urn_id'])    
    print(fullprofile)
    print("------------")
