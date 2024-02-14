# models.py
from datetime import datetime
from app import db

class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    questions = db.relationship('Question', backref='questionnaire', lazy=True)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f"Questionnaire('{self.title}')"

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'questions': [q.to_json() for q in self.questions]
        }

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # 'simple' or 'multiple'
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'), nullable=False)
    answers = db.relationship('Answer', backref='question', lazy=True)

    def __init__(self, content, question_type, questionnaire_id):
        self.content = content
        self.question_type = question_type
        self.questionnaire_id = questionnaire_id

    def __repr__(self):
        return f"Question('{self.content}', '{self.question_type}')"

    def to_json(self):
        return {
            'id': self.id,
            'content': self.content,
            'question_type': self.question_type,
            'answers': [a.to_json() for a in self.answers]
        }

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    def __init__(self, content, question_id):
        self.content = content
        self.question_id = question_id

    def __repr__(self):
        return f"Answer('{self.content}')"

    def to_json(self):
        return {
            'id': self.id,
            'content': self.content
        }
