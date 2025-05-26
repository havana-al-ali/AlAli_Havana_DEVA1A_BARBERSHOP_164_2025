"""
Gestion des "routes" FLASK et des données pour les clients.
Fichier : gestion_clients_crud.py
Auteur : OM 2021.03.16
"""

from pathlib import Path
from flask import flash, redirect, render_template, request, url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.clients.gestion_clients_wtf_forms import (
    FormWTFAjouterClients,
    FormWTFDeleteClient,
    FormWTFUpdateClient,
)

# Affichage des clients
@app.route("/clients/<string:order_by>/<int:id_client_sel>", methods=['GET', 'POST'])
def clients_afficher(order_by, id_client_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_client_sel == 0:
                    strsql_clients_afficher = "SELECT * from t_clients ORDER BY id_clients ASC"
                    mc_afficher.execute(strsql_clients_afficher)
                elif order_by == "ASC":
                    valeur_id_client_selected_dictionnaire = {"value_id_client_selected": id_client_sel}
                    strsql_clients_afficher = """
                        SELECT * FROM t_clients WHERE id_clients = %(value_id_client_selected)s
                    """
                    mc_afficher.execute(strsql_clients_afficher, valeur_id_client_selected_dictionnaire)
                else:
                    strsql_clients_afficher = "SELECT * FROM t_clients ORDER BY id_clients DESC"
                    mc_afficher.execute(strsql_clients_afficher)

                data_clients = mc_afficher.fetchall()

                if not data_clients and id_client_sel == 0:
                    flash('La table "t_clients" est vide.', "warning")
                elif not data_clients and id_client_sel > 0:
                    flash("Le client demandé n'existe pas.", "warning")
                else:
                    flash("Données clients affichées.", "success")

        except Exception as Exception_clients_afficher:
            raise ExceptionClientsAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{clients_afficher.__name__} ; "
                                          f"{Exception_clients_afficher}")

    return render_template("clients/clients_afficher.html", data=data_clients)

# Ajout client
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

                valeurs_insertion_dictionnaire = {
                    "value_intitule_client": name_client,
                    "value_prenom_pers": prenom_pers,
                    "value_telephone_pers": telephone_pers,
                }

                strsql_insert_client = """
                    INSERT INTO t_clients (id_clients, nom, prenom, telephone) 
                    VALUES (NULL, %(value_intitule_client)s, %(value_prenom_pers)s, %(value_telephone_pers)s)
                """

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_client, valeurs_insertion_dictionnaire)

                flash("Données insérées.", "success")
                return redirect(url_for('clients_afficher', order_by='DESC', id_client_sel=0))

        except Exception as Exception_clients_ajouter_wtf:
            raise ExceptionClientsAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{clients_ajouter_wtf.__name__} ; "
                                            f"{Exception_clients_ajouter_wtf}")

    return render_template("clients/clients_ajouter_wtf.html", form=form)

# Mise à jour client
@app.route("/client_update", methods=['GET', 'POST'])
def client_update_wtf():
    id_client_update = request.values.get('id_client', None)
    if id_client_update is None:
        flash("Erreur : aucun client sélectionné pour la mise à jour.", "danger")
        return redirect(url_for('clients_afficher', order_by='ASC', id_client_sel=0))

    form_update = FormWTFUpdateClient()

    try:
        if request.method == "POST" and form_update.submit.data:
            name_client_update = form_update.nom_client_update_wtf.data
            prenom_client_update = form_update.prenom_client_update_wtf.data
            telephone_client_update = form_update.telephone_client_update_wtf.data

            valeur_update_dictionnaire = {
                "value_id_client": id_client_update,
                "value_name_client": name_client_update,
                "value_prenom_client": prenom_client_update,
                "value_telephone_client": telephone_client_update
            }

            str_sql_update_intituleclient = """
                UPDATE t_clients SET nom = %(value_name_client)s,prenom = %(value_prenom_client)s, telephone = %(value_telephone_client)s
                WHERE id_clients = %(value_id_client)s
            """

            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intituleclient, valeur_update_dictionnaire)

            flash("Donnée mise à jour.", "success")
            return redirect(url_for('clients_afficher', order_by="ASC", id_client_sel=id_client_update))

        elif request.method == "GET":
            str_sql_id_client = "SELECT * FROM t_clients WHERE id_clients = %(value_id_client)s"
            valeur_select_dictionnaire = {"value_id_client": id_client_update}

            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_client, valeur_select_dictionnaire)
                data_nom_client = mybd_conn.fetchone()

            if data_nom_client:
                form_update.nom_client_update_wtf.data = data_nom_client["nom"]
                form_update.prenom_client_update_wtf.data = data_nom_client["prenom"]
                form_update.telephone_client_update_wtf.data = data_nom_client["telephone"]
            else:
                flash("Client non trouvé pour mise à jour.", "warning")
                return redirect(url_for('clients_afficher', order_by="ASC", id_client_sel=0))

    except Exception as Exception_client_update_wtf:
        raise ExceptionClientUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{client_update_wtf.__name__} ; "
                                      f"{Exception_client_update_wtf}")

    return render_template("clients/client_update_wtf.html", form_update=form_update)


