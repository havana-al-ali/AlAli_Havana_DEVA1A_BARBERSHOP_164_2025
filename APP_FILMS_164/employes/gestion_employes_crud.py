from datetime import datetime
from pathlib import Path
from flask import redirect, request, session, url_for, flash, render_template
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.employes.gestion_employes_wtf_forms import FormWTFUpdateEmploye, FormWTFAddEmployes, FormWTFDeleteEmploye
from pymysql.err import IntegrityError


@app.route("/employes/<string:order_by>/<int:id_employe_sel>", methods=['GET', 'POST'])
def employes_afficher(order_by, id_employe_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_employe_sel == 0:
                    strsql_employes_afficher = """SELECT * from t_employes ORDER BY id_employes ASC"""
                    mc_afficher.execute(strsql_employes_afficher)
                elif order_by == "ASC":
                    valeur_id_employes_selected_dictionnaire = {"value_id_employes_selected": id_employe_sel}
                    strsql_employes_afficher = """SELECT * FROM t_employes WHERE id_employes = %(value_id_employes_selected)s"""
                    mc_afficher.execute(strsql_employes_afficher, valeur_id_employes_selected_dictionnaire)
                else:
                    strsql_employes_afficher = """SELECT * FROM t_employes ORDER BY id_employes DESC"""
                    mc_afficher.execute(strsql_employes_afficher)

                data_employes = mc_afficher.fetchall()
                print("data_employes ", data_employes, " Type : ", type(data_employes))

                if not data_employes and id_employe_sel == 0:
                    flash("""La table "t_employes" est vide. !!""", "warning")
                elif not data_employes and id_employe_sel > 0:
                    flash(f"L'employé demandé n'existe pas !!", "warning")
                else:
                    flash(f"Données employées affichées !!", "success")

        except Exception as Exception_employes_afficher:
            raise ExceptionEmployesAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{employes_afficher.__name__} ; "
                                          f"{Exception_employes_afficher}")

    return render_template("employes/employes_afficher.html", data=data_employes)


@app.route("/employe_add", methods=["GET", "POST"])
def employe_add_wtf():
    form = FormWTFAddEmployes()
    if request.method == "POST" and form.validate_on_submit():
        try:
            nom = form.nom_employe_wtf.data
            prenom = form.prenom_employe_wtf.data
            telephone = form.telephone_employe_wtf.data
            specialite = form.specialite_employe_wtf.data

            valeurs_dict = {
                "nom": nom,
                "prenom": prenom,
                "telephone": telephone,
                "specialite": specialite
            }


            strsql_insert = """
                INSERT INTO t_employes (nom, prenom, telephone, specialite)
                VALUES (%(nom)s, %(prenom)s, %(telephone)s, %(specialite)s)
            """

            with DBconnection() as conn:
                conn.execute(strsql_insert, valeurs_dict)

            flash("✅ Employé ajouté avec succès", "success")
            return redirect(url_for("employes_afficher", order_by="ASC", id_employe_sel=0))

        except Exception as e:
            flash(f"❌ Erreur lors de l'ajout de l'employé : {str(e)}", "danger")
            return redirect(url_for("employe_add_wtf"))

    return render_template("employes/employe_add_wtf.html", form=form)

