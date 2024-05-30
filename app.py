from flask import Flask, request, render_template
from dotenv import load_dotenv
from linkedin_api import Linkedin
import os

load_dotenv()

app = Flask(__name__)

# Iniciar sesión en LinkedIn API
api = Linkedin(os.getenv('EMAIL'), os.getenv('PASSWORD'))

@app.route('/', methods=['GET', 'POST'])
def index():
    profile_data = None
    certifications = []
    if request.method == 'POST':
        profile = request.form['profile']
        profile_data = api.get_profile(profile)
        certifications = profile_data['certifications']
    return render_template(
        'index.html',
        profile_data=profile_data, 
        certifications=certifications,
        certifications_counter=len(certifications) 
        )

if __name__ == '__main__':
    app.run(debug=True)
