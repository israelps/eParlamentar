from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class Deputado(db.Model):
    ideCadastro = db.Column(db.Integer, primary_key=True)
    nomeParlamentar = db.Column(db.String(80))
    nome = db.Column(db.String(100))
    condicao = db.Column(db.String(20))
    uf = db.Column(db.String(2))
    partido = db.Column(db.String(5))
    gabinete = db.Column(db.Integer)
    anexo = db.Column(db.Integer)
    fone = db.Column(db.String(10))
    email = db.Column(db.String(30))
    url_foto = db.Column(db.String(100))

    def __init__(self, ideCadastro, nomeParlamentar, nome, condicao, uf, partido, gabinete, anexo, fone, email, url_foto):
        self.ideCadastro = ideCadastro
        self.nomeParlamentar = nomeParlamentar
        self.nome = nome
        self.condicao = condicao
        self.uf = uf
        self.partido = partido
        self.gabinete = gabinete
        self.anexo = anexo
        self.fone = fone
        self.email = email
        self.url_foto = url_foto

        def __repr__(self):
            return '<Deputado %r>' % self.nomeParlamentar