@app.route("/employe_update", methods=['GET', 'POST'])
def employe_update_wtf():
    id_employe_update = request.values['id_employe']
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

            str_sql_update_employe = """UPDATE t_employes SET nom = %(value_nom_employe)s,
                                                              prenom = %(value_prenom_employe)s,
                                                              telephone = %(value_telephone_employe)s,
                                                              specialite = %(value_specialite_employe)s
                                                              WHERE id_employes = %(value_id_employe)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_employe, valeur_update_dictionnaire)

            flash(f"Donnée employé mise à jour !!", "success")
            print(f"Donnée employé mise à jour !!")

            return redirect(url_for('employes_afficher', id_employe_sel=id_employe_update))
        elif request.method == "GET":
            str_sql_id_employe = "SELECT * FROM t_employes WHERE id_employes = %(value_id_employe)s"
            valeur_select_dictionnaire = {"value_id_employe": id_employe_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_employe, valeur_select_dictionnaire)
            data_employe = mybd_conn.fetchone()
            print("data_employe ", data_employe, " type ", type(data_employe), " employé ",
                  data_employe["nom"])

            form_update_employe.nom_employe_update_wtf.data = data_employe["nom"]
            form_update_employe.prenom_employe_update_wtf.data = data_employe["prenom"]
            form_update_employe.telephone_employe_update_wtf.data = data_employe["telephone"]
            form_update_employe.specialite_employe_update_wtf.data = data_employe["specialite"]

    except Exception as Exception_employe_update_wtf:
        raise ExceptionEmployeUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                       f"{employe_update_wtf.__name__} ; "
                                       f"{Exception_employe_update_wtf}")

    return render_template("employes/employe_update_wtf.html", form_update_employe=form_update_employe)


from pymysql.err import IntegrityError

@app.route("/employe_delete", methods=['GET', 'POST'])
def employe_delete_wtf():
    data_employe_delete = None
    btn_submit_del = None
    id_employe_delete = request.values['id_employe_btn_delete_html']

    form_delete_employe = FormWTFDeleteEmploye()
    try:
        if form_delete_employe.submit_btn_annuler.data:
            return redirect(url_for("employes_afficher", order_by="ASC", id_employe_sel=0))

        if form_delete_employe.submit_btn_conf_del_employe.data:
            data_employe_delete = session['data_employe_delete']
            flash("Effacer l'employé de façon définitive de la BD !!!", "danger")
            btn_submit_del = True

        if form_delete_employe.submit_btn_del_employe.data:
            valeur_delete_dictionnaire = {"value_id_employe": id_employe_delete}
            str_sql_delete_employe = """DELETE FROM t_employes WHERE id_employes = %(value_id_employe)s"""
            try:
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_employe, valeur_delete_dictionnaire)

                flash("Employé définitivement effacé !!", "success")
                return redirect(url_for('employes_afficher', order_by="ASC", id_employe_sel=0))

            except IntegrityError as e:
                flash("❌ Impossible de supprimer cet employé car il est lié à un ou plusieurs rendez-vous.", "warning")
                return redirect(url_for("employes_afficher", order_by="ASC", id_employe_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_employe": id_employe_delete}
            str_sql_employe_delete = """SELECT * FROM t_employes WHERE id_employes = %(value_id_employe)s"""
            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_employe_delete, valeur_select_dictionnaire)
                data_employe_delete = mydb_conn.fetchall()
                session['data_employe_delete'] = data_employe_delete

            btn_submit_del = False

    except Exception as Exception_employe_delete_wtf:
        raise ExceptionEmployeDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                       f"{employe_delete_wtf.__name__} ; "
                                       f"{Exception_employe_delete_wtf}")

    return render_template("employes/employe_delete_wtf.html",
                           form_delete_employe=form_delete_employe,
                           btn_submit_del=btn_submit_del,
                           data_employe_del=data_employe_delete)


@app.route('/employes_rencontres')
def employes_rencontres():
    # Récupérer les paramètres de filtre
    employe_id = request.args.get('employe_id', '0')
    date_filter = request.args.get('date_filter', '')
    print("employe_id ", employe_id, " date_filter ", date_filter)
    try:
        with DBconnection() as mc_afficher:
            # 1. Récupérer tous les employés (pour le filtre)
            mc_afficher.execute("SELECT id_employes, nom, prenom FROM t_employes ORDER BY nom, prenom")
            employes = mc_afficher.fetchall()

            # 2. Construire la requête filtrée
            sql = """
                SELECT 
                    e.id_employes, e.nom, e.prenom, e.telephone, e.specialite,
                    c.id_clients, c.nom AS client_nom, c.prenom AS client_prenom, 
                    c.telephone AS client_telephone,
                    r.id_rencontrer, r.date_heure
                FROM t_employes e
                LEFT JOIN t_rencontrer r ON e.id_employes = r.FK_employes
                LEFT JOIN t_clients c ON r.FK_clients = c.id_clients
                WHERE 1=1
            """

            params = []

            # Filtre par employé
            if employe_id and employe_id != '0':
                sql += " AND e.id_employes = %s"
                params.append(employe_id)

            # Filtre par date
            if date_filter:
                sql += " AND DATE(r.date_heure) = %s"
                params.append(date_filter)

            sql += " ORDER BY e.nom, e.prenom, r.date_heure"
            print("sql ", sql)
            mc_afficher.execute(sql)
            result = mc_afficher.fetchall()

            # Organiser les données par employé
            employes_avec_rencontres = []
            current_employe = None

            for row in result:
                if current_employe is None or current_employe['id_employes'] != row['id_employes']:
                    if current_employe is not None:
                        employes_avec_rencontres.append(current_employe)

                    current_employe = {
                        'id_employes': row['id_employes'],
                        'nom': row['nom'],
                        'prenom': row['prenom'],
                        'telephone': row['telephone'],
                        'specialite': row['specialite'],
                        'rencontres': []
                    }

                if row['date_heure']:
                    current_employe['rencontres'].append({
                        'id_rencontrer': row['id_rencontrer'],
                        'client_nom': row['client_nom'],
                        'client_prenom': row['client_prenom'],
                        'client_telephone': row['client_telephone'],
                        'date_heure': row['date_heure']
                    })

            # Ajouter le dernier employé traité
            if current_employe is not None:
                employes_avec_rencontres.append(current_employe)

    except Exception as Exception_emp_rencontre_afficher:
        raise ExceptionEmpRencontreAfficher(f"{Path(__file__).name} ; {employes_rencontres.__name__} ; {Exception_emp_rencontre_afficher}")

    return render_template(
            'employes/emp_rencontres_afficher.html',
            employes=employes,
            employes_avec_rencontres=employes_avec_rencontres
        )


# Filtres de template
@app.template_filter('datetimeformat')
def datetimeformat(value, format='%d/%m/%Y %H:%M'):
    if value is None:
        return ""
    if isinstance(value, str):
        value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    return value.strftime(format)

