from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    usuario= db.Column(db.String, nullable=False)
    password= db.Column(db.String, nullable=False)

class Libro(db.Model):
    __tablename__ = "libro"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    autor = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)

class Rate(db.Model):
    __tablename__ = "bookrate"
    idcoment = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String, nullable=False)
    bookisbn = db.Column(db.String, nullable=False)
    bookrate = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String, nullable=False)





