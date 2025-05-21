from pathlib import Path
from flask import redirect, request, session, url_for, flash, render_template
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.employes.gestion_employes_wtf_forms import FormWTFUpdateEmploye, FormWTFAddEmploye, FormWTFDeleteEmploye

@app.route("/rencontrer/<string:order_by>/<int:id_rencontrer_sel>", methods=['GET', 'POST'])
def rencontrer_afficher(order_by, id_rencontrer_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_rencontrer_sel == 0:
                    strsql_rencontrer_afficher = """SELECT * from t_rencontrer ORDER BY id_rencontrer ASC"""
                    mc_afficher.execute(strsql_rencontrer_afficher)
                elif order_by == "ASC":
                    valeur_id_rencontrer_selected_dictionnaire = {"value_id_rencontrer_selected": id_rencontrer_sel}
                    strsql_rencontrer_afficher = """SELECT * FROM t_rencontrer WHERE id_rencontrer = %(value_id_rencontrer_selected)s"""
                    mc_afficher.execute(strsql_rencontrer_afficher, valeur_id_rencontrer_selected_dictionnaire)
                else:
                    strsql_rencontrer_afficher = """SELECT * FROM t_rencontrer ORDER BY id_rencontrer DESC"""
                    mc_afficher.execute(strsql_rencontrer_afficher)

                data_rencontrer = mc_afficher.fetchall()
                print("data_rencontrer ", data_rencontrer, " Type : ", type(data_rencontrer))

                if not data_rencontrer and id_rencontrer_sel == 0:
                    flash("""La table "t_rencontrer" est vide. !!""", "warning")
                elif not data_rencontrer and id_rencontrer_sel > 0:
                    flash(f"Le rencontrer demandé n'existe pas !!", "warning")
                else:
                    flash(f"Données rencontrer affichées !!", "success")

        except Exception as Exception_rencontrer_afficher:
            raise ExceptionRencontrerAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{rencontrer_afficher.__name__} ; "
                                          f"{Exception_rencontrer_afficher}")

    return render_template("rencontrer/rencontrer_afficher.html", data=data_rencontrer)


@app.route("/employe_add", methods=['GET', 'POST'])
def rencontrer_add_wtf():
    form_add_rencontrer = FormWTFAddRencontrer()
    if request.method == "POST":
        try:
            if form_add_rencontrer.validate_on_submit():
                nom_emp_add = form_add_rencontrer.nom_rencontrer_wtf.data
                prenom_emp_add = form_add_employe.prenom_employe_wtf.data
                telephone_emp_add = form_add_employe.telephone_employe_wtf.data
                specialite_emp_add = form_add_employe.specialite_employe_wtf.data

                valeurs_insertion_dictionnaire = {
                    "value_nom_employe": nom_emp_add,
                    "value_prenom_employe": prenom_emp_add,
                    "value_telephone_employe": telephone_emp_add,
                    "value_specialite_employe": specialite_emp_add
                }
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_employe = """INSERT INTO t_employes (id_rencontrer,  FK_clients, FK_employes, date_heure) 
                                           VALUES (NULL, %(value_nom_employe)s, %(value_prenom_employe)s, %(value_telephone_employe)s, %(value_specialite_employe)s)"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_rencontrer, valeurs_insertion_dictionnaire)

                flash(f"Données rencontrer insérées !!", "success")
                print(f"Données rencontrer insérées !!")

                return redirect(url_for('rencontrer_afficher', id_rencontrer_sel=0))

        except Exception as Exception_rencontrer_ajouter_wtf:
            raise ExceptionRencontrerAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                             f"{rencontrer_add_wtf.__name__} ; "
                                             f"{Exception_rencontrer_ajouter_wtf}")

    return render_template("rencontrer/rencontrer_add_wtf.html", form_add_rencontrer=form_add_rencontrer)


@app.route("/rencontrer_update", methods=['GET', 'POST'])
def rencontrer_update_wtf():
    id_rencontrer_update = request.values['id_employe_btn_edit_html']
    form_update_employe = FormWTFUpdateEmploye()

    try:
        if request.method == "POST" and form_update_employe.submit.data:
            nom_employe_update = form_update_employe.nom_employe_update_wtf.data
            prenom_employe_update = form_update_employe.prenom_employe_update_wtf.data
            telephone_employe_update = form_update_employe.telephone_employe_update_wtf.data
            specialite_employe_update = form_update_employe.specialite_employe_update_wtf.data

            valeur_update_dictionnaire = {
                "value_id_employe": id_employe_update,
                "value_nom_employe": nom_employe_update,
                "value_prenom_employe": prenom_employe_update,
                "value_telephone_employe": telephone_employe_update,
                "value_specialite_employe": specialite_employe_update
            }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_rencontrer = """UPDATE t_employes SET date_heure = %(value_nom_employe)s,
                                                              prenom = %(value_prenom_employe)s,
                                                              telephone = %(value_telephone_employe)s,
                                                              specialite = %(value_specialite_employe)s
                                                              WHERE id_employes = %(value_id_employe)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_rencontrer, valeur_update_dictionnaire)

            flash(f"Donnée rencontrer mise à jour !!", "success")
            print(f"Donnée rencontrer mise à jour !!")

            return redirect(url_for('rencontrer_afficher', id_rencontrer_sel=id_rencontrer_update))
        elif request.method == "GET":
            str_sql_id_rencontrer = "SELECT * FROM t_rencontrer WHERE id_rencontrer = %(value_id_rencontrer)s"
            valeur_select_dictionnaire = {"value_id_rencontrer": id_rencontrer_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_rencontrer, valeur_select_dictionnaire)
            data_rencontrer = mybd_conn.fetchone()
            print("data_rencontrer ", data_rencontrer, " type ", type(data_employe), " rencontrer ",
                  data_rencontrer["date_heure"])

            form_update_rencontrer.nom_rencontrer_update_wtf.data = data_rencontrer["date_heure"]

            #form_update_employe.prenom_employe_update_wtf.data = data_employe["prenom"]
            #form_update_employe.telephone_employe_update_wtf.data = data_employe["telephone"]
            #form_update_employe.specialite_employe_update_wtf.data = data_employe["specialite"]

    except Exception as Exception_rencontrer_update_wtf:
        raise ExceptionRencontrerUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                       f"{rencontrer_update_wtf.__name__} ; "
                                       f"{Exception_rencontrer_update_wtf}")

    return render_template("rencontrer/rencontrer_update_wtf.html", form_update_rencontrer=form_update_rencontrer)


