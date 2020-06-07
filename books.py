import os
import requests
import json
from models import * 
from sqlalchemy import create_engine , or_
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask ,session, render_template, request, jsonify

app = Flask(__name__, static_url_path= '/static')
DATABASE_URL = "postgres://sukhrtlmykocpd:402cc913b56fc2d2ec0b8e93babecd2f2bfc3dc335d147914622e43b422740c3@ec2-34-194-198-176.compute-1.amazonaws.com:5432/d2kf63ukmt2270"
engine = create_engine(DATABASE_URL)
# Check for environment variable
if not (DATABASE_URL):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SQLALCHEMY_DATABASE_URI"] = (DATABASE_URL)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
dbs = scoped_session(sessionmaker(bind=engine))
 
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")
    if request.methods == "POST": 
        return render_template ("login.html")
#Proceso de Login
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
    #return render_template("login.html")
        error = None  
        user = request.form.get("username")
        passw = request.form.get("password")
        Name = Usuario.query.filter_by(usuario=user).first()
        Password = Usuario.query.filter_by(password=passw).first()  
       
        if Name is None or Password is None:
            error = 'Nombre o password invalidos'
            return render_template("login.html", error= error)
        else:
            @app.context_processor
            def context_processor(): 
                return dict(key = user)
            return render_template("libros.html")
    return render_template("login.html")
#Sing Up Creacion de Usuarios. 
@app.route("/usuarios", methods=["GET","POST"])
def usuarios():
    if request.method == "POST":
        error = None
        message = None 
        usuario = request.form.get("user")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if usuario == "":
            error = "User cant be Empty"
            return render_template("Usuarios.html", error=error)
        
        elif password != confirm :
            error = "password not match"
            return render_template ("usuarios.html", error=error)
        else : 
            crea = Usuario(usuario = usuario, password = password) 
            db.session.add(crea)
            db.session.commit()
            message = "User Success..."
            render_template("usuarios.html", message=message )
    return render_template("usuarios.html")
    
@app.route("/logout")
def logout():
    db.session.clear()
    return render_template("index.html")



@app.route("/lista")
def lista(): 
    #if request.method == "GET":
       libros = Libro.query.limit(20)
       #Libro.query.limit(20)
       if libros is None:
          return render_template ("error.html", message="No existe listado de libros.")
       return render_template("lista.html", libros=libros)

@app.route("/lista", methods=["GET", "POST"])
def listas():
    if request.method  == "POST":
        error = None
        Consulta = request.form['consulta']
        #lib = Libro.query.limit(20)     
        #lib = Libro.query.filter_by(isbn = Consulta).first()
        lib = dbs.execute("Select isbn,title,autor,year from libro where  isbn = :isbn or title = :title or autor = :autor or year = :year", 
        {"isbn":Consulta, "title":Consulta,"autor":Consulta, "year": Consulta}).fetchall()
        #lib = Libro.query.filter(or_(Libro.isbn == Consulta, Libro.title == Consulta, Libro.autor == Consulta, Libro.year == Consulta)).first()
    return render_template("consulta.html", lib=lib)

@app.route("/comentario", methods=["GET", "POST"])
def comentario(): 
    if request.method == "POST":
        message = None
        user = request.form.get("usr")
        isbn = request.form.get("bcode")
        rate = request.form.get("combo")
        coment = request.form.get("comment")
        #Busca si el comentario al libro ya existe. 
        buscalibro = dbs.execute("Select * from bookrate where userid = :userid and bookisbn = :bookisbn", {"userid": user, "bookisbn": isbn }).fetchone()
        if buscalibro is None:
        #Guarda Comentario del libro 
            comentario = Rate(userid = user, bookisbn = isbn, bookrate=rate,comment=coment)
            db.session.add(comentario)
            db.session.commit()
            message ="Comment Send."
            return render_template ("comentario.html",message=message )    
        else: 
            message=  "The isbn comment is register for this user please register other isbn or other user"
            #"The comment is register please enter a distint isbn or distint user"
            return render_template("comentario.html", message=message)
    return render_template("comentario.html")
#Goodreads Review Data
@app.route("/api", methods=["GET", "POST"])
def api():
    if request.method == "POST":

        isbnapi = request.form.get("apiconsulta")
        #other = request.form.get("apiconsulta2")
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "rYWlL2Y3KkhTXSzpBgGMw", "isbns": isbnapi})
        if res.status_code !=200:
           error= "Api unsucessfull"  
           return render_template("api.html", error=error)
        else: 
           data = res.json()
           datos = data["books"]
           for books in datos:
              return render_template("/api.html", books=books)
    return render_template("/api.html")

@app.route("/apis/<isbn>", methods=["GET","POST"])
def apis(isbn):

    book = dbs.execute("select * from libro where isbn = :isbn", {"isbn": isbn})
    if book is None:
        return jsonify({"Error": "Invalid isbn number"}), 422
    for books in book :
        return jsonify({
                "isbn": books.isbn, 
                "title": books.title,
                "autor": books.autor, 
                "year": books.year 
            })

app.run(debug=False)
    

