"""
    Fichier : gestion_clients_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp


class FormWTFAjouterClients(FlaskForm):
    """
        Dans le formulaire "clients_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_client_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_client_wtf = StringField("Clavioter le client ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                   Regexp(nom_client_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ] )
    prenom_regexp = ""
    prenom_wtf = StringField("Nom personne ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                          Regexp(prenom_regexp,
                                                                 message="Pas de chiffres, de caractères "
                                                                         "spéciaux, "
                                                                         "d'espace à double, de double "
                                                                         "apostrophe, de double trait union")
                                                          ])

    telephone_regexp = ""
    telephone_wtf = StringField("telephone ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                          Regexp(prenom_regexp,
                                                                 message="Pas de chiffres, de caractères "
                                                                         "spéciaux, "
                                                                         "d'espace à double, de double "
                                                                         "apostrophe, de double trait union")
                                                          ])
    submit = SubmitField("Enregistrer personne")


class FormWTFUpdateClient(FlaskForm):
    """
        Dans le formulaire "client_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_client_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_client_update_wtf = StringField("Clavioter le client ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(nom_client_update_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    date_client_wtf_essai = DateField("Essai date", validators=[InputRequired("Date obligatoire"),
                                                               DataRequired("Date non valide")])
    submit = SubmitField("Update client")


class FormWTFDeleteClient(FlaskForm):
    """
        Dans le formulaire "client_delete_wtf.html"

        nom_client_delete_wtf : Champ qui reçoit la valeur du client, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "client".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_client".
    """
    nom_client_delete_wtf = StringField("Effacer ce client")
    submit_btn_del = SubmitField("Effacer client")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
