"""
    Fichier : gestion_services_wtf_forms.py
    Auteur : Adapté par ChatGPT
    Gestion des formulaires avec WTF pour la table t_services
"""

from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SubmitField
from wtforms.validators import Length, InputRequired, DataRequired, Regexp, NumberRange


class FormWTFAjouterServices(FlaskForm):
    """
        Formulaire pour ajouter un service.
    """
    nom_service_regexp = r"^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ0-9\s\-']*$"
    nom_service_wtf = StringField("Nom du service",
                                  validators=[
                                      Length(min=2, max=50, message="min 2 max 50 caractères"),
                                      Regexp(nom_service_regexp,
                                             message="Le nom ne doit pas contenir de caractères spéciaux non autorisés")
                                  ])

    prix_service_wtf = DecimalField("Prix (€)",
                                    validators=[
                                        InputRequired(message="Le prix est requis"),
                                        NumberRange(min=0, max=9999, message="Prix entre 0 et 9999")
                                    ])

    duree_service_wtf = IntegerField("Durée (minutes)",
                                     validators=[
                                         InputRequired(message="La durée est requise"),
                                         NumberRange(min=1, max=1440, message="Durée entre 1 et 1440 minutes")
                                     ])

    submit = SubmitField("Ajouter service")


class FormWTFUpdateService(FlaskForm):
    """
        Formulaire pour modifier un service existant.
    """
    nom_service_update_regexp = r"^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ0-9\s\-']*$"
    nom_service_update_wtf = StringField("Nom du service",
                                         validators=[
                                             Length(min=2, max=50, message="min 2 max 50 caractères"),
                                             Regexp(nom_service_update_regexp,
                                                    message="Le nom ne doit pas contenir de caractères spéciaux non autorisés")
                                         ])

    prix_service_update_wtf = DecimalField("Prix (€)",
                                           validators=[
                                               InputRequired(message="Le prix est requis"),
                                               NumberRange(min=0, max=9999, message="Prix entre 0 et 9999")
                                           ])

    duree_service_update_wtf = IntegerField("Durée (minutes)",
                                            validators=[
                                                InputRequired(message="La durée est requise"),
                                                NumberRange(min=1, max=1440, message="Durée entre 1 et 1440 minutes")
                                            ])

    submit = SubmitField("Modifier service")


class FormWTFDeleteService(FlaskForm):
    """
        Formulaire pour supprimer un service (affichage en lecture seule).
    """
    nom_service_delete_wtf = StringField("Service à supprimer")
    submit_btn_del = SubmitField("Effacer service")
    submit_btn_conf_del = SubmitField("Êtes-vous sûr de vouloir supprimer ?")
    submit_btn_annuler = SubmitField("Annuler")
