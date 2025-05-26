"""
    Fichier : gestion_clients_wtf_forms.py
    Auteur : OM 2021.03.22 - corrigé 2025.05.26
    Gestion des formulaires avec WTF
"""

from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField
from wtforms.validators import Length, Regexp


class FormWTFAjouterClients(FlaskForm):
    """
        Formulaire pour ajouter un client.
    """
    nom_client_regexp = r"^([A-ZÀ-ÖØ-Ýa-zà-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ' -]{1,}$"
    prenom_regexp = r"^([A-ZÀ-ÖØ-Ýa-zà-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ' -]{1,}$"
    telephone_regexp = r"^[0-9 +\-]{8,20}$"

    nom_client_wtf = StringField(
        "Nom du client",
        validators=[
            Length(min=2, max=20, message="Le nom doit contenir entre 2 et 20 caractères"),
            Regexp(nom_client_regexp, message="Le nom ne doit pas contenir de chiffres ou caractères spéciaux")
        ],
    )

    prenom_wtf = StringField(
        "Prénom du client",
        validators=[
            Length(min=2, max=20, message="Le prénom doit contenir entre 2 et 20 caractères"),
            Regexp(prenom_regexp, message="Le prénom ne doit pas contenir de chiffres ou caractères spéciaux")
        ],
    )

    telephone_wtf = StringField(
        "Téléphone",
        validators=[
            Length(min=8, max=20, message="Le téléphone doit contenir entre 8 et 20 caractères"),
            Regexp(telephone_regexp, message="Le téléphone ne doit contenir que des chiffres, espaces, + ou -")
        ],
    )

    submit = SubmitField("Enregistrer client")


class FormWTFUpdateClient(FlaskForm):
    """
        Formulaire pour modifier un client.
    """
    id_client = HiddenField("ID client")

    nom_client_update_regexp = r"^([A-ZÀ-ÖØ-Ýa-zà-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ' -]{1,}$"
    nom_client_update_wtf = StringField(
        "Nom du client",
        validators=[
            Length(min=2, max=20, message="Le nom doit contenir entre 2 et 20 caractères"),
            Regexp(nom_client_update_regexp, message="Le nom ne doit pas contenir de chiffres ou caractères spéciaux")
        ],
    )
    prenom_client_update_regexp = r"^([A-ZÀ-ÖØ-Ýa-zà-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ' -]{1,}$"
    prenom_client_update_wtf = StringField(
        "Prénom du client",
        validators=[
            Length(min=2, max=20, message="Le prénom doit contenir entre 2 et 20 caractères"),
            Regexp(prenom_client_update_regexp, message="Le prénom ne doit pas contenir de chiffres ou caractères spéciaux")
        ],
    )

    telephone_client_update_regexp = r"^[0-9 +\-]{8,20}$"
    telephone_client_update_wtf = StringField(
        "Téléphone",
        validators=[
            Length(min=8, max=20, message="Le téléphone doit contenir entre 8 et 20 caractères"),
            Regexp(telephone_client_update_regexp, message="Le téléphone ne doit contenir que des chiffres, espaces, + ou -")
        ],
    )

    submit = SubmitField("Mettre à jour client")


# Dans votre forms.py (ou là où vous définissez vos formulaires)
class FormWTFDeleteClient(FlaskForm):
    nom_client_delete_wtf = StringField('Nom')
    prenom_client_delete_wtf = StringField('Prénom')
    telephone_client_delete_wtf = StringField('Téléphone')
    submit_btn_del = SubmitField('Supprimer')
    submit_btn_annuler = SubmitField('Annuler')
    submit_btn_force_del = SubmitField('Forcer la suppression')  # Nouveau bouton