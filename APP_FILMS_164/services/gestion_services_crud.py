from pathlib import Path
from flask import redirect, request, session, url_for, flash, render_template

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.services.gestion_services_wtf_forms import FormWTFAjouterServices
from APP_FILMS_164.services.gestion_services_wtf_forms import FormWTFDeleteService
from APP_FILMS_164.services.gestion_services_wtf_forms import FormWTFUpdateService


@app.route("/services_afficher/<string:order_by>/<int:id_service_sel>", methods=['GET', 'POST'])
def services_afficher(order_by, id_service_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_service_sel == 0:
                    strsql_services_afficher = """SELECT * FROM t_services ORDER BY id_services ASC"""
                    mc_afficher.execute(strsql_services_afficher)
                elif order_by == "ASC":
                    valeur_id_service_selected_dictionnaire = {"value_id_service_selected": id_service_sel}
                    strsql_services_afficher = """SELECT * FROM t_services WHERE id_services = %(value_id_service_selected)s"""
                    mc_afficher.execute(strsql_services_afficher, valeur_id_service_selected_dictionnaire)
                else:
                    strsql_services_afficher = """SELECT * FROM t_services ORDER BY id_services DESC"""
                    mc_afficher.execute(strsql_services_afficher)

                data_services = mc_afficher.fetchall()

                if not data_services and id_service_sel == 0:
                    flash("La table 't_services' est vide !!", "warning")
                elif not data_services and id_service_sel > 0:
                    flash("Le service demandé n'existe pas !!", "warning")
                else:
                    flash("Données des services affichées !!", "success")

        except Exception as Exception_services_afficher:
            raise ExceptionGenresAfficher(f"{Path(__file__).name} ; {services_afficher.__name__} ; {Exception_services_afficher}")

    return render_template("services/services_afficher.html", data=data_services)


@app.route("/services_ajouter", methods=['GET', 'POST'])
def services_ajouter_wtf():
    form = FormWTFAjouterServices()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                nom_service = form.nom_service_wtf.data
                prix = form.prix_service_wtf.data
                duree = form.duree_service_wtf.data

                valeurs_insertion_dictionnaire = {
                    "value_nom_service": nom_service,
                    "value_prix": prix,
                    "value_duree": duree
                }

                strsql_insert_service = """INSERT INTO t_services 
                                           (id_services, nom_service, prix, duree) 
                                           VALUES (NULL, %(value_nom_service)s, %(value_prix)s, %(value_duree)s)"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_service, valeurs_insertion_dictionnaire)

                flash("Service ajouté avec succès !!", "success")
                return redirect(url_for('services_afficher', order_by='DESC', id_service_sel=0))

        except Exception as Exception_services_ajouter:
            raise ExceptionGenresAjouterWtf(f"{Path(__file__).name} ; {services_ajouter_wtf.__name__} ; {Exception_services_ajouter}")

    return render_template("services/services_ajouter_wtf.html", form=form)


@app.route("/service_update", methods=['GET', 'POST'])
def service_update_wtf():
    id_service_update = request.values['id_service_btn_edit_html']
    form_update = FormWTFUpdateService()
    try:
        if request.method == "POST" and form_update.submit.data:
            nom_service = form_update.nom_service_update_wtf.data
            prix = form_update.prix_service_update_wtf.data
            duree = form_update.duree_service_update_wtf.data

            valeur_update_dictionnaire = {
                "value_id_service": id_service_update,
                "value_nom_service": nom_service,
                "value_prix": prix,
                "value_duree": duree
            }

            str_sql_update_service = """UPDATE t_services 
                                        SET nom_service = %(value_nom_service)s, 
                                            prix = %(value_prix)s, 
                                            duree = %(value_duree)s 
                                        WHERE id_services = %(value_id_service)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_service, valeur_update_dictionnaire)

            flash("Service mis à jour avec succès !!", "success")
            return redirect(url_for('services_afficher', order_by="ASC", id_service_sel=id_service_update))

        elif request.method == "GET":
            str_sql_id_service = "SELECT id_services, nom_service, prix, duree FROM t_services WHERE id_services = %(value_id_service)s"
            valeur_select_dictionnaire = {"value_id_service": id_service_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_service, valeur_select_dictionnaire)
                data_service = mybd_conn.fetchone()

                form_update.nom_service_update_wtf.data = data_service["nom_service"]
                form_update.prix_service_update_wtf.data = data_service["prix"]
                form_update.duree_service_update_wtf.data = data_service["duree"]

    except Exception as Exception_service_update:
        raise ExceptionGenreUpdateWtf(f"{Path(__file__).name} ; {service_update_wtf.__name__} ; {Exception_service_update}")

    return render_template("services/service_update_wtf.html", form_update=form_update)


@app.route("/service_delete", methods=['GET', 'POST'])
def service_delete_wtf():
    data_associe_delete = None
    btn_submit_del = None
    id_service_delete = request.values['id_service_btn_delete_html']
    form_delete = FormWTFDeleteService()
    try:
        if request.method == "POST" and form_delete.validate_on_submit():
            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("services_afficher", order_by="ASC", id_service_sel=0))

            if form_delete.submit_btn_conf_del.data:
                data_associe_delete = session['data_associe_delete']
                flash("Effacer le service de façon définitive de la BD !!!", "danger")
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_service": id_service_delete}
                str_sql_delete_service = """DELETE FROM t_services WHERE id_services = %(value_id_service)s"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_service, valeur_delete_dictionnaire)

                flash("Service supprimé définitivement !!", "success")
                return redirect(url_for('services_afficher', order_by="ASC", id_service_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_service": id_service_delete}
            str_sql_id_service = "SELECT id_services, nom_service FROM t_services WHERE id_services = %(value_id_service)s"
            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_id_service, valeur_select_dictionnaire)
                data_service = mydb_conn.fetchone()
                form_delete.nom_service_delete_wtf.data = data_service["nom_service"]

                session['data_associe_delete'] = data_associe_delete
                btn_submit_del = False

    except Exception as Exception_service_delete:
        raise ExceptionGenreDeleteWtf(f"{Path(__file__).name} ; {service_delete_wtf.__name__} ; {Exception_service_delete}")

    return render_template("services/service_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_associe=data_associe_delete)
