from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Length, InputRequired, NumberRange


class FormWTFAjouterEvaluer(FlaskForm):
    """
    Formulaire pour ajouter une évaluation
    """
    note_wtf = IntegerField(
        "Note (1 à 5)",
        validators=[
            InputRequired(message="La note est obligatoire"),
            NumberRange(min=1, max=5, message="La note doit être entre 1 et 5"),
        ],
    )
    commentaire_wtf = TextAreaField(
        "Commentaire",
        validators=[
            Length(min=5, max=1000, message="Le commentaire doit faire entre 5 et 1000 caractères")
        ],
    )
    id_client_wtf = SelectField(
        "Client",
        coerce=int,
        validators=[InputRequired(message="Le client est obligatoire")],
        choices=[]  # À remplir dynamiquement dans la vue
    )
    id_service_wtf = SelectField(
        "Service",
        coerce=int,
        validators=[InputRequired(message="Le service est obligatoire")],
        choices=[]  # À remplir dynamiquement dans la vue
    )

    submit = SubmitField("Ajouter l'évaluation")


class FormWTFUpdateEvaluer(FlaskForm):
    """
    Formulaire pour mettre à jour une évaluation
    """
    note_update_wtf = IntegerField(
        "Note (1 à 5)",
        validators=[
            InputRequired(message="La note est obligatoire"),
            NumberRange(min=1, max=5, message="La note doit être entre 1 et 5"),
        ],
    )
    commentaire_update_wtf = TextAreaField(
        "Commentaire",
        validators=[
            Length(min=5, max=1000, message="Le commentaire doit faire entre 5 et 1000 caractères")
        ],
    )

    submit = SubmitField("Mettre à jour l'évaluation")


class FormWTFDeleteEvaluer(FlaskForm):
    """
    Formulaire pour supprimer une évaluation
    """
    note_evaluer_delete_wtf = IntegerField("Note (lecture seule)", render_kw={"readonly": True})
    commentaire_evaluer_delete_wtf = TextAreaField("Commentaire (lecture seule)", render_kw={"readonly": True})
    submit_btn_del = SubmitField("Effacer l'évaluation")
    submit_btn_conf_del = SubmitField("Confirmer la suppression")
    submit_btn_annuler = SubmitField("Annuler")
