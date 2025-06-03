"""Gestion des formulaires avec WTF pour les employés
Fichier : gestion_employes_wtf_forms.py
Auteur : OM 2022.04.11, modifié 2025.05.28
"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Length, InputRequired, Regexp


class FormWTFAddEmploye(FlaskForm):
    """
    Formulaire d'ajout d'un employé
    """
    nom_employe_wtf = StringField("Nom de l'employé", validators=[
        InputRequired("Nom obligatoire"),
        Length(min=2, max=50, message="Nom entre 2 et 50 caractères"),
        Regexp("^[A-Za-zÀ-ÿ\- ]+$", message="Lettres, espaces ou tirets uniquement")
    ])

    prenom_employe_wtf = StringField("Prénom de l'employé", validators=[
        InputRequired("Prénom obligatoire"),
        Length(min=2, max=50, message="Prénom entre 2 et 50 caractères"),
        Regexp("^[A-Za-zÀ-ÿ\- ]+$", message="Lettres, espaces ou tirets uniquement")
    ])

    telephone_employe_wtf = StringField("Téléphone", validators=[
        InputRequired("Téléphone obligatoire"),
        Regexp("^[0-9]{10}$", message="10 chiffres requis, sans espace")
    ])

    specialite_employe_wtf = StringField("Spécialité", validators=[
        InputRequired("Spécialité obligatoire"),
        Length(min=2, max=100, message="Spécialité entre 2 et 100 caractères")
    ])

    submit = SubmitField("Enregistrer employé")


class FormWTFUpdateEmploye(FlaskForm):
    """
    Formulaire de mise à jour d'un employé
    """
    nom_employe_update_wtf = StringField("Nom", validators=[
        InputRequired("Nom obligatoire"),
        Length(min=2, max=50),
        Regexp("^[A-Za-zÀ-ÿ\- ]+$")
    ])

    prenom_employe_update_wtf = StringField("Prénom", validators=[
        InputRequired("Prénom obligatoire"),
        Length(min=2, max=50),
        Regexp("^[A-Za-zÀ-ÿ\- ]+$")
    ])

    telephone_employe_update_wtf = StringField("Téléphone", validators=[
        InputRequired("Téléphone obligatoire"),
        Regexp("^[0-9]{10}$", message="10 chiffres requis")
    ])

    specialite_employe_update_wtf = StringField("Spécialité", validators=[
        InputRequired("Spécialité obligatoire"),
        Length(min=2, max=100)
    ])

    submit = SubmitField("Mettre à jour")


class FormWTFDeleteEmploye(FlaskForm):
    """
    Formulaire de suppression d'un employé
    """
    nom_employe_delete_wtf = StringField("Effacer cet employé", render_kw={'readonly': True})
    submit_btn_del_employe = SubmitField("Effacer employé")
    submit_btn_conf_del_employe = SubmitField("Êtes-vous sûr d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