@app.route("/rencontrer_delete", methods=['GET', 'POST'])
def rencontrer_delete_wtf():
    data_rencontrer_delete = None
    btn_submit_del = None
    id_rencontrer_delete = request.values['id_rencontrer_btn_delete_html']

    form_delete_rencontrer = FormWTFDeleteRencontrer()
    try:
        if form_delete_rencontrer.submit_btn_annuler.data:
            return redirect(url_for("rencontrer_afficher", id_rencontrer_sel=0))

        if form_delete_rencontrer.submit_btn_conf_del_rencontrer.data:
            data_employe_delete = session['data_rencontrer_delete']
            flash(f"Effacer le rencontrer de façon définitive de la BD !!!", "danger")
            btn_submit_del = True

        if form_delete_rencontrer.submit_btn_del_rencontrer.data:
            valeur_delete_dictionnaire = {"value_id_rencontrer": id_rencontrer_delete}
            str_sql_delete_rencontrer = """DELETE FROM t_rencontrer WHERE id_rencontrer = %(value_id_rencontrer)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_delete_rencontrer, valeur_delete_dictionnaire)

            flash(f"Rencontrer définitivement effacé !!", "success")
            return redirect(url_for('rencontrer_afficher', id_employe_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_employe": id_employe_delete}
            str_sql_rencontrer_delete = """SELECT * FROM t_rencontrer WHERE id_rencontrer = %(value_id_rencontrer)s"""
            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_rencontrer_delete, valeur_select_dictionnaire)
                data_rencontrer_delete = mydb_conn.fetchall()
                session['data_rencontrer_delete'] = data_rencontrer_delete

            btn_submit_del = False

    except Exception as Exception_rencontrer_delete_wtf:
        raise ExceptionRencontrerDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                       f"{rencontrer_delete_wtf.__name__} ; "
                                       f"{Exception_rencontrer_delete_wtf}")

    return render_template("rencontrer/rencontrer_delete_wtf.html",
                           form_delete_rencontrer=form_delete_employe,
                           btn_submit_del=btn_submit_del,
                           data_rencontrer_del=data_rencontrer_delete)
