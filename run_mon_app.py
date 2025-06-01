# run_mon_app.py

"""Point de départ de l'application
Fichier : run_mon_app.py
Auteur : OM 2023.03.25
"""

from APP_FILMS_164 import app
from APP_FILMS_164 import SECRET_KEY_FLASK
from APP_FILMS_164 import DEBUG_FLASK
from APP_FILMS_164 import ADRESSE_SRV_FLASK
from APP_FILMS_164 import PORT_FLASK
from flask_cors import CORS
from flask import render_template

CORS(app)

# 💡 Ajoute ta route ici (attention à ne pas redéfinir `app`)
@app.route("/readme")
def readme():
    return render_template("readme.html")

if __name__ == '__main__':
    app.secret_key = SECRET_KEY_FLASK
    app.run(debug=DEBUG_FLASK, host=ADRESSE_SRV_FLASK, port=PORT_FLASK)
