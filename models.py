from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()


class Course(db.Model):
    __tablename__ = 'course'
    __mapper_args__ = {'order_by': 'code'}
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(120))
    exams = db.relationship('Exam', backref='course')
    questions = association_proxy('exams', 'questions')

    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __repr__(self):
        return self.code + ' ' + self.name

    @property
    def string(self):
        return self.code


class Exam(db.Model):
    __tablename__ = 'exam'
    __mapper_args__ = {'order_by': 'name'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    questions = db.relationship('Question', backref='exam')

    def __init__(self, name, course_id):
        self.name = name
        self.course_id = course_id

    def __repr__(self):
        return self.name

    @property
    def string(self):
        return self.course.code + '_' + self.name


class Question(db.Model):
    __tablename__ = 'question'
    __mapper_args__ = {'order_by': 'id'}
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    image = db.Column(db.String)
    alternatives = db.relationship('Alternative', backref='question', order_by='Alternative.number')
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'))
    course = association_proxy('exam', 'course')

    def __init__(self, text, exam_id, image=""):
        self.text = text
        self.exam_id = exam_id
        self.image = image

    def __repr__(self):
        return self.text


class Alternative(db.Model):
    __tablename__ = 'alternative'
    __mapper_args__ = {'order_by': 'number'}

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    text = db.Column(db.String)
    correct = db.Column(db.Boolean)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    def __init__(self, text, number, correct, question_id):
        self.text = text
        self.number = number
        self.correct = correct
        self.question_id = question_id

    def __repr__(self):
        return self.text
