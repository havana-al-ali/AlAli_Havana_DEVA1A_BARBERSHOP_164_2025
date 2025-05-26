from pathlib import Path
from flask import flash, redirect, render_template, request, url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.evaluer.gestion_evaluer_wtf_forms import (
    FormWTFAjouterEvaluer,
    FormWTFDeleteEvaluer,
    FormWTFUpdateEvaluer,
)

# Afficher les évaluations
@app.route("/evaluer/", defaults={"order_by": "ASC", "id_evaluer_sel": 0})
@app.route("/evaluer/<string:order_by>/<int:id_evaluer_sel>", methods=['GET', 'POST'])
def evaluer_afficher(order_by, id_evaluer_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_evaluer_sel == 0:
                    strsql_evaluer_afficher = "SELECT * from t_evaluer ORDER BY id_evaluer ASC"
                    mc_afficher.execute(strsql_evaluer_afficher)
                elif order_by == "ASC":
                    valeur_id_evaluer_selected = {"value_id_evaluer_selected": id_evaluer_sel}
                    strsql_evaluer_afficher = """
                        SELECT * FROM t_evaluer WHERE id_evaluer = %(value_id_evaluer_selected)s
                    """
                    mc_afficher.execute(strsql_evaluer_afficher, valeur_id_evaluer_selected)
                else:
                    strsql_evaluer_afficher = "SELECT * FROM t_evaluer ORDER BY id_evaluer DESC"
                    mc_afficher.execute(strsql_evaluer_afficher)

                data_evaluer = mc_afficher.fetchall()

                if not data_evaluer and id_evaluer_sel == 0:
                    flash('La table "t_evaluer" est vide.', "warning")
                elif not data_evaluer and id_evaluer_sel > 0:
                    flash("L'évaluation demandée n'existe pas.", "warning")
                else:
                    flash("Données évaluations affichées.", "success")

        except Exception as e:
            raise ExceptionEvaluerAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{evaluer_afficher.__name__} ; "
                                          f"{e}")

    return render_template("evaluer/evaluer_afficher.html", data=data_evaluer)

# Ajouter une évaluation
@app.route("/evaluer_ajouter", methods=['GET', 'POST'])
def evaluer_ajouter_wtf():
    form = FormWTFAjouterEvaluer()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                # Adapte ici selon tes champs dans la table t_evaluer
                note = form.note_wtf.data
                commentaire = form.commentaire_wtf.data
                id_client = form.id_client_wtf.data
                id_service = form.id_service_wtf.data  # Modifie ici si c'est FK_services et pas FK_employes

                valeurs_insertion = {
                    "value_note": note,
                    "value_commentaire": commentaire,
                    "value_id_client": id_client,
                    "value_id_service": id_service
                }

                strsql_insert_evaluer = """
                    INSERT INTO t_evaluer (note, commentaire, FK_clients, FK_services) 
                    VALUES (%(value_note)s, %(value_commentaire)s, %(value_id_client)s, %(value_id_service)s)
                """

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_evaluer, valeurs_insertion)

                flash("Évaluation ajoutée avec succès.", "success")
                return redirect(url_for('evaluer_afficher', order_by='DESC', id_evaluer_sel=0))

        except Exception as e:
            raise ExceptionEvaluerAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{evaluer_ajouter_wtf.__name__} ; "
                                            f"{e}")

    return render_template("evaluer/evaluer_ajouter_wtf.html", form=form)

# Mettre à jour une évaluation
@app.route("/evaluer_update", methods=['GET', 'POST'])
def evaluer_update_wtf():
    id_evaluer_update = request.values.get('id_evaluer', None)
    if id_evaluer_update is None:
        flash("Erreur : aucune évaluation sélectionnée pour la mise à jour.", "danger")
        return redirect(url_for('evaluer_afficher', order_by='ASC', id_evaluer_sel=0))

    form_update = FormWTFUpdateEvaluer()

    try:
        if request.method == "POST" and form_update.submit.data:
            note_update = form_update.note_update_wtf.data
            commentaire_update = form_update.commentaire_update_wtf.data

            valeur_update = {
                "value_id_evaluer": id_evaluer_update,
                "value_note": note_update,
                "value_commentaire": commentaire_update
            }

            str_sql_update_evaluer = """
                UPDATE t_evaluer
                SET note = %(value_note)s,
                    commentaire = %(value_commentaire)s
                WHERE id_evaluer = %(value_id_evaluer)s
            """

            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_evaluer, valeur_update)

            flash("Évaluation mise à jour.", "success")
            return redirect(url_for('evaluer_afficher', order_by="ASC", id_evaluer_sel=id_evaluer_update))

        elif request.method == "GET":
            str_sql_id_evaluer = "SELECT * FROM t_evaluer WHERE id_evaluer = %(value_id_evaluer)s"
            valeur_select = {"value_id_evaluer": id_evaluer_update}

            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_evaluer, valeur_select)
                data_evaluer = mybd_conn.fetchone()

            if data_evaluer:
                form_update.note_update_wtf.data = data_evaluer["note"]
                form_update.commentaire_update_wtf.data = data_evaluer["commentaire"]
            else:
                flash("Évaluation non trouvée pour mise à jour.", "warning")
                return redirect(url_for('evaluer_afficher', order_by="ASC", id_evaluer_sel=0))

    except Exception as e:
        raise ExceptionEvaluerUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                       f"{evaluer_update_wtf.__name__} ; "
                                       f"{e}")

    return render_template("evaluer/evaluer_update_wtf.html", form_update=form_update)

# Supprimer une évaluation
@app.route("/evaluer_delete", methods=['GET', 'POST'])
def evaluer_delete_wtf():
    id_evaluer_delete = request.values.get('id_evaluer_btn_delete_html', None)
    if id_evaluer_delete is None:
        flash("Erreur : aucune évaluation sélectionnée pour la suppression.", "danger")
        return redirect(url_for('evaluer_afficher', order_by="ASC", id_evaluer_sel=0))

    form_delete = FormWTFDeleteEvaluer()

    try:
        if request.method == "POST" and form_delete.validate_on_submit():
            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("evaluer_afficher", order_by="ASC", id_evaluer_sel=0))

            if form_delete.submit_btn_del.data:
                str_sql_delete_evaluer = "DELETE FROM t_evaluer WHERE id_evaluer = %(value_id_evaluer)s"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_evaluer, {"value_id_evaluer": id_evaluer_delete})

                flash("Évaluation supprimée.", "success")
                return redirect(url_for('evaluer_afficher', order_by="ASC", id_evaluer_sel=0))

        elif request.method == "GET":
            str_sql_evaluer = "SELECT * FROM t_evaluer WHERE id_evaluer = %(value_id_evaluer)s"
            with DBconnection() as mc_conn:
                mc_conn.execute(str_sql_evaluer, {"value_id_evaluer": id_evaluer_delete})
                data_evaluer_delete = mc_conn.fetchone()

            if data_evaluer_delete:
                form_delete.note_evaluer_delete_wtf.data = data_evaluer_delete["note"]
                form_delete.commentaire_evaluer_delete_wtf.data = data_evaluer_delete["commentaire"]
            else:
                flash("Évaluation non trouvée pour suppression.", "warning")
                return redirect(url_for('evaluer_afficher', order_by="ASC", id_evaluer_sel=0))

    except Exception as e:
        raise ExceptionEvaluerDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                       f"{evaluer_delete_wtf.__name__} ; "
                                       f"{e}")

    return render_template("evaluer/evaluer_delete_wtf.html",
                           form_delete=form_delete,
                           data_evaluer_delete=data_evaluer_delete)
