from web_app.blueprints import anmeldung
from flask import render_template

@anmeldung.route('/')
def anmeldung_index():
    return render_template('anmeldung.html')