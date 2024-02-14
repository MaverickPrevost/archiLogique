from .app import app, db
from .models import *

@app.cli.command()
def destroydb():
    """Destruction de toutes les tables."""
    db.drop_all()

@app.cli.command()
def syncdb():
    """Création de toutes les tables."""
    db.create_all()

@app.cli.command()
def resetdb():
    """Destruction et recréation de toutes les tables."""
    db.drop_all()
    db.create_all()

@app.cli.command()
def creation_questionnaire():
    """Création de toutes les tables et ajout d'un questionnaire."""
    questionnaire = Questionnaire(id=1, name="Questionnaire 1")
    db.session.add(questionnaire)
    db.session.commit()

@app.cli.command()
def creation_question():
    """Création de toutes les tables et ajout d'une question."""
    with app.app_context():
        question = Question(id=1, title="Question 1", question_type="Type 1", questionnaire_id=1)
        db.session.add(question)
        db.session.commit()

@app.cli.command()
def creation_simplequestion():
    """Création de toutes les tables et ajout d'une question simple."""
    simple_question = SimpleQuestion(
    title="Simple Question 1",
    question_type="simplequestion",
    questionnaire_id=1,
    first_alternative="Alternative 1",
    second_alternative="Alternative 2"
    )
    db.session.add(simple_question)
    db.session.commit()


@app.cli.command()
def creation_multiplequestion():
    """Création de toutes les tables et ajout d'une question à choix multiple."""
    multiple_question = MultipleQuestion(
    title="Multiple Question 1",
    question_type="multiple",
    questionnaire_id=1,
    first_alternative="Alternative 1",
    second_alternative="Alternative 2",
    third_alternative="Alternative 3",
    fourth_alternative="Alternative 4"
    )
    db.session.add(multiple_question)
    db.session.commit()