@app.route("/client_delete", methods=['GET', 'POST'])
def client_delete_wtf():
    id_client_delete = request.values.get('id_client_btn_delete_html', None)
    if id_client_delete is None:
        flash("Erreur : aucun client sélectionné pour la suppression.", "danger")
        return redirect(url_for('clients_afficher', order_by="ASC", id_client_sel=0))

    form_delete = FormWTFDeleteClient()
    data_dependances_client_delete = None

    try:
        with DBconnection() as mc_conn:
            # Vérifier les dépendances dans toutes les tables liées
            str_sql_dependances = """
                SELECT 'rencontre' AS source, id_rencontrer AS id, date_heure AS info 
                FROM t_rencontrer WHERE FK_clients = %(value_id_client)s
                UNION ALL
                SELECT 'evaluation' AS source, id_evaluer AS id, CONCAT('Note: ', note, ' - ', date_avis) AS info 
                FROM t_evaluer WHERE FK_clients = %(value_id_client)s
            """
            mc_conn.execute(str_sql_dependances, {"value_id_client": id_client_delete})
            data_dependances_client_delete = mc_conn.fetchall()

        if request.method == "POST" and form_delete.validate_on_submit():
            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("clients_afficher", order_by="ASC", id_client_sel=0))

            if form_delete.submit_btn_del.data:
                if data_dependances_client_delete:
                    flash("Impossible de supprimer ce client car il est lié à d'autres données.", "danger")
                    return redirect(url_for('clients_afficher', order_by="ASC", id_client_sel=0))
                else:
                    # Suppression normale sans dépendances
                    str_sql_delete_client = "DELETE FROM t_clients WHERE id_clients = %(value_id_client)s"
                    with DBconnection() as mconn_bd:
                        mconn_bd.execute(str_sql_delete_client, {"value_id_client": id_client_delete})
                    flash("Client supprimé avec succès.", "success")
                    return redirect(url_for('clients_afficher', order_by="ASC", id_client_sel=0))

            if form_delete.submit_btn_force_del.data:
                # Suppression forcée - on supprime d'abord les dépendances
                with DBconnection() as mconn_bd:
                    # Supprimer d'abord les rencontres
                    str_sql_delete_rencontres = "DELETE FROM t_rencontrer WHERE FK_clients = %(value_id_client)s"
                    mconn_bd.execute(str_sql_delete_rencontres, {"value_id_client": id_client_delete})

                    # Supprimer ensuite les évaluations
                    str_sql_delete_evaluations = "DELETE FROM t_evaluer WHERE FK_clients = %(value_id_client)s"
                    mconn_bd.execute(str_sql_delete_evaluations, {"value_id_client": id_client_delete})

                    # Enfin supprimer le client
                    str_sql_delete_client = "DELETE FROM t_clients WHERE id_clients = %(value_id_client)s"
                    mconn_bd.execute(str_sql_delete_client, {"value_id_client": id_client_delete})

                flash("Client et toutes ses données associées ont été supprimés avec succès.", "success")
                return redirect(url_for('clients_afficher', order_by="ASC", id_client_sel=0))

        elif request.method == "GET":
            str_sql_client = "SELECT * FROM t_clients WHERE id_clients = %(value_id_client)s"
            with DBconnection() as mc_conn:
                mc_conn.execute(str_sql_client, {"value_id_client": id_client_delete})
                data_client = mc_conn.fetchone()

            if data_client:
                form_delete.nom_client_delete_wtf.data = data_client["nom"]
                form_delete.prenom_client_delete_wtf.data = data_client["prenom"]
                form_delete.telephone_client_delete_wtf.data = data_client["telephone"]
            else:
                flash("Client non trouvé pour suppression.", "warning")
                return redirect(url_for('clients_afficher', order_by="ASC", id_client_sel=0))

    except Exception as Exception_client_delete_wtf:
        raise ExceptionClientDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                       f"{client_delete_wtf.__name__} ; "
                                       f"{Exception_client_delete_wtf}")

    return render_template("clients/client_delete_wtf.html",
                           form_delete=form_delete,
                           data_dependances_client_delete=data_dependances_client_delete)