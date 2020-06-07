import os
import csv
from flask import Flask, session,render_template,request
from models import *

app = Flask(__name__)
DATABASE_URL = "postgres://sukhrtlmykocpd:402cc913b56fc2d2ec0b8e93babecd2f2bfc3dc335d147914622e43b422740c3@ec2-34-194-198-176.compute-1.amazonaws.com:5432/d2kf63ukmt2270"

# Check for environment variable
if not (DATABASE_URL):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SQLALCHEMY_DATABASE_URI"] = (DATABASE_URL)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn,title, autor,year in reader:
        book = Libro(isbn=isbn, title=title, autor=autor,year=year)
        db.session.add(book)
        print(f"Agregando libro {isbn},{title},{autor},{year}")
        db.session.commit()
if __name__ == "__main__":
    with app.app_context():
        main()

