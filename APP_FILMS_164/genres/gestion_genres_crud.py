"""Gestion des "routes" FLASK et des données pour les clients.
Fichier : gestion_clients_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.clients.gestion_clients_wtf_forms import FormWTFAjouterClients
from APP_FILMS_164.clients.gestion_clients_wtf_forms import FormWTFDeleteClient
from APP_FILMS_164.clients.gestion_clients_wtf_forms import FormWTFUpdateClient

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /clients_afficher
    
    Test : ex : http://127.0.0.1:5575/clients_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_client_sel = 0 >> tous les clients.
                id_client_sel = "n" affiche le client dont l'id est "n"
"""


@app.route("/clients/<string:order_by>/<int:id_client_sel>", methods=['GET', 'POST'])
def clients_afficher(order_by, id_client_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_client_sel == 0:
                    strsql_clients_afficher = """SELECT * from t_clients ORDER BY id_clients ASC"""
                    mc_afficher.execute(strsql_clients_afficher)
                elif order_by == "ASC":
                    valeur_id_client_selected_dictionnaire = {"value_id_client_selected": id_client_sel}
                    strsql_clients_afficher = """SELECT * FROM t_clients WHERE id_clients = %(value_id_client_selected)s"""

                    mc_afficher.execute(strsql_clients_afficher, valeur_id_client_selected_dictionnaire)
                else:
                    strsql_clients_afficher = """SELECT *  FROM t_clients ORDER BY id_clients DESC"""

                    mc_afficher.execute(strsql_clients_afficher)

                data_clients = mc_afficher.fetchall()

                print("data_clients ", data_clients, " Type : ", type(data_clients))

                # Différencier les messages si la table est vide.
                if not data_clients and id_client_sel == 0:
                    flash("""La table "t_client" est vide. !!""", "warning")
                elif not data_clients and id_client_sel > 0:
                    flash(f"Le client demandé n'existe pas !!", "warning")
                else:
                    flash(f"Données clients affichées !!", "success")

        except Exception as Exception_clients_afficher:
            raise ExceptionClientsAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{clients_afficher.__name__} ; "
                                          f"{Exception_clients_afficher}")

    return render_template("clients/clients_afficher.html", data=data_clients)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /clients_ajouter
    
    Test : ex : http://127.0.0.1:5575/clients_ajouter
    
    Paramètres : sans
    
    But : Ajouter un client
    
    Remarque :  Dans le champ "name_client_html" du formulaire "clients/clients_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/clients_ajouter", methods=['GET', 'POST'])
