from flask.ext.sqlalchemy import SQLAlchemy
from flask import g
import urllib2
from lxml import etree

db = SQLAlchemy()


class Deputado(db.Model):
    ideCadastro = db.Column(db.Integer, primary_key=True)
    nomeParlamentar = db.Column(db.String(200))
    nome = db.Column(db.String(200))
    condicao = db.Column(db.String(60))
    uf = db.Column(db.String(3))
    partido = db.Column(db.String(10))
    gabinete = db.Column(db.String(5))
    anexo = db.Column(db.String(5))
    fone = db.Column(db.String(15))
    email = db.Column(db.String(200))
    url_foto = db.Column(db.String(300))

    def __init__(self, ideCadastro, nomeParlamentar, nome, condicao, uf, partido, gabinete, anexo, fone, email,
                 url_foto):
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
        return '<Deputado %r>' % (self.nomeParlamentar)

    @classmethod
    def atualiza_database(self):
        data = urllib2.urlopen("http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/ObterDeputados").read()
        deputados = etree.XML(data)

        for deputado in deputados:
            if not Deputado.query.filter_by(ideCadastro=int(deputado.find('ideCadastro').text)).first():
                ideCadastro = int(deputado.find('ideCadastro').text)
                nome = deputado.find('nome').text
                nomeParlamentar = deputado.find('nomeParlamentar').text
                condicao = deputado.find('condicao').text
                uf = deputado.find('uf').text
                partido = deputado.find('partido').text
                gabinete = deputado.find('gabinete').text
                anexo = deputado.find('anexo').text
                fone = deputado.find('fone').text
                email = deputado.find('email').text
                url_foto = deputado.find('urlFoto').text
                dep = Deputado(ideCadastro, nomeParlamentar, nome, condicao, uf, partido, gabinete, anexo, fone, email,
                               url_foto)
                db.session.add(dep)

        db.session.commit()


class Despesa(db.Model):
    numRessarcimento = db.Column(db.Integer, primary_key=True)
    sgUF = db.Column(db.String(2))
    sgPartido = db.Column(db.String(2))
    txtDescricao = db.Column(db.String(200))
    txtFornecedor = db.Column(db.String(200))
    vlrLiquido = db.Column(db.Float)
    numMes = db.Column(db.Integer)
    numAno = db.Column(db.Integer)
    deputado_id = db.Column(db.Integer)


    def __init__(self, numRessarcimento, deputado_id, sgUf, sgPartido, txtDescricao, txtFornecedor, vlrLiquido, numMes,
                 numAno):
        self.numRessarcimento = numRessarcimento
        self.deputado_id = deputado_id
        self.sgUF = sgUf
        self.sgPartido = sgPartido
        self.txtDescricao = txtDescricao
        self.txtFornecedor = txtFornecedor
        self.vlrLiquido = vlrLiquido
        self.numMes = numMes
        self.numAno = numAno

    @classmethod
    def atualiza_database(self):
        db.create_all()
        tree = etree.parse("D:\eParlamentar\AnoAtual.xml")
        despesas = tree.getroot()[0]

        for despesa in despesas:
            numRessarcimento = int(despesa.find('numRessarcimento').text)
            sgUF = despesa.find('sgUF').text
            sgPartido = despesa.find('sgPartido').text
            txtDescricao = despesa.find('txtDescricao').text
            txtFornecedor = despesa.find('txtFornecedor').text
            vlrLiquido = float(despesa.find('vlrLiquido').text)
            numMes = despesa.find('numMes').text
            numAno = despesa.find('numAno').text
            deputado_id = int(despesa.find('ideCadastro').text)
            d = Despesa(numRessarcimento,deputado_id,sgUF,sgPartido,txtDescricao,txtFornecedor,vlrLiquido,numMes,numAno)
            db.session.add(d)
            db.session.commit()
        db.session.commit()

    def __repr__(self):
        return '<Despesa %r>' % self.numRessarcimento