def clients_ajouter_wtf():
    form = FormWTFAjouterClients()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                name_client_wtf = form.nom_client_wtf.data
                name_client = name_client_wtf.lower()
                prenom_pers = form.prenom_wtf.data
                telephone_pers = form.telephone_wtf.data
                valeurs_insertion_dictionnaire = {"value_intitule_client": name_client,
                                                  "value_prenom_pers": prenom_pers,
                                                  "value_telephone_pers": telephone_pers,
                                                  }
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_client = """INSERT INTO t_clients (id_clients,nom,prenom,telephone) VALUES (NULL,%(value_intitule_client)s,%(value_prenom_pers)s,%(value_telephone_pers)s)"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_client, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                return redirect(url_for('clients_afficher', order_by='DESC', id_client_sel=0))

        except Exception as Exception_clients_ajouter_wtf:
            raise ExceptionClientsAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{clients_ajouter_wtf.__name__} ; "
                                            f"{Exception_clients_ajouter_wtf}")

    return render_template("clients/clients_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /client_update
    
    Test : ex cliquer sur le menu "clients" puis cliquer sur le bouton "EDIT" d'un "client"
    
    Paramètres : sans
    
    But : Editer(update) un client qui a été sélectionné dans le formulaire "clients_afficher.html"
    
    Remarque :  Dans le champ "nom_client_update_wtf" du formulaire "clients/client_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/client_update", methods=['GET', 'POST'])
def client_update_wtf():
    id_client_update = request.values['id_client_btn_edit_html']

    form_update = FormWTFUpdateClient()
    try:
        if request.method == "POST" and form_update.submit.data:
            name_client_update = form_update.nom_client_update_wtf.data
            name_client_update = name_client_update.lower()
            date_client_essai = form_update.date_client_wtf_essai.data

            valeur_update_dictionnaire = {"value_id_client": id_client_update,
                                          "value_name_client": name_client_update,
                                          "value_date_client_essai": date_client_essai
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intituleclient = """UPDATE t_client SET intitule_client = %(value_name_client)s, 
            date_ins_client = %(value_date_client_essai)s WHERE id_client = %(value_id_client)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intituleclient, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            return redirect(url_for('clients_afficher', order_by="ASC", id_client_sel=id_client_update))
        elif request.method == "GET":
            str_sql_id_client = "SELECT id_client, intitule_client, date_ins_client FROM t_client " \
                               "WHERE id_client = %(value_id_client)s"
            valeur_select_dictionnaire = {"value_id_client": id_client_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_client, valeur_select_dictionnaire)
            data_nom_client = mybd_conn.fetchone()
            print("data_nom_client ", data_nom_client, " type ", type(data_nom_client), " client ",
                  data_nom_client["intitule_client"])

            form_update.nom_client_update_wtf.data = data_nom_client["intitule_client"]
            form_update.date_client_wtf_essai.data = data_nom_client["date_ins_client"]

    except Exception as Exception_client_update_wtf:
        raise ExceptionClientUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{client_update_wtf.__name__} ; "
                                      f"{Exception_client_update_wtf}")

    return render_template("clients/client_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /client_delete
    
    Test : ex. cliquer sur le menu "clients" puis cliquer sur le bouton "DELETE" d'un "client"
    
    Paramètres : sans
    
    But : Effacer(delete) un client qui a été sélectionné dans le formulaire "clients_afficher.html"
    
    Remarque :  Dans le champ "nom_client_delete_wtf" du formulaire "clients/client_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/client_delete", methods=['GET', 'POST'])
def client_delete_wtf():
    data_films_attribue_client_delete = None
    btn_submit_del = None
    id_client_delete = request.values['id_client_btn_delete_html']

    form_delete = FormWTFDeleteClient()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("clients_afficher", order_by="ASC", id_client_sel=0))

            if form_delete.submit_btn_conf_del.data:
                data_films_attribue_client_delete = session['data_films_attribue_client_delete']
                print("data_films_attribue_client_delete ", data_films_attribue_client_delete)

                flash(f"Effacer le client de façon définitive de la BD !!!", "danger")
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_client": id_client_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_films_client = """DELETE FROM t_clients WHERE fk_clients = %(value_id_clients)s"""
                str_sql_delete_idclient = """DELETE FROM t_clients WHERE id_clients = %(value_id_clients)s"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_client, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idclient, valeur_delete_dictionnaire)

                flash(f"Client définitivement effacé !!", "success")
                print(f"Client définitivement effacé !!")

                return redirect(url_for('clients_afficher', order_by="ASC", id_client_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_client": id_client_delete}
            print(id_client_delete, type(id_client_delete))

            str_sql_clients_films_delete = """SELECT id_client_film, nom_film, id_client, intitule_client FROM t_client_film 
                                            INNER JOIN t_film ON t_client_film.fk_film = t_film.id_film
                                            INNER JOIN t_client ON t_client_film.fk_client = t_clients.id_clients
                                            WHERE fk_clients = %(value_id_clients)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_clients_films_delete, valeur_select_dictionnaire)
                data_films_attribue_client_delete = mydb_conn.fetchall()
                print("data_films_attribue_client_delete...", data_films_attribue_client_delete)

                session['data_films_attribue_client_delete'] = data_films_attribue_client_delete

                str_sql_id_client = "SELECT id_clients, intitule_client FROM t_clients WHERE id_clients = %(value_id_clients)s"

                mydb_conn.execute(str_sql_id_client, valeur_select_dictionnaire)
                data_nom_client = mydb_conn.fetchone()
                print("data_nom_client ", data_nom_client, " type ", type(data_nom_client), " client ",
                      data_nom_client["intitule_client"])

            form_delete.nom_client_delete_wtf.data = data_nom_client["intitule_client"]

            btn_submit_del = False

    except Exception as Exception_client_delete_wtf:
        raise ExceptionClientDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{client_delete_wtf.__name__} ; "
                                      f"{Exception_client_delete_wtf}")

    return render_template("clients/client_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_client_delete)
